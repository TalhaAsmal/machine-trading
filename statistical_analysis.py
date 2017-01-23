import matplotlib.pyplot as plt
import pandas as pd
from os import path
import datetime
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


def daily_returns(df):
    dr = get_daily_returns(df)
    plot_data(dr, "Daily returns", "Date", "Returns (%)")


def stat_analysis(start_date, end_date, stocks=None):
    df = pd.read_csv(path.join(data_dir, "combined.csv"), index_col='Date', parse_dates=True, na_values=['nan'])
    df = df.ix[start_date:end_date]
    if stocks is not None:
        df = df.ix[:, stocks]

    daily_returns(df)



start = datetime.date(2016, 1, 1)
end = datetime.date.today()
stat_analysis(start, end, ["SPY", "GLD"])
