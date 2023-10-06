
# Stock Analysis Tool

This Python tool is designed to help users analyze stock data and make investment decisions based on various factors such as moving averages, dividends, and more.

## Features

- Retrieve historical stock data from Yahoo Finance.

- Calculate moving averages (50-day and 200-day).

- Analyze stock recommendations based on moving averages and dividend data.

- Determine whether to Buy, Sell, or Hold a stock.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed.

- Required Python packages installed (`yfinance`, `pandas`, `numpy`, `pytest`, `coverage`).

## Installation

1\. Clone the repository:

```shell

   git clone https://github.com/yourusername/stock-analysis-tool.git

```

2\. Change into the project directory:

```shell

   cd stock-analysis-tool

```

3\. Install the required Python packages:

```shell

   pip install -r requirements.txt

```

## Usage

### Analyze Stocks from a CSV File

To analyze stocks from a CSV file, follow these steps:

1\. Create a CSV file with the following columns: `Symbol` and `Initial_Price`. Add the stock symbols and their initial prices for analysis.

2\. Run the analysis script:
``` shell

   python stock_analysis.py -f path/to/your/csv_file.csv -s 10 -p 15

```
Options:

``` shell
   - `-f` or `--file`: Specify the path to your CSV file.

   - `-s` or `--stop-loss`: Set the stop-loss percentage.

   - `-p` or `--profit-target`: Set the profit target percentage.

```

### Running Tests

To run unit tests using pytest, execute the following command:

```shell

pytest test_stock_analysis.py

```

To check code coverage using `coverage.py`, use the following commands:

```shell

coverage run -m pytest test_stock_analysis.py

coverage report -m

```

### Running Integration Tests

To run the integration test for the stock analysis workflow, execute the following command:

```shell

python test_stock_analysis_integration.py

```

## Contributing

Contributions are welcome! Please follow these guidelines:

1\. Fork the repository.

2\. Create a new branch for your feature or bug fix.

3\. Make your changes and add tests if applicable.

4\. Ensure that all tests pass.

5\. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [Yahoo Finance](https://finance.yahoo.com/) for providing stock data.

## Contact

If you have any questions or feedback, feel free to contact [Aurelio Nogueira](mailto:aurelionog@gmail.com).
