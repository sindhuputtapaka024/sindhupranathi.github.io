import pandas as pd
import streamlit as st
from logic.calls import fetch_calls

def render_userwise_view(start, end):
    st.subheader("👩‍⚕️ User View")
    df = fetch_calls(start, end)
    if df.empty:
        st.warning("No call data available.")
        return

    # Aggregate by user
    summary = df.groupby("user_name").agg({
        "duration_seconds": "sum",
        "status": lambda x: (x=="missed").sum()
    }).rename(columns={"duration_seconds":"Total Duration (sec)","status":"Missed Calls"})

    st.dataframe(summary)
    st.bar_chart(summary[["Total Duration (sec)", "Missed Calls"]])
