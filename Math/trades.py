import pandas as pd
import datetime
from datetime import timedelta
from Math.volume import *
from Math.momentum import *

class Trades:

    def __init__(self, master_df, g_date_start, g_date_end, volume_window_days, performance_window_days, vol_filter, num_coins, btc_start):
        # instantiate objects on front end #
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

    def first_position(self):

        vol_start = int((self.global_date_start_datetime + timedelta(
            days=self.volume_lookback)).strftime("%s"))

        mom_start = int((self.global_date_start_datetime + timedelta(
            days=self.momentum_lookback)).strftime("%s"))

        vol_universe = relevant_universe_list(self.vol_filter, self.master_df, vol_start,
                                              self.global_date_start_datetime_ts)

        first_btc_coin_port = top_momentum_df(vol_universe, self.num_coins, self.master_df, mom_start,
                                                self.global_date_start_datetime_ts)

        allocations = []

        for i in first_btc_coin_port.Pair:

            allocations.append({'Pair': i, 'BTC_Allocation': self.btc_start/len(first_btc_coin_port)})

        return pd.DataFrame(allocations)

    def position_profit(self, start, end, allocations):

        df = self.master_df[(self.master_df.date >= start) & (self.master_df.date <= end)]

        returns = []
        for i in allocations.Pair:

            if i == 'USDT_BTC':

                returns.append({'Pair': i, 'BTC_Return': 0})

            else:

                btc_return = (df[df.Pair == i].weightedAverage.tail(1).values - df[
                    df.Pair == i].weightedAverage.head(1).values) / df[df.Pair == i].weightedAverage.head(1).values

                returns.append({'Pair': i, 'BTC_Return': btc_return[0]})

        returns = pd.DataFrame(returns)

        joined = pd.merge(allocations, returns, on ='Pair', how='inner')

        joined['profits'] = (joined.BTC_Allocation * joined.BTC_Return) + joined.BTC_Allocation

        return joined, joined.profits.sum()

    def trade_positions(self, start_v, end_v, start_m, end_m, btc_bag):

        vol_universe = relevant_universe_list(self.vol_filter, self.master_df, start_v,
                                              end_v)

        btc_port = top_momentum_df(vol_universe, self.num_coins, self.master_df, start_m,
                                    end_m)

        allocations = []

        for i in btc_port.Pair:

            allocations.append({'Pair': i, 'BTC_Allocation': btc_bag/len(btc_port)})

        return pd.DataFrame(allocations)

    def last_position_profit(self, last_allocations, start):

        df = self.master_df[(self.master_df.date >= start) & (self.master_df.date <= self.global_date_end_datetime_ts)]

        returns = []
        for i in last_allocations.Pair:

            if i == 'USDT_BTC':

                returns.append({'Pair': i, 'BTC_Return': 0})

            else:

                btc_return = (df[df.Pair == i].weightedAverage.tail(1).values - df[
                df.Pair == i].weightedAverage.head(1).values) / df[df.Pair == i].weightedAverage.head(
                1).values

                returns.append({'Pair': i, 'BTC_Return': btc_return[0]})

        returns = pd.DataFrame(returns)

        joined = pd.merge(last_allocations, returns, on ='Pair', how='inner')

        joined['profits'] = (joined.BTC_Allocation * joined.BTC_Return) + joined.BTC_Allocation

        return joined, joined.profits.sum()












