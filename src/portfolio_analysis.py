import pandas as pd


def fetch_multiple_stocks(fetch_function, symbols):
    """
    Fetch data for multiple stocks and combine closing prices.
    """

    price_data = pd.DataFrame()

    for symbol in symbols:
        data = fetch_function(symbol)

        price_data[symbol] = data["Close"]

    return price_data


def calculate_portfolio_returns(price_data):
    """
    Calculate daily returns for multiple stocks.
    """

    returns = price_data.pct_change()

    return returns


def simulate_equal_portfolio(returns):
    """
    Simulate equal-weight portfolio performance.
    """

    weights = [1 / len(returns.columns)] * len(returns.columns)

    portfolio_return = (returns * weights).sum(axis=1)

    cumulative_return = (1 + portfolio_return).cumprod()

    return cumulative_return
