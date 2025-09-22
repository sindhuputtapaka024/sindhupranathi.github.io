import requests
import streamlit as st
from datetime import datetime, timedelta
from config import ADP_BASE_URL, ADP_CLIENT_ID, ADP_CLIENT_SECRET

def get_access_token():
    url = f"{ADP_BASE_URL}/auth/oauth/v2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": ADP_CLIENT_ID,
        "client_secret": ADP_CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error("Failed to get ADP token")
        return None

def get_clock_status(employee_id):
    token = get_access_token()
    if not token:
        return None
    url = f"{ADP_BASE_URL}/time/v1/workers/{employee_id}/clock-status"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    return None

def punch_out(employee_id, reason="AUTO_INACTIVITY_20M"):
    token = get_access_token()
    if not token:
        return None
    url = f"{ADP_BASE_URL}/time/v1/workers/{employee_id}/punches"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "action": "OUT",
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 201:
        return resp.json().get("id")
    else:
        st.error(f"Failed to punch out: {resp.text}")
        return None
