import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("💼 Professional Trading System")

stocks_input = st.text_input(
    "Enter Stocks (comma separated)",
    "RELIANCE.NS,TCS.NS,INFY.NS"
)

timeframe = st.selectbox("Select Timeframe", ["1d", "1h", "15m"])

if st.button("Run Pro Analysis"):

    stocks = [s.strip() for s in stocks_input.split(",")]

    results = []

    for stock in stocks:

        data = yf.download(stock, period="1mo", interval=timeframe)

        if data.empty:
            continue

        close = data['Close']

        # Moving averages
        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()

        # RSI
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        macd = ema12 - ema26
        signal_line = macd.ewm(span=9).mean()

        price = close.iloc[-1]

        # Signals
        signal = "NO TRADE"

        if price > ma20.iloc[-1] and macd.iloc[-1] > signal_line.iloc[-1] and rsi.iloc[-1] < 70:
            signal = "BUY"
        elif price < ma20.iloc[-1] and macd.iloc[-1] < signal_line.iloc[-1] and rsi.iloc[-1] > 30:
            signal = "SELL"

        # Support/Resistance
        resistance = data['High'].tail(20).max()
        support = data['Low'].tail(20).min()

        if signal == "BUY":
            entry = price
            sl = support
            target = entry + (entry - sl) * 2
        elif signal == "SELL":
            entry = price
            sl = resistance
            target = entry - (sl - entry) * 2
        else:
            entry = sl = target = 0

        rr = abs(target - entry) / abs(entry - sl) if signal != "NO TRADE" else 0

        results.append({
            "Stock": stock,
            "Signal": signal,
            "Price": round(price,2),
            "RSI": round(rsi.iloc[-1],2) if not pd.isna(rsi.iloc[-1]) else "N/A",
            "Entry": round(entry,2),
            "SL": round(sl,2),
            "Target": round(target,2),
            "RR": round(rr,2)
        })

        # Chart
        st.subheader(f"📊 Chart - {stock}")
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])
        st.plotly_chart(fig, use_container_width=True)

    df = pd.DataFrame(results)

    if not df.empty:
        st.subheader("📈 Trade Setup")
        st.dataframe(df)

        best = df[df["Signal"] != "NO TRADE"]

        if not best.empty:
            best = best.sort_values(by="RR", ascending=False).iloc[0]
            st.success(f"🔥 Best Trade: {best['Stock']} → {best['Signal']} (RR: {best['RR']})")
        else:
            st.info("No strong trades")
