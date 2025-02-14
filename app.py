import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="SQGLP Stock Analysis", layout="wide")
st.title("📊 SQGLP Stock Analysis Dashboard")

try:
    df = pd.read_csv("sqglp_results.csv")
    st.success("✅ Data Loaded Successfully!")

    st.sidebar.header("📌 Filter Options")

    tickers = df["Ticker"].unique().tolist()
    selected_tickers = st.sidebar.multiselect("Select Tickers", tickers, default=tickers)

    sectors = df["Sector"].unique().tolist()
    selected_sector = st.sidebar.selectbox("Select Sector", ["All"] + sectors)

    df = df[df["Ticker"].isin(selected_tickers)]
    if selected_sector != "All":
        df = df[df["Sector"] == selected_sector]

    st.subheader("📊 Filtered Stock Analysis Data")
    st.dataframe(df)

    fig = px.bar(df, x="Ticker", y="SQGLP_Score", color="Sector", title="SQGLP Scores by Sector")
    st.plotly_chart(fig)

    fig_pie = px.pie(df, names="Sector", title="Stock Distribution by Sector")
    st.plotly_chart(fig_pie)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    st.download_button(
        "📥 Download Data",
        data=df.to_csv(index=False),
        file_name=f"sqglp_results_{timestamp}.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("❌ `sqglp_results.csv` not found! Please run `main.py` first.")