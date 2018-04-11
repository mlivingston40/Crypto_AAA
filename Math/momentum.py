class Momentum:

    def __init__(self, num_coins_allocate, df, start_date, end_date):

        self.num_coins = num_coins_allocate
        # This will already be in memory - the master dataframe from class Data #
        self.data = df
        # This should be the start int corresponding in the trade_days dataframe that is in memory #
        self.start_date_int = start_date
        self.end_date_int = end_date

    def relevant_coin_list(self):
        # This will turn the relevant coins to buy for each iteration through the trade_days dataframe #
        # Which will then be used to feed the analytics in the results.py module #
        pass


