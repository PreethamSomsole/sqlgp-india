import plotly.express as px
import pandas as pd
import streamlit as st

def generate_sector_heatmap(df):
    """Generates a heatmap based on stock sector performance."""
    if "Sector" not in df.columns or df.empty:
        st.warning("⚠️ No sector data available for heatmap.")
        return

    heatmap_data = df.groupby("Sector").mean().reset_index()

    fig = px.imshow(
        heatmap_data.drop(columns=["Sector"]),
        labels=dict(x="Metrics", y="Sector", color="Value"),
        x=heatmap_data.drop(columns=["Sector"]).columns,
        y=heatmap_data["Sector"],
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        title="📊 Sector Performance Heatmap",
        xaxis_title="Financial Metrics",
        yaxis_title="Sector",
    )

    st.plotly_chart(fig, use_container_width=True)