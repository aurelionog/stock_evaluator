import unittest
from unittest.mock import patch, MagicMock
from main_code import (
    fetch_historical_data,
    calculate_moving_averages,
    calculate_dividend_yield,
    calculate_total_dividends,
    analyze_stock,
)

class TestStockAnalysisFunctions(unittest.TestCase):

    @patch('your_stock_analysis_module.yf.download')
    def test_fetch_historical_data(self, mock_yf_download):
        # Create a mock DataFrame to simulate the API response
        mock_data = MagicMock()
        mock_data.empty = False  # Simulate a non-empty DataFrame
        mock_yf_download.return_value = mock_data

        # Call the function with a symbol
        symbol = 'AAPL'
        data = fetch_historical_data(symbol)

        # Assertions
        mock_yf_download.assert_called_once_with(symbol, start='2022-01-01', end='2022-12-31')
        self.assertFalse(data.empty)  # Ensure that the result is not an empty DataFrame

    def test_calculate_moving_average(self):
        # Create a mock DataFrame with sample historical data
        mock_data = MagicMock()
        mock_data['Close'] = [100, 110, 120, 130, 140]

        # Calculate moving averages
        short_ma = calculate_moving_average(mock_data, window=2)
        long_ma = calculate_moving_average(mock_data, window=5)

        # Assertions
        self.assertEqual(list(short_ma), [None, 105.0, 115.0, 125.0, 135.0])
        self.assertEqual(list(long_ma), [None, None, None, None, 120.0])

    def test_calculate_dividend_yield(self):
        # Calculate dividend yield
        dividend_yield = calculate_dividend_yield(total_dividends=2.0, initial_price=100.0)

        # Assertion
        self.assertAlmostEqual(dividend_yield, 2.0)

    def test_calculate_total_dividends(self):
        # Create a mock DataFrame with sample dividend data
        mock_dividend_data = MagicMock()
        mock_dividend_data['Dividends'] = [0.5, 0.3, 0.4]

        # Calculate total dividends
        total_dividends = calculate_total_dividends(mock_dividend_data)

        # Assertion
        self.assertAlmostEqual(total_dividends, 1.2)

    def test_analyze_stock(self):
        # Create a mock DataFrame with sample historical data
        mock_data = MagicMock()
        mock_data['Close'] = [100, 105, 110, 105, 100]

        # Create a mock DataFrame with sample dividend data
        mock_dividend_data = MagicMock()
        mock_dividend_data['Dividends'] = [0.2, 0.3, 0.2, 0.1, 0.2]

        # Perform stock analysis
        recommendation = analyze_stock(mock_data, mock_dividend_data, stop_loss_percent=5, profit_target_percent=10)

        # Assertion
        self.assertEqual(recommendation, 'Hold')

if __name__ == '__main__':
    unittest.main()
