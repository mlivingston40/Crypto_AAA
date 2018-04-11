class Volume:

    def __init__(self, coin_filter, df, start_date, end_date):

        self.universe_coins_num = coin_filter
        # This will already be in memory - the master dataframe from class Data #
        self.data = df
        # This should be the start int corresponding in the trade_days dataframe that is in memory #
        self.start_date_int = start_date
        self.end_date_int = end_date

    def relevant_universe_list(self):
        # This will turn the relevant universe for each iteration through the trade_days dataframe #
        # Which will then be used to feed the analytics in the results.py module #
        pass
