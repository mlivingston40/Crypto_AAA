import pandas as pd

class Momentum:

    def __init__(self, rel_universe, num_coins_allocate, df, start_date, end_date):

        self.rel_universe = rel_universe
        self.num_coins = num_coins_allocate
        # This should be the start int corresponding in the trade_days dataframe that is in memory #
        self.start_date_int = start_date
        self.end_date_int = end_date
        # This will already be in memory - the master dataframe from class Data #
        self.df_mom = df[(df.date >= self.start_date_int) & (df.date <= self.end_date_int)]

    def top_momentum_df(self):

        returns = []
        for i in self.rel_universe:

            mom = (self.df_mom[self.df_mom.Pair == i].weightedAverage.tail(1).values - self.df_mom[
                self.df_mom.Pair == i].weightedAverage.head(1).values) / self.df_mom[self.df_mom.Pair == i].weightedAverage.head(
                1).values

            returns.append({'Pair': i, 'Momentum': mom[0]})

        returns = pd.DataFrame(returns)

        top_returns = returns.sort_values(by=['Momentum'], ascending = False).head(self.num_coins)

        #account for only positive momentum #

        return top_returns[top_returns.Momentum > 0]



