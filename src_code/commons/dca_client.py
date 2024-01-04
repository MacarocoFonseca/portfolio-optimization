from datetime import datetime as date
from operator import index

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from commons.ticker_data_collection import YahooTickerDataCollection


class DollarCostAveragingInvestment(YahooTickerDataCollection):
    """
    Args:
        YahooTickerDataCollection (class): retrives correspondent ticker data from yahoo finance
    """

    def __init__(
        self, ticker, start_date, end_date, initial_investment, dca_investment_periods
    ):
        super().__init__(ticker=ticker, start_date=start_date, end_date=end_date)
        self.initial_investment = initial_investment
        self.dca_investment_periods = dca_investment_periods

    def _calculate_returns(self, date):
        # Calculate the portion or amount that I plan to invest for each investment date period
        investment_portion = self.initial_investment / self.dca_investment_periods

        # Get the dates of the investment periods
        all_investment_dates = pd.date_range(
            date, periods=self.dca_investment_periods, freq="30D"
        )

        # Get the dates up to the last date in our data set
        investment_dates = all_investment_dates[
            all_investment_dates < self.data.index[-1]
        ]

        # Get the indecies (and in turn the dates) within the data set that are the closest to the investment date
        closest_investment_date = self.data.index.searchsorted(investment_dates)

        # Get a list of stock prices at the closest investment date
        asset_prices = self.data["Adj Close"].iloc[closest_investment_date]

        # Get the total number of shares that I invested in by summing all of the shares purchased on each of the investment dates
        total_shares_invested = sum(investment_portion / asset_prices)

        # Get the cahs that was not invested from the initial investment amount
        uninvested_cash = investment_portion * sum(
            all_investment_dates >= self.data.index[-1]
        )

        # Calculate the total
        return uninvested_cash + self.data["Adj Close"].iloc[-1] * total_shares_invested

    def investment_generator(self):
        dca_list = []
        for date in self.data.index:
            dca_list.append(self._calculate_returns(date))
        # Convert list to a series
        df_dca = pd.DataFrame()
        df_dca["DCA"] = dca_list
        df_dca = df_dca.set_index(pd.DatetimeIndex(self.data.index))
        df_dca = df_dca.squeeze()
        return df_dca

    def calculate_returns_alternative(self):
        dca_investment = pd.Series(index=self.data.index, dtype="float64").fillna(0)
        for month_end in dca_investment.asfreq("M").index:
            dca_investment[month_end] = self.monthly_investment
        dca_investment = dca_investment.cumsum()
        return (dca_investment / self.data).cumsum() * self.data
