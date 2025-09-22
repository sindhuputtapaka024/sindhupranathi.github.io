import streamlit as st
from logic.calls import process_calls_and_inactivity
from datetime import datetime
import pandas as pd

def render_userwise_view(start_date, end_date):
    st.header("User-wise Dashboard")
    employees_list = [
        {"id":"u_123", "name":"Jane Doe", "manager":"John Smith", "last_input_ts": datetime.utcnow()},
        {"id":"u_124", "name":"Bob Lee", "manager":"Alice Wong", "last_input_ts": datetime.utcnow()}
    ]
    df_calls = process_calls_and_inactivity(employees_list, start_date, end_date)
    if df_calls.empty:
        st.info("No calls in this date range.")
        return
    st.subheader("Call Activity")
    st.dataframe(df_calls)
    st.subheader("Auto Clock-Out Summary")
    from logic import calls
    for emp in employees_list:
        if emp["id"] in calls.cache:
            times = ", ".join(calls.cache[emp["id"]]["times"])
            reasons = ", ".join(calls.cache[emp["id"]]["reasons"])
            st.write(f"**{emp['name']}** → Auto Clock-Outs: {len(calls.cache[emp['id']]['times'])} | Times: {times} | Reasons: {reasons}")
