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
    plot_correlation_heatmap,
)

from portfolio_analysis import (
    fetch_multiple_stocks,
    calculate_portfolio_returns,
    simulate_equal_portfolio,
)


def main():

    symbol = "AAPL"

    print(f"\nFetching data for {symbol}...\n")

    data = fetch_stock_data(symbol)

    stats = calculate_statistics(data)

    print("Market Statistics")
    print("------------------")

    for key, value in stats.items():
        print(f"{key}: {value}")

    data = calculate_daily_returns(data)

    data = calculate_moving_averages(data)

    volatility = calculate_volatility(data)

    print("\nMarket Volatility:", volatility)

    plot_price_trend(data)
    plot_volume(data)
    plot_moving_averages(data)
    plot_candlestick(data)

    # -------- Multi-stock analysis --------

    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

    print("\nFetching multiple stocks:", symbols)

    price_data = fetch_multiple_stocks(fetch_stock_data, symbols)

    returns = calculate_portfolio_returns(price_data)

    portfolio = simulate_equal_portfolio(returns)

    plot_correlation_heatmap(price_data)

    print("\nPortfolio simulation completed")


if __name__ == "__main__":
    main()
