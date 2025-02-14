import streamlit as st
import pandas as pd
import plotly.express as px
import talib

st.title("📊 SQGLP Stock Analysis Dashboard")

try:
    # Load Data
    df = pd.read_csv("sqglp_results.csv")
    st.success("✅ Data Loaded Successfully!")

    # Sorting & Filtering
    df = df.sort_values("SQGLP_Score", ascending=False)
    min_score, max_score = st.sidebar.slider("SQGLP Score Range", int(df["SQGLP_Score"].min()), int(df["SQGLP_Score"].max()), (60, 100))
    df = df[(df["SQGLP_Score"] >= min_score) & (df["SQGLP_Score"] <= max_score)]

    # Display Filtered Data
    st.dataframe(df)

    # Interactive Chart for SQGLP Scores
    fig = px.bar(df, x="Ticker", y="SQGLP_Score", color="SQGLP_Score", title="SQGLP Scores")
    st.plotly_chart(fig)

    # Technical Indicators - Add Technical Analysis
    st.subheader("📈 Technical Indicators")

    # Check if we have 'Close' price for calculating technical indicators
    if 'Close' in df.columns:
        # Calculate Moving Averages
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        df['MA_200'] = df['Close'].rolling(window=200).mean()

        # RSI (Relative Strength Index)
        df['RSI'] = talib.RSI(df['Close'], timeperiod=14)

        # MACD (Moving Average Convergence Divergence)
        df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

        # Display Moving Averages
        st.subheader("Moving Averages")
        fig_ma = px.line(df, x='Date', y=['MA_50', 'MA_200'], title="50 and 200 Period Moving Averages")
        st.plotly_chart(fig_ma)

        # Display RSI
        st.subheader("Relative Strength Index (RSI)")
        fig_rsi = px.line(df, x='Date', y='RSI', title="RSI (14 Period)")
        st.plotly_chart(fig_rsi)

        # Display MACD
        st.subheader("MACD")
        fig_macd = px.line(df, x='Date', y=['MACD', 'MACD_signal'], title="MACD and Signal Line")
        st.plotly_chart(fig_macd)

    else:
        st.warning("❌ 'Close' price column is missing for technical analysis. Please ensure your data contains 'Close' prices.")

    # Download CSV Button
    st.download_button("Download CSV", df.to_csv(index=False), "sqglp_results.csv")

except FileNotFoundError:
    st.error("❌ Data not found! Run `main.py` first.")