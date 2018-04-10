import datetime
from datetime import timedelta
import pandas as pd
import requests
import numpy as np

class Data:

    def __init__(self, date_start_, date_end_, volume_window_days_, performance_window_days_):

        self.date_start_str = date_start_
        self.date_start_datetime = datetime.datetime.strptime(date_start_,'%Y-%m-%d')

        self.date_end_str = date_end_
        self.date_end_datetime = datetime.datetime.strptime(date_end_,'%Y-%m-%d')

        self.volume_lookback = -volume_window_days_
        self.momentum_lookback = -performance_window_days_

        self.min_date_datetime = self.date_start_datetime + timedelta(
            days=self.volume_lookback)


    def master_df(self):

        avail_pairs = Data.get_avail_universe_pairs()

        master_data = pd.DataFrame()

        for i in avail_pairs:

            data = pd.DataFrame(requests.get(
                    "https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period=300".format(
                        i, self.min_date_datetime, self.date_end_datetime)).json())
            data['Pair'] = i

            master_data = master_data.append(data)

        return master_data


    @staticmethod
    def get_avail_universe_pairs():

        tickers = pd.DataFrame(requests.get("https://poloniex.com/public?command=returnTicker").json())

        avail_pairs = []
        avail_pairs.append('USDT_BTC')
        for i in tickers.columns:
            if i[0:4] == 'BTC_':
                avail_pairs.append(i)

        return avail_pairs







