import yfinance as yf
import pandas as pd
import numpy as np
import logging

# Define constants
TRADING_DAYS_PER_YEAR = 252

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch historical stock data with error handling
def fetch_historical_data(ticker_symbol):
    try:
        stock_data = yf.Ticker(ticker_symbol)
        return stock_data.history(period="1y")
    except Exception as e:
        logger.error(f"Error fetching data for {ticker_symbol}: {e}")
        return None

# Function to calculate moving averages
def calculate_moving_averages(data):
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()
    return data

# Function to calculate volatility (standard deviation of daily returns)
def calculate_volatility(data):
    returns = data['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    return volatility

# Function to calculate the total dividends over the last year
def calculate_total_dividends(historical_data):
    try:
        if 'Dividends' in historical_data.columns:
            last_year_dividends = historical_data['Dividends'].dropna()
            if not last_year_dividends.empty:
                total_dividends = last_year_dividends.sum()
                return total_dividends
    except KeyError:
        pass  # Fall back to 0.0 if there's an issue with dividend data
    return 0.0  # Default to 0.0 if dividend data is missing or empty

# Function to analyze a stock and make a recommendation
def analyze_stock(ticker_symbol, initial_price, historical_data, stop_loss_percent, profit_target_percent):
    if historical_data is None:
        return {
            "Ticker Symbol": ticker_symbol,
            "Recommendation": "Recommendation: Data Retrieval Error",
        }

    current_price = historical_data['Close'][-1]
    total_dividends = 0.0  # Initialize total_dividends to 0

    if current_price > historical_data['50_MA'][-1] and current_price > historical_data['200_MA'][-1]:
        recommendation = "Recommendation: Buy (Golden Cross)"
    elif current_price < historical_data['50_MA'][-1] and current_price < historical_data['200_MA'][-1]:
        recommendation = "Recommendation: Sell (Death Cross)"
    else:
        total_dividends = calculate_total_dividends(historical_data)

        if total_dividends == 0.0:
            recommendation = "Recommendation: Data Issue (Missing Dividend Data)"
        else:
            try:
                last_dividend = historical_data['Dividends'][-1]
                if not pd.isnull(last_dividend):
                    recommendation = "Recommendation: Hold (Based on Total Dividends)"
                else:
                    recommendation = "Recommendation: Data Issue (Dividend Data Missing or Incorrect)"
            except KeyError:
                recommendation = "Recommendation: Data Issue (Dividend Data Missing or Incorrect)"

    volatility = calculate_volatility(historical_data)
    roi = ((current_price - initial_price) / initial_price) * 100

    stop_loss_price = initial_price * (1 - stop_loss_percent / 100)
    profit_target_price = initial_price * (1 + profit_target_percent / 100)

    return {
        "Ticker Symbol": ticker_symbol,
        "Recommendation": recommendation,
        "Initial Price": f"{initial_price:.2f}",
        "Current Price": f"{current_price:.2f}",
        "Volatility (annualized)": f"{volatility:.2f}",
        "ROI (%)": f"{roi:.2f}",
        "Stop-Loss Price": f"{stop_loss_price:.2f}",
        "Profit Target Price": f"{profit_target_price:.2f}",
        "Total Dividends": f"{total_dividends:.2f}"
    }

# Function to analyze stocks from a CSV file
def analyze_stocks_from_csv(csv_file_path, stop_loss_percent, profit_target_percent):
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