"""
portfolio_analysis.py
---------------------
Simulates an equal-weight multi-stock portfolio and calculates
key performance metrics.

Metrics:
    - Total return
    - Annualised return
    - Annualised volatility
    - Sharpe ratio
    - Maximum drawdown
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

TRADING_DAYS_PER_YEAR = 252
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def simulate_portfolio(
    stocks: dict[str, pd.DataFrame],
    initial_investment: float = 10_000.0,
    risk_free_rate: float = 0.05
) -> dict:
    """
    Simulate an equal-weight portfolio across multiple stocks.

    Each stock receives an equal allocation of the initial investment.
    Returns are calculated from daily closing prices.

    Args:
        stocks:             Dictionary of {ticker: DataFrame} with 'Close' column.
        initial_investment: Starting capital in USD. Default: $10,000.
        risk_free_rate:     Annual risk-free rate for Sharpe calculation. Default: 5%.

    Returns:
        Dictionary with keys:
            - tickers:            List of stock symbols
            - initial_investment: Starting capital
            - final_value:        Portfolio value at end of period
            - total_return_pct:   Percentage gain/loss
            - annualised_return:  CAGR-style annual return
            - volatility:         Annualised portfolio volatility
            - sharpe_ratio:       Risk-adjusted return metric
            - max_drawdown:       Worst peak-to-trough decline
            - portfolio_values:   Time-series of portfolio value (pd.Series)

    Example:
        >>> results = simulate_portfolio({"AAPL": df1, "MSFT": df2}, initial_investment=10000)
        >>> print(f"Final Value: ${results['final_value']:,.2f}")
    """
    if not stocks:
        logger.error("No stocks provided for portfolio simulation.")
        return {}

    # Align all closing prices on common dates
    close_prices = pd.DataFrame({
        ticker: df["Close"] for ticker, df in stocks.items()
    }).dropna()

    if close_prices.empty:
        logger.error("No overlapping dates found across stocks.")
        return {}

    # Equal-weight daily returns
    daily_returns = close_prices.pct_change().dropna()
    portfolio_daily_returns = daily_returns.mean(axis=1)

    # Portfolio value over time
    portfolio_values = (1 + portfolio_daily_returns).cumprod() * initial_investment

    final_value     = round(portfolio_values.iloc[-1], 2)
    total_return    = round((final_value - initial_investment) / initial_investment * 100, 2)
    n_years         = len(daily_returns) / TRADING_DAYS_PER_YEAR

    # Annualised return (CAGR)
    annualised_return = round(
        ((final_value / initial_investment) ** (1 / n_years) - 1) * 100, 2
    ) if n_years > 0 else 0.0

    # Annualised volatility
    volatility = round(
        portfolio_daily_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR) * 100, 2
    )

    # Sharpe ratio
    mean_daily    = portfolio_daily_returns.mean()
    std_daily     = portfolio_daily_returns.std()
    daily_rf_rate = risk_free_rate / TRADING_DAYS_PER_YEAR
    sharpe = round(
        (mean_daily - daily_rf_rate) / std_daily * np.sqrt(TRADING_DAYS_PER_YEAR), 2
    ) if std_daily != 0 else 0.0

    # Maximum drawdown
    rolling_max  = portfolio_values.cummax()
    drawdown     = (portfolio_values - rolling_max) / rolling_max
    max_drawdown = round(drawdown.min() * 100, 2)

    results = {
        "tickers":            list(stocks.keys()),
        "initial_investment": initial_investment,
        "final_value":        final_value,
        "total_return_pct":   total_return,
        "annualised_return":  annualised_return,
        "volatility":         volatility,
        "sharpe_ratio":       sharpe,
        "max_drawdown":       max_drawdown,
        "portfolio_values":   portfolio_values,
    }

    logger.info("Portfolio simulation completed.")
    return results


def plot_portfolio(results: dict, save: bool = True) -> None:
    """
    Plot portfolio value growth over time.

    Args:
        results: Output dictionary from simulate_portfolio().
        save:    Save to outputs/ if True, else display interactively.
    """
    if "portfolio_values" not in results:
        logger.warning("No portfolio values to plot.")
        return

    values = results["portfolio_values"]
    tickers = ", ".join(results["tickers"])

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(values.index, values, color="#6366f1", linewidth=2, label="Portfolio Value")
    ax.axhline(results["initial_investment"], color="#94a3b8",
               linestyle="--", linewidth=1.2, label="Initial Investment")
    ax.fill_between(values.index, results["initial_investment"], values,
                    where=(values >= results["initial_investment"]),
                    alpha=0.1, color="#16a34a")
    ax.fill_between(values.index, results["initial_investment"], values,
                    where=(values < results["initial_investment"]),
                    alpha=0.1, color="#dc2626")

    ax.set_title(f"Portfolio Simulation — {tickers}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value (USD)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    ax.legend()
    plt.tight_layout()

    if save:
        path = os.path.join(OUTPUT_DIR, "portfolio_simulation.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        logger.info(f"Chart saved: {path}")
    else:
        plt.show()
    plt.close()


def print_portfolio_results(results: dict) -> None:
    """
    Print a formatted summary of portfolio simulation results.

    Args:
        results: Output dictionary from simulate_portfolio().
    """
    sign = "+" if results["total_return_pct"] >= 0 else ""

    print("\nPortfolio Simulation")
    print("-" * 40)
    print(f"  Stocks               : {', '.join(results['tickers'])}")
    print(f"  Initial Investment   : ${results['initial_investment']:,.2f}")
    print(f"  Final Value          : ${results['final_value']:,.2f}")
    print(f"  Total Return         : {sign}{results['total_return_pct']:.2f}%")
    print(f"  Annualised Return    : {sign}{results['annualised_return']:.2f}%")
    print(f"  Annualised Volatility: {results['volatility']:.2f}%")
    print(f"  Sharpe Ratio         : {results['sharpe_ratio']:.2f}")
    print(f"  Max Drawdown         : {results['max_drawdown']:.2f}%")
    print("-" * 40)
    print("  Portfolio simulation completed ✅")


if __name__ == "__main__":
    from fetch_data import fetch_multiple_stocks
    stocks = fetch_multiple_stocks(["AAPL", "MSFT", "GOOGL"], period="1y")
    results = simulate_portfolio(stocks, initial_investment=10_000)
    print_portfolio_results(results)
    plot_portfolio(results)
  
