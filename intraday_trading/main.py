from intraday_trading.intraday_trading_app import fetch_historical_data, calculate_technical_indicators, evaluate_buy_signal, calculate_stop_loss_price, calculate_max_reward_price, fetch_intraday_data, calculate_target_percent, calculate_intraday_target_price

if __name__ == "__main__":
    stock_symbol = "GOOG"  # Replace with the stock symbol you want to evaluate
    risk_percent = 2  # Define the risk percentage

    # Fetch historical data
    stock_data = fetch_historical_data(stock_symbol, period="1y")

    if stock_data.empty:
        print(f"No data available for {stock_symbol}. Cannot evaluate.")
    else:
        # Calculate technical indicators
        stock_data = calculate_technical_indicators(stock_data)

        # Evaluate buy signal
        buy_signal, buy_price = evaluate_buy_signal(stock_data)

        if buy_signal == "buy":
            buy_price = stock_data['Close'].iloc[-1]
            stop_loss_price = calculate_stop_loss_price(
                buy_price, risk_percent)
            max_reward_price = calculate_max_reward_price(buy_price, risk_percent)

            print(f"Buy Signal: Yes")
            print(f"Buy Price: ${buy_price:.2f}")
            print(f"Stop Loss Price: ${stop_loss_price:.2f}")
            print(f"Max Reward Price: ${max_reward_price:.2f}")
        elif buy_signal == "buy_dip":
            print(f"Buy Signal: Buy the Dip")
            print(f"Suggested Buy Price: ${buy_price:.2f}")
        else:
            print(f"Buy Signal: No")

    # Fetch intraday data for the specified stock symbol and number of days back
    intraday_data = fetch_intraday_data(stock_symbol, days_back=7)

    if intraday_data.empty:
        print(
            f"No intraday data available for {stock_symbol}. Cannot calculate target percent and target price.")
    else:
        # Calculate the potential target percent for the day
        target_percent = calculate_target_percent(intraday_data)

        # Calculate the intraday target price
        intraday_target_price = calculate_intraday_target_price(
            intraday_data, target_percent)

        # Display the potential target percent and intraday target price
        print(
            f"Automatically Calculated Target Percent: {target_percent:.2f}%")
        print(f"Intraday Target Price: ${intraday_target_price:.2f}")
