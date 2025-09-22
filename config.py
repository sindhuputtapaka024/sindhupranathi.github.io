import streamlit as st

# GoTo API credentials from secrets
GOTO_BASE_URL = st.secrets["goto"]["GOTO_BASE_URL"]
GOTO_ACCESS_TOKEN = st.secrets["goto"]["GOTO_ACCESS_TOKEN"]

# ADP (optional)
ADP_BASE_URL = st.secrets["adp"]["BASE_URL"]  # if you add ADP secrets
ADP_CLIENT_ID = st.secrets["adp"]["CLIENT_ID"]
ADP_CLIENT_SECRET = st.secrets["adp"]["CLIENT_SECRET"]
