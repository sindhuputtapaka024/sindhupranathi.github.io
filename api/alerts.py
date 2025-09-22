import streamlit as st
import requests

SLACK_WEBHOOK_URL = st.secrets["slack"]["WEBHOOK_URL"]

def send_slack_alert(employee_name, manager_name, times, reasons, adp_punch_ids):
    payload = {
        "text": ":rotating_light: Auto clock-outs threshold exceeded",
        "blocks": [
            {"type":"section","text":{"type":"mrkdwn","text":f"*Auto clock-outs: {len(times)} (24h window)*"}} ,
            {"type":"section","fields":[
                {"type":"mrkdwn","text":f"*Employee:* {employee_name}"},
                {"type":"mrkdwn","text":f"*Manager:* {manager_name}"},
                {"type":"mrkdwn","text":f"*Times:* {', '.join(times)}"},
                {"type":"mrkdwn","text":f"*Reason:* {', '.join(reasons)}"}
            ]},
            {"type":"context","elements":[{"type":"mrkdwn","text":f"ADP punches: {', '.join(adp_punch_ids)}"}]}
        ]
    }
    requests.post(SLACK_WEBHOOK_URL, json=payload)
