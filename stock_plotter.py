import matplotlib.pyplot as plt
import pandas as pd
from os import path
import datetime

def plot_all(start_date, end_date):
    df = pd.read_csv(path.join("data", "combined.csv"), index_col='Date', parse_dates=True, na_values=['nan'])
    df = df.ix[start_date:end_date]
    df = df / df.ix[0]
    df.plot()
    plt.show()

start = datetime.date(2016, 1, 1)
end = datetime.date.today()
plot_all(start, end)