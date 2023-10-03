import yfinance as yf
import pandas as pd
import numpy as np

# Function to fetch historical stock data
def fetch_historical_data(ticker_symbol):
    stock_data = yf.Ticker(ticker_symbol)
    return stock_data.history(period="1y")

# Function to calculate moving averages
def calculate_moving_averages(data):
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()
    return data

# Function to calculate volatility (standard deviation of daily returns)
def calculate_volatility(data):
    returns = data['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252)  # Assuming 252 trading days in a year
    return volatility

# Function to analyze a stock and make a recommendation
def analyze_stock(ticker_symbol, initial_price, historical_data, stop_loss_percent, profit_target_percent):
    current_price = historical_data['Close'][-1]

    if current_price > historical_data['50_MA'][-1] and current_price > historical_data['200_MA'][-1]:
        recommendation = "Recommendation: Buy (Golden Cross)"
    elif current_price < historical_data['50_MA'][-1] and current_price < historical_data['200_MA'][-1]:
        recommendation = "Recommendation: Sell (Death Cross)"
    else:
        recommendation = "Recommendation: Hold"

    volatility = calculate_volatility(historical_data)
    roi = ((current_price - initial_price) / initial_price) * 100

    # Calculate the stop-loss price
    stop_loss_price = initial_price * (1 - stop_loss_percent / 100)

    # Calculate the profit-taking price based on the profit target
    profit_target_price = initial_price * (1 + profit_target_percent / 100)

    return {
        "Ticker Symbol": ticker_symbol,
        "Recommendation": recommendation,
        "Initial Price": f"{initial_price:.2f}",
        "Current Price": f"{current_price:.2f}",
        "Volatility (annualized)": f"{volatility:.2f}",
        "ROI (%)": f"{roi:.2f}",
        "Stop-Loss Price": f"{stop_loss_price:.2f}",
        "Profit Target Price": f"{profit_target_price:.2f}"
    }

# Function to analyze stocks from a CSV file
def analyze_stocks_from_csv(csv_file_path, stop_loss_percent, profit_target_percent):
    if isinstance(csv_file_path, pd.DataFrame):
        stock_df = csv_file_path
    else:
        stock_df = pd.read_csv(csv_file_path)
    analysis_results = []

    for index, row in stock_df.iterrows():
        ticker_symbol = row[0]
        initial_price = row[1]
        historical_data = fetch_historical_data(ticker_symbol)
        historical_data = calculate_moving_averages(historical_data)
        result = analyze_stock(ticker_symbol, initial_price, historical_data, stop_loss_percent, profit_target_percent)
        analysis_results.append(result)

    return pd.DataFrame(analysis_results)

