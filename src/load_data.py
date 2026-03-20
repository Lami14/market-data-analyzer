"""
fetch_data.py
-------------
Fetches historical stock market data from Yahoo Finance
using the yfinance library.

Supports single and multiple ticker symbols with
configurable time periods.
"""

import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Valid period strings accepted by yfinance
VALID_PERIODS = {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"}


def fetch_stock_data(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a single stock ticker.

    Args:
        ticker: Stock symbol (e.g. 'AAPL', 'MSFT', 'GOOGL').
        period: Time period string. One of: 1d, 5d, 1mo, 3mo,
                6mo, 1y, 2y, 5y, 10y, ytd, max. Default: '6mo'.

    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume, ticker.
        Returns empty DataFrame if the fetch fails.

    Example:
        >>> df = fetch_stock_data("AAPL", period="1y")
        >>> print(df.head())
    """
    ticker = ticker.upper().strip()

    if period not in VALID_PERIODS:
        logger.warning(f"Invalid period '{period}'. Defaulting to '6mo'.")
        period = "6mo"

    logger.info(f"Fetching data for {ticker} (period={period})...")

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        if df.empty:
            logger.warning(f"No data returned for ticker '{ticker}'. Check the symbol.")
            return pd.DataFrame()

        # Keep only standard OHLCV columns
        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
        df.index = pd.to_datetime(df.index)
        df.index.name = "Date"
        df["ticker"] = ticker

        logger.info(f"Successfully fetched {len(df)} rows for {ticker}.")
        return df

    except Exception as e:
        logger.error(f"Failed to fetch data for '{ticker}': {e}")
        return pd.DataFrame()


def fetch_multiple_stocks(tickers: list[str], period: str = "6mo") -> dict[str, pd.DataFrame]:
    """
    Fetch historical data for multiple stock tickers.

    Args:
        tickers: List of stock symbols (e.g. ['AAPL', 'MSFT', 'GOOGL']).
        period:  Time period string. Default: '6mo'.

    Returns:
        Dictionary mapping ticker symbol → DataFrame.
        Tickers that fail to fetch are excluded from the result.

    Example:
        >>> stocks = fetch_multiple_stocks(["AAPL", "MSFT"], period="1y")
        >>> for ticker, df in stocks.items():
        ...     print(f"{ticker}: {len(df)} rows")
    """
    results = {}

    for ticker in tickers:
        df = fetch_stock_data(ticker, period=period)
        if not df.empty:
            results[ticker] = df

    logger.info(f"Fetched data for {len(results)}/{len(tickers)} tickers.")
    return results


def get_stock_info(ticker: str) -> dict:
    """
    Fetch basic company information for a ticker.

    Args:
        ticker: Stock symbol.

    Returns:
        Dictionary with company name, sector, market cap, etc.
    """
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info
        return {
            "name":        info.get("longName", "N/A"),
            "sector":      info.get("sector", "N/A"),
            "industry":    info.get("industry", "N/A"),
            "market_cap":  info.get("marketCap", "N/A"),
            "currency":    info.get("currency", "USD"),
            "exchange":    info.get("exchange", "N/A"),
        }
    except Exception as e:
        logger.error(f"Could not fetch info for '{ticker}': {e}")
        return {}


if __name__ == "__main__":
    df = fetch_stock_data("AAPL", period="3mo")
    print(df.tail())
    print(f"\nShape: {df.shape}")
      
