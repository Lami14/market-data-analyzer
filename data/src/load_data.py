import pandas as pd

def load_market_data(filepath):
    """
    Load market data from a CSV file.
    """

    data = pd.read_csv(filepath)

    # Convert date column to datetime
    data["date"] = pd.to_datetime(data["date"])

    return data
