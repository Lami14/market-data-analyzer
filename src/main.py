"""
main.py
-------
Command-line entry point for the Market Data Analyzer.

Usage:
    # Analyse a single live stock
    python src/main.py --ticker AAPL --period 6mo

    # Load from a CSV file
    python src/main.py --file data/sample_stock_data.csv

    # Analyse multiple stocks + correlation heatmap
    python src/main.py --tickers AAPL MSFT GOOGL --period 1y

    # Run a portfolio simulation
    python src/main.py --portfolio AAPL MSFT TSLA --investment 10000
"""

import argparse
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_args():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="📈 Market Data Analyzer — financial analysis & visualisation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --ticker AAPL --period 6mo
  python src/main.py --file data/sample_stock_data.csv
  python src/main.py --tickers AAPL MSFT GOOGL --period 1y
  python src/main.py --portfolio AAPL MSFT TSLA --investment 10000
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticker",    type=str,          help="Single stock ticker (e.g. AAPL)")
    group.add_argument("--tickers",   type=str, nargs="+", help="Multiple tickers (e.g. AAPL MSFT)")
    group.add_argument("--file",      type=str,          help="Path to local CSV file")
    group.add_argument("--portfolio", type=str, nargs="+", help="Tickers for portfolio simulation")

    parser.add_argument("--period",     type=str, default="6mo",
                        help="Time period: 1mo 3mo 6mo 1y 2y (default: 6mo)")
    parser.add_argument("--investment", type=float, default=10_000.0,
                        help="Initial portfolio investment in USD (default: 10000)")
    parser.add_argument("--no-save",   action="store_true",
                        help="Display charts interactively instead of saving to outputs/")

    return parser.parse_args()


def run_single_stock(ticker: str, period: str, save: bool) -> None:
    """Full analysis pipeline for a single stock."""
    from fetch_data import fetch_stock_data
    from analyze_data import (calculate_daily_returns, calculate_moving_averages,
                               get_market_statistics, calculate_volatility,
                               calculate_sharpe_ratio, print_statistics)
    from visualize_data import (plot_price_trend, plot_volume,
                                plot_candlestick, plot_returns_distribution)

    df = fetch_stock_data(ticker, period=period)
    if df.empty:
        logger.error(f"No data available for {ticker}. Exiting.")
        sys.exit(1)

    df = calculate_daily_returns(df)
    df = calculate_moving_averages(df)

    stats  = get_market_statistics(df)
    vol    = calculate_volatility(df)
    sharpe = calculate_sharpe_ratio(df)
    print_statistics(stats, vol, sharpe)

    plot_price_trend(df, ticker=ticker, save=save)
    plot_volume(df, ticker=ticker, save=save)
    plot_candlestick(df, ticker=ticker, save=save)
    plot_returns_distribution(df, ticker=ticker, save=save)

    if save:
        print(f"\n✅ Charts saved to outputs/")


def run_multiple_stocks(tickers: list, period: str, save: bool) -> None:
    """Fetch and compare multiple stocks with a correlation heatmap."""
    from fetch_data import fetch_multiple_stocks
    from analyze_data import (calculate_daily_returns, calculate_moving_averages,
                               get_market_statistics, calculate_volatility,
                               calculate_sharpe_ratio, print_statistics)
    from visualize_data import plot_price_trend, plot_correlation_heatmap

    stocks = fetch_multiple_stocks(tickers, period=period)

    if not stocks:
        logger.error("Could not fetch data for any of the provided tickers.")
        sys.exit(1)

    for ticker, df in stocks.items():
        df = calculate_daily_returns(df)
        df = calculate_moving_averages(df)
        stocks[ticker] = df

        print(f"\n{'='*40}")
        print(f"  {ticker}")
        print(f"{'='*40}")
        stats  = get_market_statistics(df)
        vol    = calculate_volatility(df)
        sharpe = calculate_sharpe_ratio(df)
        print_statistics(stats, vol, sharpe)
        plot_price_trend(df, ticker=ticker, save=save)

    plot_correlation_heatmap(stocks, save=save)

    if save:
        print(f"\n✅ Charts saved to outputs/")


def run_from_csv(filepath: str, save: bool) -> None:
    """Load data from a CSV file and run the full analysis."""
    from load_data import load_csv_data, summarise_dataframe
    from analyze_data import (calculate_daily_returns, calculate_moving_averages,
                               get_market_statistics, calculate_volatility,
                               calculate_sharpe_ratio, print_statistics)
    from visualize_data import (plot_price_trend, plot_volume, plot_returns_distribution)

    df = load_csv_data(filepath)
    summarise_dataframe(df)

    df = calculate_daily_returns(df)
    df = calculate_moving_averages(df)

    stats  = get_market_statistics(df)
    vol    = calculate_volatility(df)
    sharpe = calculate_sharpe_ratio(df)
    print_statistics(stats, vol, sharpe)

    plot_price_trend(df, ticker="CSV_DATA", save=save)
    plot_volume(df, ticker="CSV_DATA", save=save)
    plot_returns_distribution(df, ticker="CSV_DATA", save=save)

    if save:
        print(f"\n✅ Charts saved to outputs/")


def run_portfolio(tickers: list, period: str, investment: float, save: bool) -> None:
    """Run a portfolio simulation across multiple stocks."""
    from fetch_data import fetch_multiple_stocks
    from portfolio_analysis import simulate_portfolio, print_portfolio_results, plot_portfolio

    stocks = fetch_multiple_stocks(tickers, period=period)

    if not stocks:
        logger.error("Could not fetch data for portfolio simulation.")
        sys.exit(1)

    results = simulate_portfolio(stocks, initial_investment=investment)
    print_portfolio_results(results)
    plot_portfolio(results, save=save)

    if save:
        print(f"\n✅ Portfolio chart saved to outputs/")


def main():
    args = parse_args()
    save = not args.no_save

    print("\n📈 Market Data Analyzer")
    print("=" * 40)

    if args.ticker:
        run_single_stock(args.ticker, args.period, save)

    elif args.tickers:
        run_multiple_stocks(args.tickers, args.period, save)

    elif args.file:
        run_from_csv(args.file, save)

    elif args.portfolio:
        run_portfolio(args.portfolio, args.period, args.investment, save)


if __name__ == "__main__":
    main()
  
