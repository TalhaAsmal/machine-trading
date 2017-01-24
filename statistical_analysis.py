import matplotlib.pyplot as plt
import pandas as pd
from os import path
import datetime
import numpy as np
from common import data_dir, get_bollinger_bands, plot_data, get_daily_returns


def bollinger_bands(df):
    ax = df.plot(title="SPY rolling mean", label='SPY')

    rm_spy = df['SPY'].rolling(center=False, window=20).mean()
    rm_spy.plot(label='Rolling Mean', ax=ax)

    rstd_spy = df['SPY'].rolling(center=False, window=20).std()

    upper_band, lower_band = get_bollinger_bands(rm_spy, rstd_spy)
    upper_band.plot(label="Upper band", ax=ax)
    lower_band.plot(label="Lower band", ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    plt.show()


def stat_analysis(start_date, end_date, stocks=None):
    df = pd.read_csv(path.join(data_dir, "combined.csv"), index_col='Date', parse_dates=True, na_values=['nan'])
    df = df.ix[start_date:end_date]
    if stocks is not None:
        df = df.ix[:, stocks]

    daily_returns = get_daily_returns(df)
    beta_XOM, alpha_XOM = create_scatter_plot(daily_returns, "SPY", "XOM")
    beta_GLD, alpha_GLD = create_scatter_plot(daily_returns, "SPY", "GLD")


def create_histograms(df, bins):
    # Get daily returns
    daily_returns = get_daily_returns(df)
    # Plot histogram
    daily_returns.hist(bins=bins)

    # Calculate and plot mean and std. deviation
    mean = daily_returns.SPY.mean()
    std_dev = daily_returns.SPY.std()
    print("Mean: {}\nStd. Dev: {}".format(mean, std_dev))

    plt.axvline(mean, color='w', linestyle='dashed', linewidth=2)
    plt.axvline(std_dev, color='r', linestyle='dashed', linewidth=2)
    plt.axvline(-std_dev, color='r', linestyle='dashed', linewidth=2)

    # Calculate kurtosis
    print("Kurtosis: {}".format(daily_returns.kurtosis()))
    plt.show()


def create_scatter_plot(daily_returns, x_axis, y_axis):
    daily_returns.plot(kind="scatter", x=x_axis, y=y_axis)
    beta, alpha = np.polyfit(daily_returns[x_axis], daily_returns[y_axis], 1)
    plt.plot(daily_returns[x_axis], beta * daily_returns[x_axis] + alpha, '-', color='r')
    plt.show()
    return beta, alpha


start = datetime.date(2009, 1, 1)
end = datetime.date.today()
stat_analysis(start, end, ["SPY", "XOM", "GLD"])
