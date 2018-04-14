# Web application to back test the momentum strategy

## Parameters will be:

### N Days Volume Filter Lookback (default of 70)
### Top N coins for volume filter on Poloniex (default of 20)
### N Days Momentum Filter Lookback (default of 21)
### Top N coins for momentum (default of 10)
### N Days to Recalibrate (default of 7)


## Data will be pulling from an aggregated mysql database (which has aws lambda job pulling from poloniex api on some sort cron job schedule to keep data up to date)

