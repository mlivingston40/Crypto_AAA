import datetime
from datetime import timedelta
import pandas as pd

class TradeDays:

    def __init__(self, date_start, date_end, volume_window_days, performance_window_days, recalibrate_days):

        self.date_start_str = date_start
        self.date_start_datetime = datetime.datetime.strptime(self.date_start_str,'%Y-%m-%d')
        self.date_start_datetime_ts = int(self.date_start_datetime.strftime("%s"))

        self.date_end_str = date_end
        self.date_end_datetime = datetime.datetime.strptime(self.date_end_str,'%Y-%m-%d')
        self.date_end_datetime_ts = int(self.date_end_datetime.strftime("%s"))

        self.volume_lookback = -volume_window_days

        self.momentum_lookback = -performance_window_days

        self.recalibrate_days = recalibrate_days

        # number of times you will recalibrate
        self.recal_times = int(((self.date_end_datetime - self.date_start_datetime).days)/self.recalibrate_days)


    def trade_days_df(self):

        trade_days = []
        for i in range(0, self.recal_times):

            trade_days.append({'Trade_Number': i + 1,

                               'Trade_Date': self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days),

                               'Trade_Date_str': (self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days)).strftime('%Y-%m-%d'),

                               'Trade_Date_ts': int((self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days)).strftime("%s")),

                               'Performance_LB_Start': self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days + self.momentum_lookback),

                               'Performance_LB_Start_str': (self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days + self.momentum_lookback)).strftime('%Y-%m-%d'),

                               'Performance_LB_Start_ts': int((self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days + self.momentum_lookback)).strftime("%s")),

                               'Volume_LB_Start': self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days + self.volume_lookback),

                               'Volume_LB_Start_str': (self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days + self.volume_lookback)).strftime('%Y-%m-%d'),

                               'Volume_LB_Start_ts': int((self.date_start_datetime + timedelta(
                                   days=(i + 1) * self.recalibrate_days + self.volume_lookback)).strftime("%s"))
                               })
        return pd.DataFrame(trade_days)

