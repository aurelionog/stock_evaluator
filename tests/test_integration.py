import os
import pandas as pd
import pytest
from main_code import analyze_stocks_from_csv

# Define the path to your CSV file
csv_file_path = f"{os.getcwd()}/stock_prices.csv"

# Integration test
def test_integration():
    # Read the CSV data
    csv_data = pd.read_csv(csv_file_path)

    # Perform the analysis using your script
    stop_loss_percent = 10.0
    profit_target_percent = 15.0
    result_df = analyze_stocks_from_csv(csv_data, stop_loss_percent, profit_target_percent)

    # Check that the result DataFrame is not empty
    assert not result_df.empty

    # You can add additional assertions based on your script's behavior

if __name__ == "__main__":
    pytest.main()
