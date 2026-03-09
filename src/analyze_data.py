def calculate_statistics(data):
    """
    Calculate basic statistics from the dataset.
    """

    stats = {
        "average_close_price": data["close"].mean(),
        "max_close_price": data["close"].max(),
        "min_close_price": data["close"].min(),
        "average_volume": data["volume"].mean(),
    }

    return stats


def calculate_daily_returns(data):
    """
    Calculate daily percentage returns.
    """

    data["daily_return"] = data["close"].pct_change()

    return data
