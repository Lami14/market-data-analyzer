from fetch_data import fetch_stock_data
from analyze_data import (
    calculate_statistics,
    calculate_daily_returns,
    calculate_moving_averages,
    calculate_volatility,
)
from visualize_data import (
    plot_price_trend,
    plot_volume,
    plot_moving_averages,
    plot_candlestick,
)


def main():

    symbol = "AAPL"

    print(f"\nFetching data for {symbol}...\n")

    # Fetch market data
    data = fetch_stock_data(symbol)

    # Calculate statistics
    stats = calculate_statistics(data)

    print("Market Statistics")
    print("------------------")

    for key, value in stats.items():
        print(f"{key}: {value}")

    # Calculate daily returns
    data = calculate_daily_returns(data)

    # Calculate moving averages
    data = calculate_moving_averages(data)

    # Calculate volatility
    volatility = calculate_volatility(data)

    print("\nMarket Volatility")
    print("------------------")
    print(volatility)

    # Generate visualizations
    plot_price_trend(data)
    plot_volume(data)
    plot_moving_averages(data)
    plot_candlestick(data)


if __name__ == "__main__":
    main()
