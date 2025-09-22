import streamlit as st
import pandas as pd

def render_userwise_view(start, end):
    """
    User-level dashboard logic – breakdown by nurse/user
    """
    st.subheader("👩‍⚕️ User View")

    # Example dummy dataset
    users = ["Nurse A", "Nurse B", "Nurse C"]
    data = {
        "User": users,
        "Total Calls": [25, 40, 15],
        "Missed Calls": [2, 5, 1],
    }
    df = pd.DataFrame(data)

    # Show table
    st.write("### User Performance")
    st.dataframe(df)

    # Show bar chart
    st.bar_chart(df.set_index("User")[["Total Calls", "Missed Calls"]])
