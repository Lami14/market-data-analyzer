"""
analyze_data.py
---------------
Performs statistical and financial analysis on stock price data.

Includes:
- Summary statistics (price, volume)
- Daily return calculations
- Moving averages (7-day, 30-day)
- Annualised volatility
- Sharpe ratio (risk-adjusted return)
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

TRADING_DAYS_PER_YEAR = 252


def get_market_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate key summary statistics from a stock DataFrame.

    Args:
        df: DataFrame with at least 'Close' and 'Volume' columns.

    Returns:
        Dictionary with average/max/min close price and average volume.

    Example:
        >>> stats = get_market_statistics(df)
        >>> print(stats["average_close_price"])
    """
    if df.empty or "Close" not in df.columns:
        logger.error("DataFrame is empty or missing 'Close' column.")
        return {}

    return {
        "average_close_price": round(df["Close"].mean(), 2),
        "max_close_price":     round(df["Close"].max(), 2),
        "min_close_price":     round(df["Close"].min(), 2),
        "average_volume":      int(df["Volume"].mean()) if "Volume" in df.columns else None,
        "total_trading_days":  len(df),
        "date_range":          f"{df.index.min().date()} → {df.index.max().date()}"
    }


def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns from closing prices.

    Formula: return_t = (Close_t - Close_{t-1}) / Close_{t-1} * 100

    Args:
        df: DataFrame with a 'Close' column.

    Returns:
        Original DataFrame with a new 'daily_return' column (in %).
        First row will be NaN (no prior day to compare).

    Example:
        >>> df = calculate_daily_returns(df)
        >>> print(df["daily_return"].describe())
    """
    df = df.copy()
    df["daily_return"] = df["Close"].pct_change() * 100
    logger.info("Daily returns calculated.")
    return df


def calculate_moving_averages(df: pd.DataFrame, windows: list[int] = [7, 30]) -> pd.DataFrame:
    """
    Add moving average columns to the DataFrame.

    Args:
        df:      DataFrame with a 'Close' column.
        windows: List of window sizes in trading days. Default: [7, 30].

    Returns:
        DataFrame with new columns 'MA_7', 'MA_30', etc.

    Example:
        >>> df = calculate_moving_averages(df, windows=[7, 30, 50])
        >>> print(df[["Close", "MA_7", "MA_30"]].tail())
    """
    df = df.copy()
    for window in windows:
        col_name = f"MA_{window}"
        df[col_name] = df["Close"].rolling(window=window, min_periods=1).mean().round(2)
        logger.info(f"Moving average added: {col_name}")
    return df


def calculate_volatility(df: pd.DataFrame) -> float:
    """
    Calculate annualised volatility of a stock's daily returns.

    Volatility = std(daily_returns) * sqrt(252)

    A higher value means more price uncertainty/risk.
    Typical range: 0.10 (low risk) to 0.60+ (high risk).

    Args:
        df: DataFrame with a 'Close' column.

    Returns:
        Annualised volatility as a decimal (e.g. 0.33 = 33%).

    Example:
        >>> vol = calculate_volatility(df)
        >>> print(f"Annualised Volatility: {vol:.2%}")
    """
    if "daily_return" not in df.columns:
        df = calculate_daily_returns(df)

    daily_std = df["daily_return"].dropna().std() / 100  # Convert % back to decimal
    annualised = round(daily_std * np.sqrt(TRADING_DAYS_PER_YEAR), 4)
    logger.info(f"Annualised volatility: {annualised:.2%}")
    return annualised


def calculate_sharpe_ratio(df: pd.DataFrame, risk_free_rate: float = 0.05) -> float:
    """
    Calculate the annualised Sharpe Ratio for a stock.

    Sharpe Ratio = (Mean Annual Return - Risk-Free Rate) / Annual Volatility

    A ratio > 1.0 is generally considered good.
    A ratio > 2.0 is considered very good.

    Args:
        df:              DataFrame with a 'Close' column.
        risk_free_rate:  Annual risk-free rate (default: 5% = 0.05).

    Returns:
        Sharpe ratio as a float. Higher is better.

    Example:
        >>> sharpe = calculate_sharpe_ratio(df)
        >>> print(f"Sharpe Ratio: {sharpe:.2f}")
    """
    if "daily_return" not in df.columns:
        df = calculate_daily_returns(df)

    returns = df["daily_return"].dropna() / 100
    mean_annual_return = returns.mean() * TRADING_DAYS_PER_YEAR
    annual_volatility  = returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)

    if annual_volatility == 0:
        return 0.0

    sharpe = round((mean_annual_return - risk_free_rate) / annual_volatility, 4)
    logger.info(f"Sharpe Ratio: {sharpe:.2f}")
    return sharpe


def print_statistics(stats: dict, volatility: float, sharpe: float) -> None:
    """
    Print a formatted summary of market statistics to the console.

    Args:
        stats:      Dictionary from get_market_statistics().
        volatility: Annualised volatility from calculate_volatility().
        sharpe:     Sharpe ratio from calculate_sharpe_ratio().
    """
    print("\nMarket Statistics")
    print("-" * 35)
    for key, value in stats.items():
        label = key.replace("_", " ").title()
        print(f"  {label:<28}: {value:,}" if isinstance(value, int) else f"  {label:<28}: {value}")

    print("\nMarket Volatility")
    print("-" * 35)
    print(f"  Annualised Volatility       : {volatility:.2%}")

    print("\nRisk-Adjusted Return")
    print("-" * 35)
    print(f"  Sharpe Ratio                : {sharpe:.2f}")
    rating = "Excellent" if sharpe > 2 else "Good" if sharpe > 1 else "Below average"
    print(f"  Rating                      : {rating}")


if __name__ == "__main__":
    from load_data import load_csv_data
    df = load_csv_data("data/sample_stock_data.csv")
    df = calculate_daily_returns(df)
    df = calculate_moving_averages(df)
    stats = get_market_statistics(df)
    vol   = calculate_volatility(df)
    sharpe = calculate_sharpe_ratio(df)
    print_statistics(stats, vol, sharpe)
  
