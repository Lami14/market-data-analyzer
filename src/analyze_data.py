import pandas as pd


def calculate_statistics(data):
    """
    Calculate basic statistics from the dataset.
    Works for both CSV sample data (lowercase columns)
    and API data from yfinance (capitalized columns).
    """

    close_col = "close" if "close" in data.columns else "Close"
    volume_col = "volume" if "volume" in data.columns else "Volume"

    stats = {
        "average_close_price": data[close_col].mean(),
        "max_close_price": data[close_col].max(),
        "min_close_price": data[close_col].min(),
        "average_volume": data[volume_col].mean(),
    }

    return stats


def calculate_daily_returns(data):
    """
    Calculate daily percentage return.
    """

    close_col = "close" if "close" in data.columns else "Close"

    data["daily_return"] = data[close_col].pct_change()

    return data


def calculate_moving_averages(data):
    """
    Calculate moving averages for technical analysis.
    """

    close_col = "close" if "close" in data.columns else "Close"

    data["MA_7"] = data[close_col].rolling(window=7).mean()
    data["MA_30"] = data[close_col].rolling(window=30).mean()

    return data


def calculate_volatility(data):
    """
    Calculate market volatility using the
    standard deviation of daily returns.
    """

    close_col = "close" if "close" in data.columns else "Close"

    data["daily_return"] = data[close_col].pct_change()

    volatility = data["daily_return"].std()

    return volatility
