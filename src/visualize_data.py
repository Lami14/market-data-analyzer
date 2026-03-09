import matplotlib.pyplot as plt
import seaborn as sns


def plot_price_trend(data):
    """
    Plot closing price trend over time.
    """

    plt.figure(figsize=(10,5))

    sns.lineplot(x="date", y="close", data=data)

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

    plt.figure(figsize=(10,5))

    sns.barplot(x="date", y="volume", data=data)

    plt.title("Trading Volume by Day")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()
