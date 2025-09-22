import requests
import pandas as pd
from datetime import datetime
from logic.adp import get_clock_status, punch_out
from logic.alerts import send_slack_alert
import streamlit as st

GOTO_BASE_URL = st.secrets["goto"]["GOTO_BASE_URL"]
GOTO_ACCESS_TOKEN = st.secrets["goto"]["GOTO_ACCESS_TOKEN"]

cache = {}

def fetch_calls(start_date, end_date):
    url = f"{GOTO_BASE_URL}/v2/calls"
    headers = {"Authorization": f"Bearer {GOTO_ACCESS_TOKEN}"}
    params = {"startTime": f"{start_date}T00:00:00Z", "endTime": f"{end_date}T23:59:59Z"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json().get("calls", [])
        return pd.DataFrame(data)
    else:
        st.error(f"Error fetching GoTo data: {response.status_code}")
        return pd.DataFrame()

def check_inactivity(employee_id, employee_name, manager_name, last_input_ts, call_active):
    now = datetime.utcnow()
    inactive_minutes = (now - last_input_ts).total_seconds() / 60
    if inactive_minutes >= 20 and not call_active:
        status = get_clock_status(employee_id)
        if status and status.get("clocked_in"):
            punch_id = punch_out(employee_id)
            if punch_id:
                if employee_id not in cache:
                    cache[employee_id] = {"times": [], "reasons": [], "punch_ids": []}
                cache[employee_id]["times"].append(now.strftime("%H:%M"))
                cache[employee_id]["reasons"].append("Inactive ≥20 min, no active call")
                cache[employee_id]["punch_ids"].append(str(punch_id))
                if len(cache[employee_id]["times"]) > 2:
                    send_slack_alert(employee_name, manager_name,
                                     cache[employee_id]["times"],
                                     cache[employee_id]["reasons"],
                                     cache[employee_id]["punch_ids"])

def process_calls_and_inactivity(employees, start_date, end_date):
    df_calls = fetch_calls(start_date, end_date)
    if df_calls.empty:
        st.warning("No call data found for the selected range.")
        return pd.DataFrame()
    for emp in employees:
        emp_calls = df_calls[df_calls["user_id"] == emp["id"]]
        call_active = False
        if not emp_calls.empty:
            call_active = any(emp_calls["status"].isin(["active","wrapup","ringing"]))
        check_inactivity(emp["id"], emp["name"], emp["manager"], emp["last_input_ts"], call_active)
    return df_calls
