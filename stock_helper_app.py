import streamlit as st
import yfinance as yf
import pandas as pd

# App title
st.title("📈 Stock Helper App")
st.write("Enter an amount, pick a stock, and get buy/sell guidance based on technical indicators.")

# User inputs
ticker_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL").upper()
amount_to_invest = st.number_input("Amount to invest ($):", min_value=1.0, value=100.0, step=1.0)

if st.button("Analyze"):
    try:
        # Fetch historical data
        data = yf.download(ticker_symbol, period="6mo")

        # Check if data is empty
        if data.empty:
            st.error(f"No data found for ticker '{ticker_symbol}'. Please check the symbol and try again.")
        elif "Close" not in data.columns:
            st.error(f"'Close' column not found. Available columns: {list(data.columns)}")
            st.write(data.tail())  # For debugging
        else:
            # Get the latest closing price (FIXED)
            latest_price = data["Close"].iloc[-1]

            # Simple moving averages for basic trend check
            sma_20 = data["Close"].rolling(window=20).mean().iloc[-1]
            sma_50 = data["Close"].rolling(window=50).mean().iloc[-1]

            # Display current price
            st.subheader(f"Latest Price for {ticker_symbol}: ${latest_price:.2f}")

            # Buy/Sell signal based on SMA crossover
            if sma_20 > sma_50:
                signal = "BUY"
                color = "green"
            elif sma_20 < sma_50:
                signal = "SELL"
                color = "red"
            else:
                signal = "HOLD"
                color = "gray"

            st.markdown(f"**Recommendation:** <span style='color:{color}; font-size: 20px;'>{signal}</span>", unsafe_allow_html=True)

            # Calculate how many shares can be bought
            shares = amount_to_invest / latest_price
            st.write(f"With ${amount_to_invest:.2f}, you can buy approximately **{shares:.2f} shares**.")

            # Show last few days of data
            st.write("Recent Data:")
            st.dataframe(data.tail())

    except Exception as e:
        st.error(f"An error occurred: {e}")
