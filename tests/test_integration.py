
import pandas as pd
import pytest
from main_code import analyze_stocks_from_csv

def test_stock_analysis_integration():
    import os
    # Create a temporary CSV file with sample data for testing
    csv_data = """
    Symbol,Initial_Price
    AAPL,150.00
    MSFT,250.00
    """
    with open(f'{os.getcwd()}/tests/mock_data/test_stock_data.csv', 'w') as f:
        f.write(csv_data)

    # Perform the stock analysis from the CSV file
    stop_loss_percent = 10
    profit_target_percent = 15
    analysis_df = analyze_stocks_from_csv(f'{os.getcwd()}/tests/mock_data/test_stock_data.csv', stop_loss_percent, profit_target_percent)

    # Clean up: Remove the temporary CSV file
    
    os.remove(f'{os.getcwd()}/tests/mock_data/test_stock_data.csv')

    # Perform assertions on the analysis results
    assert len(analysis_df) == 2
    assert 'Symbol' in analysis_df.columns
    assert 'Initial_Price' in analysis_df.columns
    assert 'Recommendation' in analysis_df.columns

    # Add specific assertions based on the expected results for the given test data
    assert analysis_df.loc[analysis_df['Symbol'] == 'AAPL', 'Recommendation'].values[0] == 'Hold'
    assert analysis_df.loc[analysis_df['Symbol'] == 'MSFT', 'Recommendation'].values[0] == 'Hold'

if __name__ == '__main__':
    pytest.main()
