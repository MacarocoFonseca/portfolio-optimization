from datetime import datetime as date

from commons.dca_client import DollarCostAveragingInvestment
from commons.lump_sum_client import LumpSumInvestment

if __name__ == "__main__":
    # Usage
    ticker = "^GSPC"
    start_date = "2012-01-01"
    end_date = date.today()
    initial_investment = 10_000
    dca_investment_periods = 12.0

    lump_sum = LumpSumInvestment(ticker, start_date, end_date, initial_investment)
    lump_sum_returns = lump_sum.calculate_returns()

    dca = DollarCostAveragingInvestment(
        ticker, start_date, end_date, initial_investment, dca_investment_periods
    )
    dca_returns = dca.investment_generator()

    print("----- Lump Sum Investments -----")
    print(
        f"Lump Sum day to invest an amount of {initial_investment} lump sum was on {lump_sum_returns.idxmax().strftime('%b %d %Y')} and would be worth ${round(lump_sum_returns.max(),2)}"
    )
    print(
        f"Lump Sum day to invest an amount of {initial_investment} lump sum was on {lump_sum_returns.idxmin().strftime('%b %d %Y')} and would be worth ${round(lump_sum_returns.min(),2)}"
    )
    print("-" * 100)
    print("-" * 100)
    print("----- Dollar Cost Investments -----")
    print(
        f"DCA day to invest an amount of {initial_investment} DCA was on {dca_returns.idxmax().strftime('%b %d %Y')} and would be worth ${round(dca_returns.max(),2)}"
    )
    print(
        f"DCA day to invest an amount of {initial_investment} DCA was on {dca_returns.idxmin().strftime('%b %d %Y')} and would be worth ${round(dca_returns.min(),2)}"
    )
