import pandas_datareader.data as web
import datetime
from os import path
import pandas as pd


def fetch_stocks(stock, start_date, end_date):
    print("Fetching data for {}".format(stock))
    f = web.DataReader(stock, "google", start_date, end_date)
    f.to_csv(path.join("data", "{}.csv".format(stock.replace(":", "_"))), index=True)


def combine_stocks(stocks, col_to_keep, tracker_etf, start_date, end_date, prefix):
    if tracker_etf not in stocks:
        stocks.insert(0, tracker_etf)

    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    df.index.name = "Date"

    for stock in stocks:
        csv_path = path.join("data", "{}.csv".format(stock.replace(":", "_")))

        if not path.exists(csv_path):
            fetch_stocks(stock, start_date, end_date)

        df_temp = pd.read_csv(csv_path, index_col="Date", usecols=["Date", col_to_keep],parse_dates=True,
                              na_values=["nan"])
        df_temp.rename(columns={col_to_keep: stock}, inplace=True)
        df = df.join(df_temp)
        if stock == tracker_etf:
            df.dropna(subset=[tracker_etf], inplace=True)

    df.to_csv(path.join("data", "{}_combined_{}_{}.csv".format(prefix, str(start_date), str(end_date))))

start = datetime.date(2000, 1, 1)
end = datetime.date.today()

# stocks = ["SPY", "AAPL", "GOOGL", "YHOO", "MSFT", "IBM", "FB", "TWTR", "GOOG", "GLD", "XOM"]

stocks = pd.read_csv(path.join('stock_lists', 'jse_salsi.csv')).stocks.values.tolist()

# combine_stocks(stocks, "Adj Close", start, end)
combine_stocks(stocks, 'Close', 'JSE:BBET40', start, end, 'salsi')