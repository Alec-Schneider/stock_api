import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


class Equity:
    def __init__(self):
        pass
    
    def get_sp500_tickers(self):
        data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        table = data[0]
        return table
    

    def download_ticker(self, ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return  data
    
    def track_50_200_signal(self, data):
        """
        Caclulate the 50 day and 200 day moving average of the Adj. Close price of the security.
        Then create 'cross50' column to signal if the 50 day avg. crosses above or below the 200 
        day avg.and get the crossing 50day price when it crossed as 'cross_price'.
        
        """
         # Calculate the 50-day and 200-day moving averages
        data['50_day_ma'] = data['Adj Close'].rolling(window=50).mean()
        data['200_day_ma'] = data['Adj Close'].rolling(window=200).mean()
        cmap = mpl.colors.ListedColormap(["purple", "green"])
        # get shapes to pass to matplotlib plot function

        data["cross50"] = np.where(
            # if 50 was above 200 the day prior and is now below the 200, -1
            ((data['50_day_ma'].shift(1) > data['200_day_ma'].shift(1))
            & (data['50_day_ma'] < data['200_day_ma'])),
            -1,
            # if 50 was below 200 the day prior and is now above the 200, 1
            np.where(
                ((data['50_day_ma'].shift(1) < data['200_day_ma'].shift(1))
            & (data['50_day_ma'] > data['200_day_ma'])),
            1,
            0
            )
         )
        
        data["cross_price"] = np.where(
            data["cross50"] != 0,
            data['50_day_ma'],
            None
        )

        data["cross_above_below"]  = np.where(
            data['cross50'] == 1,
            "above",
            np.where(
            data['cross50'] == -1,
            "below",
            None
            )
        )

        # fig, ax = plt.subplots(1)
        # data[['50_day_ma', '200_day_ma']].plot(ax=ax)
        # # data.reset_index().plot(kind="scatter", x="Date", y="cross_price", ax=ax, c="cross50", cmap=cmap)
        # # create a scatter plot for both the values of 1 and -1 of cross50 with a different marker for each
        # data[data["cross50"] == 1].reset_index().plot(kind="scatter", x="Date", y="cross_price", ax=ax, c="green", marker="^")
        # data[data["cross50"] == -1].reset_index().plot(kind="scatter", x="Date", y="cross_price", ax=ax, c="red", marker="v")
        
        # fig.show()
        # fig.savefig("plot.png")

        crosses = data[data["cross50"] != 0]
        for i in range(len(crosses)):
            if crosses['cross50'][i] == 1:
                current_state = "above"
            if crosses['cross50'][i] == -1:
                current_state = "below"

            date = crosses.index[i].strftime('%Y-%m-%d')
            print(f"The 50-day MA crossed {current_state} the 200-day MA on {date}.")

        # crosses = crosses.reset_index()
        # for i in range(1, len(crosses)):
            
        #     entry_point = crosses.iloc[i-1]
        #     signal = "above" if entry_point["cross50"] == 1 else "below"
        #     exit_point = crosses.iloc[i]
        #     price_return = (exit_point['Adj Close'] - entry_point['Adj Close'])/ entry_point['Adj Close'] * 100
        #     print(f"Period of {signal}")
        #     print(f"{entry_point['Date']} - {exit_point['Date']}: {price_return:.2f}%")

        return data