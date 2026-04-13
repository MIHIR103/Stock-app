import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Pro Stock Analysis Dashboard")

stock = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if st.button("Analyze"):

    data = yf.download(stock, start="2022-01-01")

    if data.empty:
        st.error("Invalid Stock Symbol")
    else:
        # ---------------- INDICATORS ----------------
        data['MA20'] = data['Close'].rolling(20).mean()
        data['MA50'] = data['Close'].rolling(50).mean()

        # RSI
        delta = data['Close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        latest = data.iloc[-1]

        # ---------------- METRICS ----------------
        st.subheader("📈 Key Metrics")

        col1, col2, col3 = st.columns(3)
        col1.metric("Price", round(latest['Close'], 2))
        col2.metric("RSI", round(latest['RSI'], 2))
        col3.metric("MA20", round(latest['MA20'], 2))

        # ---------------- SIGNAL ----------------
        st.subheader("💡 Signal")

        if latest['RSI'] < 30:
            st.success("STRONG BUY 📈")
        elif latest['RSI'] > 70:
            st.error("STRONG SELL 📉")
        else:
            st.info("HOLD / WAIT 🤝")

        # ---------------- GRAPH ----------------
        st.subheader("📊 Price Chart")

        fig, ax = plt.subplots()
        ax.plot(data['Close'], label="Price")
        ax.plot(data['MA20'], label="MA20")
        ax.plot(data['MA50'], label="MA50")
        ax.legend()
        st.pyplot(fig)

        # ---------------- RSI CHART ----------------
        st.subheader("📉 RSI Chart")

        fig2, ax2 = plt.subplots()
        ax2.plot(data['RSI'], label="RSI")
        ax2.axhline(30)
        ax2.axhline(70)
        ax2.legend()
        st.pyplot(fig2)

        # ---------------- SUMMARY ----------------
        st.subheader("🧠 Analysis Summary")

        if latest['Close'] > latest['MA20']:
            st.write("📈 Trend: Uptrend")
        else:
            st.write("📉 Trend: Downtrend")
