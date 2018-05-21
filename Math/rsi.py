"""
RSI = 100 - 100 / (1 + RS)

Where RS = Average gain of up periods during the specified time frame / Average loss of down periods during the specified time frame/



Read more: Relative Strength Index (RSI) https://www.investopedia.com/terms/r/rsi.asp#ixzz5ETQLkGOQ 
Follow us: Investopedia on Facebook
"""

### Since this is a momentum indicator will do the same window as meomentum

### RSI just has to be under 70 to qualify ###


import pandas as pd

first_allocation = trades.first_position()
print("done w/ first allocation")

for i in range(0, len(trades_days_df)):

    if i == 0:

        allocations = trades.trade_positions(trades_days_df.Volume_LB_Start_ts[0].item(),
                                             trades_days_df.Trade_Date_ts[0].item(),
                                             trades_days_df.Performance_LB_Start_ts[0].item(),
                                             trades_days_df.Trade_Date_ts[0].item(),
                                             trades_days_df.RSI_1_LB_Start_ts[0].item(),
                                             trades_days_df.Performance_LB_Start_ts[0].item(),
                                             trades_days_df.RSI_2_LB_Start_ts[0].item(),
                                             trades_days_df.Trade_Date_ts[0].item())


    elif i == len(trades_days_df) - 1:

        allocation = trades.trade_positions(trades_days_df.Volume_LB_Start_ts[i].item(),
                                             trades_days_df.Trade_Date_ts[i].item(),
                                             trades_days_df.Performance_LB_Start_ts[i].item(),
                                             trades_days_df.Trade_Date_ts[i].item(),
                                             trades_days_df.RSI_1_LB_Start_ts[i].item(),
                                             trades_days_df.Performance_LB_Start_ts[i].item(),
                                             trades_days_df.RSI_2_LB_Start_ts[i].item(),
                                             trades_days_df.Trade_Date_ts[i].item())

        allocations = allocations.append(allocation)

    else:

        allocation = trades.trade_positions(trades_days_df.Volume_LB_Start_ts[i].item(),
                                             trades_days_df.Trade_Date_ts[i].item(),
                                             trades_days_df.Performance_LB_Start_ts[i].item(),
                                             trades_days_df.Trade_Date_ts[i].item(),
                                             trades_days_df.RSI_1_LB_Start_ts[i].item(),
                                             trades_days_df.Performance_LB_Start_ts[i].item(),
                                             trades_days_df.RSI_2_LB_Start_ts[i].item(),
                                             trades_days_df.Trade_Date_ts[i].item())

        allocations = allocations.append(allocation)

        # end = time.time()
        # print(end - start)
        # print(final_btc_bag)
        # return trade_ports.to_html()