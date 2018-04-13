import pandas
import datetime
from datetime import timedelta
from Math.volume import *
from Math.momentum import *

class Trades:

    def __init__(self, master_df, trade_days_df, g_date_start, g_date_end, volume_window_days, performance_window_days, vol_filter, num_coins, btc_start):
        # instantiate objects on front end #
        self.trade_df = trade_days_df
        self.master_df = master_df

        self.global_date_start_str = g_date_start
        self.global_date_start_datetime = datetime.datetime.strptime(self.global_date_start_str,'%Y-%m-%d')
        self.global_date_start_datetime_ts = int(self.global_date_start_datetime.strftime("%s"))

        self.global_date_end_str = g_date_end
        self.global_date_end_datetime = datetime.datetime.strptime(self.global_date_end_str,'%Y-%m-%d')
        self.global_date_end_datetime_ts = int(self.global_date_end_datetime.strftime("%s"))

        self.volume_lookback = -volume_window_days
        self.momentum_lookback = -performance_window_days

        self.btc_start = btc_start

        self.vol_filter = vol_filter
        self.num_coins = num_coins

    # def first_position(self):
    # def last_position(self):


    def trade_positions(self):

        for i in range(0, len(self.trade_df)):

            if i == 0:

                vol_start = int((self.global_date_start_datetime + timedelta(
                    days=self.volume_lookback)).strftime("%s"))

                mom_start = int((self.global_date_start_datetime + timedelta(
                    days=self.momentum_lookback)).strftime("%s"))

                vol_universe = relevant_universe_list(self.vol_filter, self.master_df, vol_start, self.global_date_end_datetime_ts)
                coin_port = top_momentum_df(vol_universe.coin, self.num_coins, self.master_df, mom_start, self.global_date_end_datetime_ts)

            else:
                pass

            return pd.DataFrame(coin_port)





    #
    #
    #
    # def coins(self):
    #
    #     return Momentum(Volume(self.coin_filter,self.master_df,self.start_date,self.end_date),self.coins, self.master_df,self.start_Date,self.end_date)
    #
    #
    #
    #
    #
    # def btc_start(self):
    #
    #
    #
    # def btc_end(self):
    #
    #
    #
    #
    # Volume()