import pandas as pd

class Volume:

    def __init__(self, coin_filter, df, start_date, end_date):

        self.universe_coins_num = coin_filter
        # This should be the start int corresponding in the trade_days dataframe that is in memory #
        self.start_date_int = start_date
        self.end_date_int = end_date
        # This will already be in memory - the master dataframe from class Data #
        self.df_vol = df[(df.date >= self.start_date_int) & (df.date <= self.end_date_int)]

    def relevant_universe_list(self):
        # This will turn the relevant universe for each iteration through the trade_days dataframe #
        # Which will then be used to feed the analytics in the results.py module #

        pairs = self.df_vol.groupby('Pair').agg({'volume': 'count'})
        # Probably want to bake in a filter for pairs that aren't there for the whole past volume_window_days_ #

        coin_volume = []
        for i in pairs.index:
            data = self.df_vol[self.df_vol['Pair'] == i]
            avg = data.volume.sum() / len(data)
            coin_volume.append({'coin': i, 'avg_vol': avg})
        coin_volume = pd.DataFrame(coin_volume)

        # sort for top based upon 'universe_amt' parameter and return the list #

        return list(coin_volume.sort_values(by=['avg_vol'], ascending=False).head(self.universe_coins_num))



