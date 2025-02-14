import plotly.express as px
import pandas as pd
import streamlit as st

def plot_sqglp_trend(history_df):
    """Plots historical SQGLP score trends for selected stocks."""
    if "Date" not in history_df.columns or history_df.empty:
        st.warning("⚠️ No historical data available for trend analysis.")
        return

    history_df["Date"] = pd.to_datetime(history_df["Date"])  # Ensure proper date format

    fig = px.line(
        history_df,
        x="Date",
        y="SQGLP_Score",
        color="Ticker",
        title="📈 SQGLP Score Trend Over Time",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="SQGLP Score",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)