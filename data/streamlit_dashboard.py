import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 SQGLP Stock Analysis Dashboard")

try:
    df = pd.read_csv("sqglp_results.csv")
    st.success("✅ Data Loaded Successfully!")

    # Sorting & Filtering
    df = df.sort_values("SQGLP_Score", ascending=False)
    min_score, max_score = st.sidebar.slider("SQGLP Score Range", int(df["SQGLP_Score"].min()), int(df["SQGLP_Score"].max()), (60, 100))
    df = df[(df["SQGLP_Score"] >= min_score) & (df["SQGLP_Score"] <= max_score)]

    st.dataframe(df)

    # Interactive Charts
    fig = px.bar(df, x="Ticker", y="SQGLP_Score", color="SQGLP_Score", title="SQGLP Scores")
    st.plotly_chart(fig)

    # Download Button
    st.download_button("Download CSV", df.to_csv(index=False), "sqglp_results.csv")

except FileNotFoundError:
    st.error("❌ Data not found! Run `main.py` first.")