import streamlit as st
import pandas as pd

def render_overall_view(start, end):
    """
    Overall dashboard logic – simple metrics & charts
    """
    st.subheader("📊 Overall View")

    # Example dummy dataset
    data = {
        "Date": pd.date_range(start=start, end=end, freq="D"),
        "Total Calls": [10, 15, 20, 5, 12][: (end - start).days + 1],
        "Missed Calls": [2, 1, 3, 0, 1][: (end - start).days + 1],
    }
    df = pd.DataFrame(data)

    # Show table
    st.write("### Call Summary")
    st.dataframe(df)

    # Show chart
    st.line_chart(df.set_index("Date")[["Total Calls", "Missed Calls"]])
