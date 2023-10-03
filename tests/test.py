import pytest
import pandas as pd
from main_code import (
    fetch_historical_data,
    calculate_moving_averages,
    calculate_volatility,
    analyze_stock,
    analyze_stocks_from_csv,
)

# Example data for testing
example_stock_data = pd.DataFrame({
    'Close': [100.0, 101.0, 102.0, 103.0, 104.0],
})

# Mocking the yfinance module
class MockYFinance:
    @classmethod
    def Ticker(cls, symbol):
        return cls()

    def history(self, **kwargs):
        return example_stock_data

# Mocking yfinance to avoid real API calls
yf = MockYFinance()
import sys
sys.modules['yfinance'] = yf

# Unit tests
def test_fetch_historical_data():
    data = fetch_historical_data('AAPL')
    assert not data.empty

def test_calculate_moving_averages():
    data = example_stock_data.copy()
    data = calculate_moving_averages(data)
    assert '50_MA' in data.columns
    assert '200_MA' in data.columns

def test_calculate_volatility():
    data = example_stock_data.copy()
    volatility = calculate_volatility(data)
    assert isinstance(volatility, float)

def test_analyze_stock():
    ticker_symbol = 'AAPL'
    initial_price = 100.0
    historical_data = example_stock_data.copy()
    stop_loss_percent = 5.0
    profit_target_percent = 10.0
    result = analyze_stock(ticker_symbol, initial_price, historical_data, stop_loss_percent, profit_target_percent)
    assert 'Ticker Symbol' in result
    assert 'Recommendation' in result
    assert 'Initial Price' in result
    assert 'Current Price' in result
    assert 'Volatility (annualized)' in result
    assert 'ROI (%)' in result
    assert 'Stop-Loss Price' in result
    assert 'Profit Target Price' in result

def test_analyze_stocks_from_csv():
    csv_data = pd.DataFrame({
        'Symbol': ['AAPL', 'GOOGL'],
        'Initial_Price': [100.0, 2000.0],
    })
    stop_loss_percent = 5.0
    profit_target_percent = 10.0
    result_df = analyze_stocks_from_csv(csv_data, stop_loss_percent, profit_target_percent)
    assert not result_df.empty
    assert 'Ticker Symbol' in result_df.columns
    assert 'Recommendation' in result_df.columns
    assert 'Initial Price' in result_df.columns
    assert 'Current Price' in result_df.columns
    assert 'Volatility (annualized)' in result_df.columns
    assert 'ROI (%)' in result_df.columns
    assert 'Stop-Loss Price' in result_df.columns
    assert 'Profit Target Price' in result_df.columns

if __name__ == "__main__":
    pytest.main()
