import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🚀 Stock Analysis System")

stock = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if st.button("Analyze"):
    data = yf.download(stock, start="2022-01-01")

    if data.empty:
        st.error("Invalid Stock Symbol")
        st.stop()

    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()

    delta = data['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]

    def safe(value):
        if pd.isna(value):
            return "N/A"
        return round(float(value), 2)

    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Price", safe(latest['Close']))
    col2.metric("RSI", safe(latest['RSI']))
    col3.metric("MA20", safe(latest['MA20']))

    st.subheader("💡 Signal")

    rsi = latest['RSI']
    price = latest['Close']
    ma20 = latest['MA20']

    if pd.isna(rsi) or pd.isna(ma20):
        st.warning("Not enough data")
        signal = "WAIT"
    else:
        if rsi < 30 and price > ma20:
            st.success("STRONG BUY 📈")
            signal = "BUY"
        elif rsi > 70 and price < ma20:
            st.error("STRONG SELL 📉")
            signal = "SELL"
        else:
            st.info("HOLD 🤝")
            signal = "HOLD"

    st.subheader("🤖 AI Prediction")

    recent = data['Close'].tail(10)

    if len(recent) < 2:
        st.write("Not enough data")
        trend = 0
    else:
        trend = np.polyfit(range(len(recent)), recent, 1)[0]
        if trend > 0:
            st.write("📈 Uptrend likely")
        else:
            st.write("📉 Downtrend likely")

    st.subheader("📊 Chart")

    fig, ax = plt.subplots()
    ax.plot(data['Close'], label="Price")
    ax.plot(data['MA20'], label="MA20")
    ax.plot(data['MA50'], label="MA50")
    ax.legend()
    st.pyplot(fig)

    st.subheader("🧠 Final Decision")

    if signal == "BUY" and trend > 0:
        st.success("✅ FINAL: BUY")
    elif signal == "SELL" and trend < 0:
        st.error("❌ FINAL: SELL")
    else:
        st.info("⚖️ FINAL: WAIT")

    st.subheader("📌 Summary")
    st.write(f"Signal: {signal}")
