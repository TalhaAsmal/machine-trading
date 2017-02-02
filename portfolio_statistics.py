import datetime
from os import path
import pandas as pd
from common import data_dir, get_daily_returns, get_sharpe_ratio

start_val = 1000000
start_date = datetime.date(2009, 1, 1)
end_date = datetime.date(2011, 12, 31)
symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
allocation = [0.4, 0.4, 0.1, 0.1]

def get_portfolio_value(start_val, start_date, end_date, symbols, allocations):
    prices = pd.read_csv(path.join(data_dir, "combined.csv"), index_col='Date', parse_dates=True, na_values=['nan'])
    prices = prices.ix[start_date:end_date, symbols]

    normed = prices / prices.ix[0]
    alloced = normed * allocations
    pos_vals = alloced * start_val
    port_val = pos_vals.sum(axis=1)

    return port_val


def get_portfolio_stats(port_val):
    daily_rets = get_daily_returns(port_val)[1:]
    cum_ret = (port_val.iloc[-1] / port_val.iloc[0]) - 1
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = get_sharpe_ratio(daily_rets, risk_free_rate=0)

    print("Cumulative Returns: {}\nAverage Daily Returns: {}\nStd Deviation of daily returns: {}\nSharpe Ratio: {}".format(cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio))



if __name__ == "__main__":
    port_val = get_portfolio_value(start_val, start_date, end_date, symbols, allocation)
    get_portfolio_stats(port_val)
