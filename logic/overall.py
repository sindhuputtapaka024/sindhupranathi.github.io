import streamlit as st
import pandas as pd
from logic.calls import process_calls_and_inactivity
from datetime import datetime

def render_overall_view(start_date, end_date):
    """
    Render overall dashboard: all calls, total inactive users, auto clock-outs.
    """
    st.header("Overall Dashboard")

    # Example employee list
    employees_list = [
        {"id":"u_123", "name":"Jane Doe", "manager":"John Smith", "last_input_ts": datetime.utcnow() - pd.Timedelta(minutes=25)},
        {"id":"u_124", "name":"Bob Lee", "manager":"Alice Wong", "last_input_ts": datetime.utcnow() - pd.Timedelta(minutes=10)}
    ]

    # Process calls and inactivity
    df_calls = process_calls_and_inactivity(employees_list, start_date, end_date)

    if df_calls.empty:
        st.info("No calls in this date range.")
        return

    # Total calls
    st.subheader("Total Calls")
    st.metric("Total Calls", len(df_calls))

    # Calls by user
    st.subheader("Calls by User")
    calls_per_user = df_calls.groupby("user_id").size().reset_index(name="total_calls")
    st.bar_chart(calls_per_user.set_index("user_id"))

    # Auto clock-outs summary
    st.subheader("Auto Clock-Outs")
    cache = getattr(__import__("logic.calls"), "cache")  # access cache from calls.py
    summary = []
    for emp in employees_list:
        if emp["id"] in cache:
            summary.append({
                "User": emp["name"],
                "Auto Clock-Outs": len(cache[emp["id"]]["times"])
            })
    if summary:
        df_summary = pd.DataFrame(summary)
        st.table(df_summary)
