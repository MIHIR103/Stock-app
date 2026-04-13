import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("Stock Analysis")

stock = st.text_input("Enter Stock", "RELIANCE.NS")

if st.button("Analyze"):

    data = yf.download(stock, start="2022-01-01")

    if data.empty:
        st.write("Invalid Stock")
    else:
        data['MA20'] = data['Close'].rolling(20).mean()

        latest = data.iloc[-1]

        st.write("Price:", round(latest['Close'],2))

        delta = data['Close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100/(1+rs))

        st.write("RSI:", round(rsi.iloc[-1],2))

        plt.plot(data['Close'])
        plt.plot(data['MA20'])
        st.pyplot(plt)
