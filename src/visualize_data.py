    import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf


def plot_price_trend(data):
    """
    Plot closing price trend over time.
    """

    date_col = "date" if "date" in data.columns else "Date"
    close_col = "close" if "close" in data.columns else "Close"

    plt.figure(figsize=(10, 5))

    sns.lineplot(x=data[date_col], y=data[close_col])

    plt.title("Closing Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


def plot_volume(data):
    """
    Plot daily trading volume.
    """

    date_col = "date" if "date" in data.columns else "Date"
    volume_col = "volume" if "volume" in data.columns else "Volume"

    plt.figure(figsize=(10, 5))

    sns.barplot(x=data[date_col], y=data[volume_col])

    plt.title("Daily Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


def plot_moving_averages(data):
    """
    Plot closing price with moving averages.
    """

    date_col = "date" if "date" in data.columns else "Date"
    close_col = "close" if "close" in data.columns else "Close"

    plt.figure(figsize=(12, 6))

    plt.plot(data[date_col], data[close_col], label="Close Price")

    if "MA_7" in data.columns:
        plt.plot(data[date_col], data["MA_7"], label="7-Day MA")

    if "MA_30" in data.columns:
        plt.plot(data[date_col], data["MA_30"], label="30-Day MA")

    plt.title("Price Trend with Moving Averages")

    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.xticks(rotation=45)

    plt.legend()

    plt.tight_layout()

    plt.show()


def plot_candlestick(data):
    """
    Plot candlestick chart with volume and moving averages.
    """

    if "date" in data.columns:
        data = data.rename(
            columns={
                "date": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume",
            }
        )

    data = data.set_index("Date")

    mpf.plot(
        data,
        type="candle",
        volume=True,
        style="yahoo",
        mav=(7, 30),
        title="Candlestick Chart with Moving Averages",
    )


def plot_correlation_heatmap(price_data):
    """
    Plot correlation heatmap between multiple stocks.
    """

    correlation = price_data.corr()

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Stock Correlation Heatmap")

    plt.tight_layout()

    plt.show()
