from datetime import datetime as date
from operator import index

from commons.ticker_data_collection import YahooTickerDataCollection


class LumpSumInvestment(YahooTickerDataCollection):
    """
    Args:
        YahooTickerDataCollection (class): retrives correspondent ticker data from yahoo finance
    """

    def __init__(self, ticker, start_date, end_date, initial_investment) -> None:
        super().__init__(ticker=ticker, start_date=start_date, end_date=end_date)
        self.lump_sum_amount = initial_investment

    def calculate_returns(self):
        # Get the adjusted close prices from the data set
        adj_close_prices = self.data["Adj Close"]

        # Get the latest prices values of the Stock/ETF within this data set
        asset_latest_value = adj_close_prices[-1]

        # Get the number of shares bought on each date with the hypothetical investment amount (lump sum)
        num_shares_bought = self.lump_sum_amount / adj_close_prices

        # Calculate how much money a person would have according to the last price of this data set for investing a lum sum on a given date in the past
        return asset_latest_value * num_shares_bought
