"""
visualize_data.py
-----------------
Generates professional financial charts from stock market data.

Charts:
    - Price trend with moving averages
    - Trading volume bar chart
    - Candlestick OHLC chart
    - Multi-stock correlation heatmap
    - Daily returns distribution
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import mplfinance as mpf
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Style ─────────────────────────────────────────────────────
plt.style.use("seaborn-v0_8-darkgrid")
COLOUR_CLOSE   = "#6366f1"
COLOUR_MA7     = "#f59e0b"
COLOUR_MA30    = "#10b981"
COLOUR_VOLUME  = "#94a3b8"
COLOUR_RETURNS = "#dc2626"

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save_or_show(filename: str, save: bool = True) -> None:
    """Save figure to outputs/ or display it interactively."""
    if save:
        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150, bbox_inches="tight")
        logger.info(f"Chart saved: {path}")
    else:
        plt.show()
    plt.close()


def plot_price_trend(df: pd.DataFrame, ticker: str = "Stock", save: bool = True) -> None:
    """
    Plot closing price over time with 7-day and 30-day moving averages.

    Args:
        df:     DataFrame with 'Close', 'MA_7', 'MA_30' columns.
        ticker: Stock symbol for chart title.
        save:   Save to outputs/ if True, else display interactively.

    Example:
        >>> plot_price_trend(df, ticker="AAPL")
    """
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(df.index, df["Close"], label="Close Price",
            color=COLOUR_CLOSE, linewidth=1.8, zorder=3)

    if "MA_7" in df.columns:
        ax.plot(df.index, df["MA_7"], label="7-Day MA",
                color=COLOUR_MA7, linewidth=1.2, linestyle="--", alpha=0.85)

    if "MA_30" in df.columns:
        ax.plot(df.index, df["MA_30"], label="30-Day MA",
                color=COLOUR_MA30, linewidth=1.2, linestyle="--", alpha=0.85)

    ax.set_title(f"{ticker} — Price Trend with Moving Averages", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    ax.legend(loc="upper left")
    plt.tight_layout()

    _save_or_show(f"{ticker}_price_trend.png", save)


def plot_volume(df: pd.DataFrame, ticker: str = "Stock", save: bool = True) -> None:
    """
    Plot daily trading volume as a bar chart.

    Args:
        df:     DataFrame with 'Volume' column.
        ticker: Stock symbol for chart title.
        save:   Save to outputs/ if True, else display interactively.
    """
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.bar(df.index, df["Volume"] / 1_000_000,
           color=COLOUR_VOLUME, alpha=0.75, width=1.5)

    ax.set_title(f"{ticker} — Daily Trading Volume", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume (Millions)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()

    _save_or_show(f"{ticker}_volume.png", save)


def plot_candlestick(df: pd.DataFrame, ticker: str = "Stock", save: bool = True) -> None:
    """
    Plot an OHLC candlestick chart using mplfinance.

    Args:
        df:     DataFrame with Open, High, Low, Close, Volume columns
                and a DatetimeIndex. Uses the last 60 rows for clarity.
        ticker: Stock symbol for chart title.
        save:   Save to outputs/ if True, else display interactively.
    """
    plot_df = df[["Open", "High", "Low", "Close", "Volume"]].tail(60).copy()
    plot_df.index = pd.DatetimeIndex(plot_df.index)

    save_path = os.path.join(OUTPUT_DIR, f"{ticker}_candlestick.png") if save else None

    mpf.plot(
        plot_df,
        type="candle",
        style="yahoo",
        title=f"{ticker} — Candlestick Chart (Last 60 Days)",
        ylabel="Price (USD)",
        volume=True,
        savefig=save_path,
        figsize=(12, 6)
    )

    if save:
        logger.info(f"Chart saved: {save_path}")
    else:
        plt.show()


def plot_returns_distribution(df: pd.DataFrame, ticker: str = "Stock", save: bool = True) -> None:
    """
    Plot the distribution of daily returns as a histogram with KDE.

    Args:
        df:     DataFrame with 'daily_return' column.
        ticker: Stock symbol for chart title.
        save:   Save to outputs/ if True, else display interactively.
    """
    if "daily_return" not in df.columns:
        logger.warning("No 'daily_return' column found. Skipping returns chart.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    returns = df["daily_return"].dropna()

    ax.hist(returns, bins=40, color=COLOUR_RETURNS, alpha=0.6,
            edgecolor="white", density=True, label="Daily Returns")

    returns.plot.kde(ax=ax, color=COLOUR_RETURNS, linewidth=2)

    ax.axvline(returns.mean(), color="#1e293b", linestyle="--",
               linewidth=1.5, label=f"Mean: {returns.mean():.2f}%")

    ax.set_title(f"{ticker} — Daily Returns Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Daily Return (%)")
    ax.set_ylabel("Density")
    ax.legend()
    plt.tight_layout()

    _save_or_show(f"{ticker}_returns_distribution.png", save)


def plot_correlation_heatmap(stocks: dict[str, pd.DataFrame], save: bool = True) -> None:
    """
    Plot a Pearson correlation heatmap of daily returns across multiple stocks.

    Args:
        stocks: Dictionary of {ticker: DataFrame} with 'Close' column.
        save:   Save to outputs/ if True, else display interactively.

    Example:
        >>> plot_correlation_heatmap({"AAPL": df1, "MSFT": df2})
    """
    if len(stocks) < 2:
        logger.warning("Need at least 2 stocks for a correlation heatmap.")
        return

    # Build a combined returns DataFrame
    returns_df = pd.DataFrame({
        ticker: df["Close"].pct_change()
        for ticker, df in stocks.items()
    }).dropna()

    corr_matrix = returns_df.corr()

    fig, ax = plt.subplots(figsize=(max(6, len(stocks)), max(5, len(stocks) - 1)))

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1, vmax=1,
        linewidths=0.5,
        ax=ax,
        annot_kws={"size": 11}
    )

    ax.set_title("Stock Returns Correlation Heatmap", fontsize=14, fontweight="bold")
    plt.tight_layout()

    _save_or_show("correlation_heatmap.png", save)


if __name__ == "__main__":
    from load_data import load_csv_data
    from analyze_data import calculate_daily_returns, calculate_moving_averages

    df = load_csv_data("data/sample_stock_data.csv")
    df = calculate_daily_returns(df)
    df = calculate_moving_averages(df)

    plot_price_trend(df, ticker="SAMPLE")
    plot_volume(df, ticker="SAMPLE")
    plot_returns_distribution(df, ticker="SAMPLE")
    print("Charts saved to outputs/")
      
