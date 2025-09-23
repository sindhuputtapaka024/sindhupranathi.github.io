import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from logic import calls  # import calls module directly

def render_overall_view(start_date, end_date):
    """
    Render overall dashboard: all calls, total inactive users, auto clock-outs.
    """
    st.header("Overall Dashboard")

    # Example employee list (replace with DB/ADP API in production)
    employees_list = [
        {"id": "u_123", "name": "Jane Doe", "manager": "John Smith",
         "last_input_ts": datetime.utcnow() - timedelta(minutes=25)},
        {"id": "u_124", "name": "Bob Lee", "manager": "Alice Wong",
         "last_input_ts": datetime.utcnow() - timedelta(minutes=10)}
    ]

    # Process calls and inactivity
    df_calls = calls.process_calls_and_inactivity(employees_list, start_date, end_date)

    if df_calls.empty:
        st.info("No calls in this date range.")
        return

    # Normalize column names (in case API uses userId instead of user_id)
    if "userId" in df_calls.columns and "user_id" not in df_calls.columns:
        df_calls.rename(columns={"userId": "user_id"}, inplace=True)

    # --- Total calls ---
    st.subheader("Total Calls")
    st.metric("Total Calls", len(df_calls))

    # --- Calls by user ---
    st.subheader("Calls by User")
    calls_per_user = df_calls.groupby("user_id").size().reset_index(name="total_calls")
    st.bar_chart(calls_per_user.set_index("user_id"))

    # --- Auto clock-outs summary ---
    st.subheader("Auto Clock-Outs")
    cache = calls.cache  # use cache directly from calls.py
    summary = []
    for emp in employees_list:
        if emp["id"] in cache:
            summary.append({
                "User": emp["name"],
                "Auto Clock-Outs": len(cache[emp["id"]]["times"]),
                "Last Punch": cache[emp["id"]]["times"][-1] if cache[emp["id"]]["times"] else None
            })

    if summary:
        df_summary = pd.DataFrame(summary)
        st.table(df_summary)
    else:
        st.info("No auto clock-outs recorded in this period.")
