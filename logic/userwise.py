import streamlit as st
from datetime import datetime
from logic import calls

def render_userwise_view(start_date, end_date, user_id, employees_list):
    emp = next(e for e in employees_list if e["id"] == user_id)
    st.header(f"Dashboard for {emp['name']}")

    # Process calls
    df_calls = calls.process_calls_and_inactivity(employees_list, start_date, end_date)

    if df_calls.empty:
        st.info("No calls in this date range.")
        return

    # Filter for this user
    user_calls = df_calls[df_calls["user_id"] == user_id]

    st.subheader("Call Activity")
    st.dataframe(user_calls)

    # Auto Clock-Out Summary
    st.subheader("Auto Clock-Out Summary")
    if user_id in calls.cache:
        times = ", ".join(calls.cache[user_id]["times"])
        reasons = ", ".join(calls.cache[user_id]["reasons"])
        st.write(f"Auto Clock-Outs: {len(calls.cache[user_id]['times'])}")
        st.write(f"Times: {times}")
        st.write(f"Reasons: {reasons}")
