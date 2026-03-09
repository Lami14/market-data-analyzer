    def plot_correlation_heatmap(price_data):
    """
    Plot correlation between multiple stocks.
    """

    import seaborn as sns
    import matplotlib.pyplot as plt

    correlation = price_data.corr()

    plt.figure(figsize=(8,6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Stock Correlation Heatmap")

    plt.tight_layout()

    plt.show()
