import streamlit as st
import pandas as pd
from logic.calls import process_calls_and_inactivity
from datetime import datetime

def render_userwise_view(start_date, end_date):
    """
    Render per-user dashboard: calls, inactive time, auto clock-outs.
    """
    st.header("User-wise Dashboard")

    # Example employee list
    employees_list = [
        {"id":"u_123", "name":"Jane Doe", "manager":"John Smith", "last_input_ts": datetime.utcnow() - pd.Timedelta(minutes=25)},
        {"id":"u_124", "name":"Bob Lee", "manager":"Alice Wong", "last_input_ts": datetime.utcnow() - pd.Timedelta(minutes=10)}
    ]

    # Fetch GoTo calls and process inactivity
    df_calls = process_calls_and_inactivity(employees_list, start_date, end_date)

    if df_calls.empty:
        st.info("No calls in this date range.")
        return

    # Show table of calls per user
    st.subheader("Call Activity")
    st.dataframe(df_calls)

    # Show summary per user
    st.subheader("Auto Clock-Out Summary")
    for emp in employees_list:
        cache = getattr(__import__("logic.calls"), "cache")  # access cache from calls.py
        if emp["id"] in cache:
            st.markdown(f"**{emp['name']}**")
            times = ", ".join(cache[emp["id"]]["times"])
            reasons = ", ".join(cache[emp["id"]]["reasons"])
            st.write(f"Auto Clock-Outs: {len(cache[emp['id']]['times'])} | Times: {times} | Reasons: {reasons}")
