import yfinance as yf


def fetch_stock_data(symbol, start="2023-01-01", end="2024-01-01"):
    """
    Fetch historical stock data using Yahoo Finance API.
    """

    data = yf.download(symbol, start=start, end=end)

    data.reset_index(inplace=True)

    return data
