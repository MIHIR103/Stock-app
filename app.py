import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🚀 Advanced Stock Analysis App")

stocks_input = st.text_input("Enter Stock Symbols (comma separated)", "RELIANCE.NS,TCS.NS")

if st.button("Analyze"):

    stocks = [s.strip() for s in stocks_input.split(",")]

    st.subheader("📊 Multi-Stock Comparison")

    fig = go.Figure()

    for stock in stocks:
        data = yf.download(stock, period="3mo")
        if not data.empty:
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name=stock))

    st.plotly_chart(fig, use_container_width=True)

    # Single stock detailed (first one)
    stock = stocks[0]
    ticker = yf.Ticker(stock)
    data = ticker.history(period="3mo")

    if data.empty:
        st.error("Invalid stock")
        st.stop()

    st.subheader(f"🕯️ Candlestick Chart ({stock})")

    fig2 = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📐 Pattern Detection")

    last = data.iloc[-1]
    prev = data.iloc[-2]

    # Basic patterns
    if abs(last['Close'] - last['Open']) < (last['High'] - last['Low']) * 0.1:
        st.info("Doji Pattern ⚖️")

    elif last['Close'] > last['Open'] and prev['Close'] < prev['Open']:
        st.success("Bullish Reversal Pattern 📈")

    elif last['Close'] < last['Open'] and prev['Close'] > prev['Open']:
        st.error("Bearish Reversal Pattern 📉")

    # RSI
    close = data['Close']
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    st.subheader("📊 RSI")

    latest_rsi = rsi.iloc[-1]

    if pd.isna(latest_rsi):
        st.write("RSI not available")
        signal = "WAIT"
    elif latest_rsi < 30:
        st.success("BUY Signal 📈")
        signal = "BUY"
    elif latest_rsi > 70:
        st.error("SELL Signal 📉")
        signal = "SELL"
    else:
        st.info("HOLD 🤝")
        signal = "HOLD"

    # News
    st.subheader("📰 News")

    try:
        news = ticker.news
        if news:
            for n in news[:5]:
                st.write("🔹", n.get('title', 'No title'))
    except:
        st.write("News not available")

    # Final decision
    st.subheader("🧠 Final Decision")

    if signal == "BUY":
        st.success("Consider Buying")
    elif signal == "SELL":
        st.error("Consider Selling")
    else:
        st.info("Wait")
