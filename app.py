import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Pro Stock Analysis Dashboard")

stock = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if st.button("Analyze"):

    data = yf.download(stock, start="2022-01-01")

    if data.empty:
        st.error("Invalid Stock Symbol")
        st.stop()

    # Indicators
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()

    delta = data['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]

    def safe(val):
        return round(val, 2) if pd.notna(val) else "N/A"

    # Metrics
    st.subheader("📌 Key Metrics")
    c1, c2, c3 = st.columns(3)

    c1.metric("Price", safe(latest['Close']))
    c2.metric("RSI", safe(latest['RSI']))
    c3.metric("MA20", safe(latest['MA20']))

    # Signal
    st.subheader("💡 Signal")

    rsi = latest['RSI']
    price = latest['Close']
    ma20 = latest['MA20']

    if pd.isna(rsi) or pd.isna(ma20):
        st.warning("Not enough data yet")
        signal = "WAIT"
    else:
        if rsi < 30 and price > ma20:
            st.success("🟢 STRONG BUY")
            signal = "BUY"
        elif rsi > 70 and price < ma20:
            st.error("🔴 STRONG SELL")
            signal = "SELL"
        else:
            st.info("🟡 HOLD")
            signal = "HOLD"

    # AI Prediction
    st.subheader("🤖 AI Prediction")

    recent = data['Close'].tail(10)

    if len(recent) > 1:
        trend = np.polyfit(range(len(recent)), recent, 1)[0]
        st.write("📈 Uptrend" if trend > 0 else "📉 Downtrend")
    else:
        trend = 0
        st.write("Not enough data")

    # Price Chart
    st.subheader("📈 Price Chart")

    fig, ax = plt.subplots()
    ax.plot(data['Close'], label="Price", linewidth=2)
    ax.plot(data['MA20'], label="MA20")
    ax.plot(data['MA50'], label="MA50")
    ax.legend()
    st.pyplot(fig)

    # RSI Chart
    st.subheader("📉 RSI Chart")

    fig2, ax2 = plt.subplots()
    ax2.plot(data['RSI'], label="RSI")
    ax2.axhline(30, linestyle='--')
    ax2.axhline(70, linestyle='--')
    ax2.legend()
    st.pyplot(fig2)

    # Final Decision
    st.subheader("🧠 Final Decision")

    if signal == "BUY" and trend > 0:
        st.success("✅ FINAL: BUY")
    elif signal == "SELL" and trend < 0:
        st.error("❌ FINAL: SELL")
    else:
        st.info("⚖️ FINAL: WAIT")

    # Summary
    st.subheader("📌 Summary")
    st.write(f"Trend: {'Uptrend' if trend > 0 else 'Downtrend'}")
    st.write(f"Signal: {signal}")
