import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Stock Analysis (Simple & Stable)")

stock = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if st.button("Analyze"):

    data = yf.download(stock, period="6mo")

    if data.empty:
        st.error("Invalid stock")
    else:
        close = data['Close']

        # Moving Average
        ma20 = close.rolling(20).mean()

        # RSI
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        latest_price = float(close.iloc[-1])
        latest_rsi = rsi.iloc[-1]

        # ---------------- BASIC INFO ----------------
        st.subheader("📌 Basic Info")
        st.write("Price:", round(latest_price, 2))

        if pd.isna(latest_rsi):
            st.write("RSI: Not available")
        else:
            st.write("RSI:", round(float(latest_rsi), 2))

        # ---------------- SIGNAL ----------------
        st.subheader("💡 Signal")

        if pd.isna(latest_rsi):
            st.write("Not enough data")
            signal = "WAIT"
        elif latest_rsi < 30:
            st.success("BUY 📈")
            signal = "BUY"
        elif latest_rsi > 70:
            st.error("SELL 📉")
            signal = "SELL"
        else:
            st.info("HOLD 🤝")
            signal = "HOLD"

        # ---------------- TREND ----------------
        st.subheader("📈 Trend")

        if latest_price > ma20.iloc[-1]:
            st.write("Uptrend 📈")
        else:
            st.write("Downtrend 📉")

        # ---------------- AI (Simple Trend) ----------------
        st.subheader("🤖 Prediction")

        recent = close.tail(10)

        if len(recent) > 1:
            slope = (recent.iloc[-1] - recent.iloc[0]) / len(recent)
            if slope > 0:
                st.write("📈 Uptrend likely")
            else:
                st.write("📉 Downtrend likely")

        # ---------------- CHART ----------------
        st.subheader("📊 Chart")

        fig, ax = plt.subplots()
        ax.plot(close, label="Price")
        ax.plot(ma20, label="MA20")
        ax.legend()
        st.pyplot(fig)

        # ---------------- FINAL DECISION ----------------
        st.subheader("🧠 Final Decision")

        if signal == "BUY":
           st.success("Consider Buying")
        elif signal == "SELL":
            st.error("Consider Selling")
        else:
            st.info("Wait & Watch")

        # ---------------- SUMMARY ----------------
        st.subheader("📌 Summary")
        st.write("Signal:", signal)
    
