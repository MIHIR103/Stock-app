import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🚀 Ultimate Stock Analysis System")

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

    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2

    latest = data.iloc[-1]

    # Metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Price", round(latest['Close'], 2))
    col2.metric("RSI", round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else "N/A")
    col3.metric("MA20", round(latest['MA20'], 2) if not pd.isna(latest['MA20']) else "N/A")

    # Price Action
    st.subheader("📈 Price Action")
    if latest['Close'] > latest['MA20']:
        st.write("📈 Bullish (Above MA20)")
    else:
        st.write("📉 Bearish (Below MA20)")

    # Signal
    st.subheader("💡 Buy/Sell Signal")
    signal = "HOLD"

    if not pd.isna(latest['RSI']):
        if latest['RSI'] < 30 and latest['Close'] > latest['MA20']:
            signal = "STRONG BUY"
            st.success(signal)
        elif latest['RSI'] > 70 and latest['Close'] < latest['MA20']:
            signal = "STRONG SELL"
            st.error(signal)
        else:
            st.info("HOLD")
    else:
        st.warning("Not enough data")

    # AI Prediction
    st.subheader("🤖 AI Prediction")
    recent = data['Close'].tail(10)
    trend = np.polyfit(range(len(recent)), recent, 1)[0]

    if trend > 0:
        st.write("📈 Uptrend likely")
    else:
        st.write("📉 Downtrend likely")

    # Fundamental
    st.subheader("💰 Fundamental Analysis")
    try:
        info = yf.Ticker(stock).info
        st.write("P/E:", info.get("trailingPE", "N/A"))
        st.write("EPS:", info.get("trailingEps", "N/A"))
        st.write("Market Cap:", info.get("marketCap", "N/A"))
    except:
        st.warning("No fundamental data")

    # Chart
    st.subheader("📊 Price Chart")
    fig, ax = plt.subplots()
    ax.plot(data['Close'], label="Price")
    ax.plot(data['MA20'], label="MA20")
    ax.plot(data['MA50'], label="MA50")
    ax.legend()
    st.pyplot(fig)

    # Final Decision
    st.subheader("🧠 Final Decision")
    if signal == "STRONG BUY" and trend > 0:
        st.success("BUY")
    elif signal == "STRONG SELL" and trend < 0:
        st.error("SELL")
    else:
        st.info("WAIT")

    # Summary
    st.subheader("📌 Summary")
    st.write(f"Trend: {'Uptrend' if trend > 0 else 'Downtrend'}")
    st.write(f"Signal: {signal}")

