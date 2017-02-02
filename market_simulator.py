import pandas as pd
from common import data_dir
from portfolio_statistics import get_portfolio_stats
from os import path
import numpy as np


def compute_portvals(orders_file=path.join('orders', 'orders.csv'), start_val=1000000):
    order_types = {'BUY': 1, 'SELL': -1}

    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True)
    prices = pd.read_csv(path.join(data_dir, 'combined.csv'), index_col='Date', parse_dates=True)
    current_cash = start_val

    start_date = orders.index.min()
    end_date = orders.index.max()
    stocks_of_interest = orders.Symbol.unique()
    prices = prices.ix[start_date:end_date, stocks_of_interest]
    owned_shares = pd.DataFrame(data=np.zeros((1, len(stocks_of_interest))), columns=stocks_of_interest)
    port_val = pd.DataFrame(index=prices.index, columns=['port_val'])

    for day in prices.iterrows():
        if day[0] in orders.index:
            daily_orders = orders.ix[[day[0]]]
            for order in daily_orders.itertuples():
                current_cash -= order_types[order.Order] * order.Shares * day[1][order.Symbol]
                owned_shares[order.Symbol] += order_types[order.Order] * order.Shares
        current_port_val = current_cash + (owned_shares * day[1]).sum(axis=1)
        port_val.ix[day[0], 'port_val'] = current_port_val[0]

    return port_val

port_val = compute_portvals()
get_portfolio_stats(port_val.iloc[:, 0])