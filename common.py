import matplotlib.pyplot as plt

data_dir = "data"


def get_bollinger_bands(rm, rstd):
    upper_bound = rm + 2 * rstd
    lower_bound = rm - 2 * rstd
    return upper_bound, lower_bound


def get_daily_returns(df):
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.fillna(0)
    return daily_returns


def plot_data(df, title, xlable, ylable):
    ax = df.plot(title=title, fontsize=12)
    ax.set_ylabel(ylable)
    ax.set_xlabel(xlable)
    plt.show()
