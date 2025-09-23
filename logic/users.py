import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from logic import calls  # import once at top

def render_userwise_view(start_date, end_date):
    """
    Render per-user dashboard: shows individual call activity and auto clock-out details.
    """
    st.header("User-wise Dashboard")

    # Example employee list (replace with real data from ADP/DB)
    employees_list = [
        {"id": "u_123", "name": "Jane Doe", "manager": "John Smith",
         "last_input_ts": datetime.utcnow() - timedelta(minutes=15)},
        {"id": "u_124", "name": "Bob Lee", "manager": "Alice Wong",
         "last_input_ts": datetime.utcnow() - timedelta(minutes=5)}
    ]

    # Fetch calls + inactivity
    df_calls = calls.process_calls_and_inactivity(employees_list, start_date, end_date)

    if df_calls.empty:
        st.info("No calls in this date range.")
        return

    # Normalize column names
    if "userId" in df_calls.columns and "user_id" not in df_calls.columns:
        df_calls.rename(columns={"userId": "user_id"}, inplace=True)

    # --- Call Activity ---
    st.subheader("Call Activity")
    st.dataframe(df_calls)

    # --- Auto Clock-Out Summary ---
    st.subheader("Auto Clock-Out Summary")
    for emp in employees_list:
        if emp["id"] in calls.cache:
            times = ", ".join(calls.cache[emp["id"]]["times"])
            reasons = ", ".join(calls.cache[emp["id"]]["reasons"])
            punch_ids = ", ".join(calls.cache[emp["id"]]["punch_ids"])

            st.markdown(
                f"""
                **{emp['name']}**  
                - Auto Clock-Outs: `{len(calls.cache[emp['id']]['times'])}`  
                - Times: {times}  
                - Reasons: {reasons}  
                - Punch IDs: {punch_ids}
                """
            )
