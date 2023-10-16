import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from intraday_trading.intraday_trading_app import fetch_historical_data, calculate_technical_indicators, evaluate_buy_signal, calculate_stop_loss_price, calculate_max_reward_price, fetch_intraday_data, calculate_target_percent, calculate_intraday_target_price


# Streamlit App
st.title('Intraday Trading Signal Evaluator')

# Sidebar
st.sidebar.header('User Input Parameters')
stock_symbol = st.sidebar.text_input("Enter Stock Symbol:", "GOOG")
risk_percent = st.sidebar.slider("Set Risk Percentage:", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
intraday_days_back = st.sidebar.number_input("Days back for intraday analysis:", 7)



# Fetch and display historical data
with st.spinner('Fetching Historical Data...'):
    stock_data = fetch_historical_data(stock_symbol)

# Error handling for data fetching
if stock_data is None or stock_data.empty:
    st.error(f"No data available for {stock_symbol}. Cannot evaluate.")
else:
    stock_data = calculate_technical_indicators(stock_data)
    # Evaluate and display Buy/Sell signal
    st.header('Buy/Sell Signal')
    # Check if 'RSI' exists in stock_data
    if 'RSI' not in stock_data.columns or stock_data['RSI'].isna().all():
        st.write("RSI data is not available or insufficient. Cannot evaluate buy signal.")
    else:
        buy_signal, buy_price = evaluate_buy_signal(stock_data)
    signal_color = 'green' if buy_signal == 'buy' else 'red'
    st.markdown(f"<h2 style='text-align: center; color: {signal_color};'>{buy_signal.upper()}</h2>", unsafe_allow_html=True)

    if buy_signal == 'buy':
        buy_price = stock_data['Close'].iloc[-1]
        stop_loss_price = calculate_stop_loss_price(buy_price, risk_percent)
        max_reward_price = calculate_max_reward_price(buy_price, risk_percent)

        # Create a DataFrame for results and display as a table
        results_df = pd.DataFrame({
            'Metric': ['Buy Price', 'Stop Loss Price', 'Max Reward Price'],
            'Value': [f"${buy_price:.2f}", f"${stop_loss_price:.2f}", f"${max_reward_price:.2f}"]
        })
        st.table(results_df.set_index('Metric'))
    elif buy_signal == "buy_dip":
        buy_price = stock_data['Close'].iloc[-1]
        dip_threshold = buy_signal[1]
        results_df = pd.DataFrame({
            'Metric': ['Suggested Buy Price', 'Dip Threshold'],
            'Value': [f"${buy_price}", f"${dip_threshold}"]
        })
        st.table(results_df.set_index('Metric'))
    else:
        st.write('No buy signal detected.')
    
    # Main Content
    st.header('Historical Data Analysis')
    st.write('Here you can analyze the historical data of the selected stock.')

    # Display closing prices as a line chart
    st.line_chart(stock_data['Close'])

    # Calculate and display technical indicators
    with st.expander("Technical Indicators"):
        stock_data = calculate_technical_indicators(stock_data)
        st.table(stock_data.tail())



# Intraday Data Analysis
st.header('Intraday Data Analysis')
st.write('Here you can analyze the intraday data of the selected stock.')

# Fetch and display intraday data
with st.spinner('Fetching Intraday Data...'):
    intraday_data = fetch_intraday_data(stock_symbol, days_back=intraday_days_back)

# Error handling for intraday data fetching
if intraday_data is None or intraday_data.empty:
    st.error(f"No intraday data available for {stock_symbol}. Cannot evaluate.")
else:
    # Display intraday prices as a line chart
    st.line_chart(intraday_data['Close'])

    # Calculate and display intraday target price
    with st.expander("Intraday Target Price",expanded=True):
        target_percent = calculate_target_percent(intraday_data)
        intraday_target_price = calculate_intraday_target_price(intraday_data, target_percent)
        st.write(f"Automatically Calculated Target Percent: {target_percent:.2f}%")
        st.write(f"Intraday Target Price: ${intraday_target_price:.2f}")