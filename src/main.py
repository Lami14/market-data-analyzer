from load_data import load_market_data
from analyze_data import calculate_statistics, calculate_daily_returns
from visualize_data import plot_price_trend, plot_volume


def main():

    filepath = "../data/sample_stock_data.csv"

    # Load dataset
    data = load_market_data(filepath)

    # Calculate statistics
    stats = calculate_statistics(data)

    print("\nMarket Statistics")
    print("-----------------------")

    for key, value in stats.items():
        print(f"{key}: {value}")

    # Calculate daily returns
    data = calculate_daily_returns(data)

    # Visualizations
    plot_price_trend(data)
    plot_volume(data)


if __name__ == "__main__":
    main()
