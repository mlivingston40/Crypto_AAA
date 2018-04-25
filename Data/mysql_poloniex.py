import datetime
from datetime import timedelta
import pandas as pd
import requests

import pandas as pd
import pymysql.cursors
import time

class Data:

    def __init__(self, date_start, date_end, volume_window_days):

        self.date_start_str = date_start
        self.date_start_datetime = datetime.datetime.strptime(self.date_start_str,'%Y-%m-%d')
        self.date_start_datetime_ts = int(self.date_start_datetime.strftime("%s"))

        self.date_end_str = date_end
        self.date_end_datetime = datetime.datetime.strptime(self.date_end_str,'%Y-%m-%d')
        self.date_end_datetime_ts = int(self.date_end_datetime.strftime("%s"))

        self.volume_lookback = -volume_window_days

        ## assumption is that volume lookback will always be longer than momentum window ##
        self.min_date_datetime = self.date_start_datetime + timedelta(
            days=self.volume_lookback)
        self.min_date_datetime_ts = int(self.min_date_datetime.strftime("%s"))

        self.connection = pymysql.connect(host='mysql-instance-dev-crypto.ceytqsjhi5fg.us-east-2.rds.amazonaws.com',
                             user='mlivingston',
                             password='Paradise2',
                             db='Poloniex',
                             port=3306)

    def master_df(self):

        avail_pairs = Data.get_avail_universe_pairs()

        master_data = pd.DataFrame()

        for i in avail_pairs:
            select = "Select * From " + i + " where date between {} and {}".format(self.min_date_datetime_ts, self.date_end_datetime_ts)

            data = pd.read_sql(select, con=self.connection)

            master_data = master_data.append(data)

        self.connection.close()

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







