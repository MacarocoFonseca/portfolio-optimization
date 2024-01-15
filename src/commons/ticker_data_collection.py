from operator import index

import pandas as pd
import yfinance as yf


class YahooTickerDataCollection:
    def __init__(self, ticker: str, start_date: str, end_date: str):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = pd.DataFrame(
            data=yf.download(
                tickers=self.ticker, start=self.start_date, end=self.end_date
            )
        )
        self.data = self.data.dropna()

    def calculate_returns(self):
        raise NotImplementedError("Subclasses should implement this method")
