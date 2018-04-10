import datetime
from datetime import timedelta
import pandas as pd
import requests
import numpy as np



def get_avail_universe_pair():

    tickers = pd.DataFrame(requests.get("https://poloniex.com/public?command=returnTicker").json())
    tickers.columns





