import streamlit as st

st.set_page_config(page_title="Nurse Dashboard", layout="wide")
st.title("Nurse Auto Clock-Out Dashboard")

# Load employee data
import json

with open("data/employees.json") as f:
    employees = json.load(f)

for emp in employees:
    st.subheader(emp["name"])
    st.write(f"Status: {emp['status']}")
    st.write(f"Last Input: {emp['last_input']}")
    st.write(f"Call State: {emp['call_state']}")
    st.write(f"Auto Clock-Outs: {emp['auto_clock_outs']}")
    st.write(f"Manager: {emp['manager']}")
    if emp["alert"]:
        st.warning("⚠️ Alert")
