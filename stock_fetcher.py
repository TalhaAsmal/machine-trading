import pandas_datareader.data as web
import datetime
from os import path
import pandas as pd


def fetch_stocks(stock, start_date, end_date):
    print("Fetching data for {}".format(stock))
    f = web.DataReader(stock, "yahoo", start_date, end_date)
    f.to_csv(path.join("data", "{}.csv".format(stock)), index=True)


def combine_stocks(stocks, col_to_keep, start_date, end_date):
    if "SPY" not in stocks:
        stocks.insert(0, "SPY")

    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    df.index.name = "Date"

    for stock in stocks:
        csv_path = path.join("data", "{}.csv".format(stock))

        if not path.exists(csv_path):
            fetch_stocks(stock, start_date, end_date)

        df_temp = pd.read_csv(csv_path, index_col="Date", usecols=["Date", col_to_keep],parse_dates=True,
                              na_values=["nan"])
        df_temp.rename(columns={col_to_keep: stock}, inplace=True)
        df = df.join(df_temp)
        if stock == "SPY":
            df.dropna(subset=["SPY"], inplace=True)

    df.to_csv(path.join("data", "combined.csv".format(str(start_date), str(end_date))))

start = datetime.date(2000, 1, 1)
end = datetime.date.today()

stocks = ["SPY", "AAPL", "GOOGL", "YHOO", "MSFT", "IBM", "FB", "TWTR", "GOOG", "GLD", "XOM"]
combine_stocks(stocks, "Adj Close", start, end)