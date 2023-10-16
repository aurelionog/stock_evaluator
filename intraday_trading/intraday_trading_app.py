import yfinance as yf
import pandas as pd
from datetime import datetime


def fetch_historical_data(stock_symbol, period="1y"):
    # Fetch historical stock data from Yahoo Finance
    stock = yf.Ticker(stock_symbol)
    historical_data = stock.history(period=period)
    return historical_data

def calculate_technical_indicators(data, short_window=50, long_window=200, rsi_window=14, macd_short=12, macd_long=26, macd_signal=9):
    # Calculate technical indicators (SMA, RSI, MACD)
    data['SMA_50'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_200'] = data['Close'].rolling(window=long_window).mean()
    data['RSI'] = compute_rsi(data['Close'], rsi_window)
    data['MACD'], data['Signal_Line'] = compute_macd(data['Close'], macd_short, macd_long, macd_signal)
    return data

def compute_rsi(data, window):
    # Calculate Relative Strength Index (RSI)
    delta = data.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_macd(data, short_window, long_window, signal_window):
    # Calculate Moving Average Convergence Divergence (MACD)
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal_line

def evaluate_buy_signal(data, rsi_threshold=30, dip_threshold_percent=2):
    if 'RSI' not in data.columns:
        return "not_buy", None

    # Define buy criteria
    if data['RSI'].iloc[-1] > rsi_threshold and data['Close'].iloc[-1] > data['SMA_50'].iloc[-1] and data['MACD'].iloc[-1] > data['Signal_Line'].iloc[-1]:
        return "buy", data['Close'].iloc[-1]
    else:
        # Check for "buy the dip" opportunity
        sma_50_last = data['SMA_50'].iloc[-1]
        close_last = data['Close'].iloc[-1]
        dip_threshold = sma_50_last * (1 - dip_threshold_percent / 100)

        if close_last < dip_threshold:
            return "buy_dip", dip_threshold
        else:
            return "not_buy", None

def calculate_reward_multiple(risk_percent, risk_reward_ratio):
    # Calculate the reward_multiple based on the risk_percent and risk_reward_ratio
    reward_multiple = risk_percent * risk_reward_ratio
    return reward_multiple

def calculate_stop_loss_price(buy_price, risk_percent=2):
    # Calculate stop-loss price based on risk percentage
    stop_loss_percent = risk_percent
    stop_loss_price = buy_price * (1 - stop_loss_percent / 100)
    return stop_loss_price

def calculate_max_reward_price(buy_price, risk_percent, risk_reward_ratio=2):
    # Calculate maximum reward price based on risk-reward ratio
    reward_multiple = calculate_reward_multiple(risk_percent, risk_reward_ratio)
    max_reward_price = buy_price * (1 + reward_multiple / 100)
    return max_reward_price


def fetch_intraday_data(stock_symbol, interval="1d", days_back=1):
    # Fetch intraday stock data from Yahoo Finance for the specified number of days back
    stock = yf.Ticker(stock_symbol)
    
    # Calculate the start and end date for the intraday data
    end_date = datetime.now().strftime("%Y-%m-%d")  # Current date in the format "YYYY-MM-DD"
    start_date = (datetime.now() - pd.DateOffset(days=days_back)).strftime("%Y-%m-%d")
    
    intraday_data = stock.history(period=interval, interval="1m", start=start_date, end=end_date)
    return intraday_data

def calculate_target_percent(intraday_data, time_period_minutes=30, target_percent_factor=1.5):
    if len(intraday_data) < time_period_minutes:
        print("Insufficient data for calculating target percent.")
        return 0
    
    last_close_price = intraday_data['Close'].iloc[-1]
    start_price = intraday_data['Close'].iloc[-time_period_minutes]
    
    if last_close_price == start_price:
        print("No price change in the specified time period.")
        return 0
    
    price_change = last_close_price - start_price
    target_percent = (price_change / start_price) * 100 * target_percent_factor
    
    return target_percent

def calculate_intraday_target_price(intraday_data, target_percent):
    # Calculate the intraday target price based on the target percent
    last_close_price = intraday_data['Close'].iloc[-1]
    target_price = last_close_price * (1 + target_percent / 100)
    return target_price
