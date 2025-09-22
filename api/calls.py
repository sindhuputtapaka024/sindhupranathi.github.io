import requests
import pandas as pd
from config import GOTO_BASE_URL, GOTO_ACCESS_TOKEN
import streamlit as st

def fetch_calls(start_date, end_date):
    """
    Fetch GoTo call events from API
    """
    url = f"{GOTO_BASE_URL}/v2/calls"
    headers = {"Authorization": f"Bearer {GOTO_ACCESS_TOKEN}"}
    params = {
        "startTime": f"{start_date}T00:00:00Z",
        "endTime": f"{end_date}T23:59:59Z"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json().get("calls", [])
        df = pd.DataFrame(data)
        return df
    else:
        st.error(f"Error fetching GoTo data: {response.status_code}")
        return pd.DataFrame()
