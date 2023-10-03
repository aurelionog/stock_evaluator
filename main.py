from main_code import analyze_stocks_from_csv



CSV_PATH = '/Users/aurelionog/Documents/GitHub/langchain_postgres/stock_prices.csv'

# Main function
def main(csv_file_path):
    stop_loss_percent = 10  # Set your desired stop-loss percentage
    profit_target_percent = 15  # Set your desired profit target percentage
    analysis_df = analyze_stocks_from_csv(csv_file_path, stop_loss_percent, profit_target_percent)
    print(analysis_df)

if __name__ == "__main__":
    main()