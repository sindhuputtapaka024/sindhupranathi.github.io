import streamlit as st
import pandas as pd
from logic.calls import fetch_calls

def render_overall_view(start, end):
    st.subheader("📊 Overall View")
    df = fetch_calls(start, end)
    if df.empty:
        st.warning("No call data available.")
        return

    df["duration_min"] = df["duration_seconds"] / 60
    total_calls = len(df)
    missed_calls = len(df[df["status"]=="missed"])

    st.metric("Total Calls", total_calls)
    st.metric("Missed Calls", missed_calls)

    df["date"] = pd.to_datetime(df["start_time"]).dt.date
    summary = df.groupby("date").agg({"duration_min":"sum","status":"count"}).rename(columns={"status":"Total Calls"})
    st.line_chart(summary)
