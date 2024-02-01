#!/usr/bin/env python3.9
import quantstats as qs
import os

# Directory where the file will be saved
output_dir = "portfolio_experiment/strategies/output"

# Create the directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

qs.extend_pandas()

stock = qs.utils.download_returns("QQQ", period="3y")
qs.plots.drawdowns_periods(stock)
stock.plot_earnings(
    savefig="portfolio_experiment/strategies/output/qqq_earning.png",
    start_balance=10_000,
)

ticker_weights = {"AMZN": 0.5, "META": 0.1}
zukt_portfolio = qs.utils.make_index(ticker_weights)
qs.reports.html(
    zukt_portfolio,
    "qqq",
    output="portfolio_experiment/strategies/output/zukt_portfolio_vs_qqq.html",
)
