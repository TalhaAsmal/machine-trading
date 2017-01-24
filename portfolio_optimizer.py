import scipy.optimize as spo
import pandas as pd
from common import data_dir, get_daily_returns, get_sharpe_ratio
from os import path
import datetime
import numpy as np


def f(allocations, prices):
    normed = prices / prices.ix[0]
    alloced = normed * allocations
    pos_vals = alloced
    port_val = pos_vals.sum(axis=1)
    daily_returns = get_daily_returns(port_val)[1:]

    sharpe_ratio = get_sharpe_ratio(daily_returns)
    print("Sharpe ratio: {}".format(sharpe_ratio))

    return -sharpe_ratio


def alloc_constraint(allocs):
    return 1.0 - np.sum(allocs)


def portfolio_optimizer():
    start_date = datetime.date(2016, 1, 1)
    end_date = datetime.date(2016, 12, 31)
    symbols = ["SPY", "YHOO", "MSFT", "IBM", "GLD", "XOM"]
    prices = pd.read_csv(path.join(data_dir, "combined.csv"), index_col='Date', parse_dates=True, na_values=['nan'])
    prices = prices.ix[start_date:end_date, symbols]

    print("Optimizing...")
    init_allocs = np.ones(len(symbols), dtype=np.float32) / len(symbols)
    bounds = [(0, 1) for a in symbols]
    constraints = {'type': 'eq', 'fun': alloc_constraint}
    result = spo.minimize(f, init_allocs, args=(prices,), method='SLSQP', bounds=bounds, constraints=constraints)

    print("Final allocations: {}\nFinal sharpe value: {}".format(result.x, -f(result.x, prices)))
    print("SUM of allocations: {}".format(np.sum(result.x)))

portfolio_optimizer()