import pandas as pd
## should build something in for no return at all
###make just btc then

def top_momentum_df(rel_universe, num_coins_allocate, df, start_date, end_date):

    # This will already be in memory - the master dataframe from class Data #
    df_mom = df[(df.date >= start_date) & (df.date <= end_date)]


    returns = []
    for i in rel_universe:

        mom = (df_mom[df_mom.Pair == i].weightedAverage.tail(1).values - df_mom[
            df_mom.Pair == i].weightedAverage.head(1).values) / df_mom[df_mom.Pair == i].weightedAverage.head(
            1).values

        returns.append({'Pair': i, 'Momentum': mom[0]})

    returns = pd.DataFrame(returns)

    top_returns = returns.sort_values(by=['Momentum'], ascending = False).head(num_coins_allocate)

    # account for only positive momentum #

    top_returns = top_returns[top_returns.Momentum > 0]

    if len(top_returns) == 0:

        top_returns = top_returns.append({'Pair': 'USDT_BTC',
                                              'Momentum': "No coins with momentum"}, ignore_index=True)
    else:
        pass

    return top_returns



