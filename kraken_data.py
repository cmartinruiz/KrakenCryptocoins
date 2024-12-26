# -*- coding: utf-8 -*-
"""Kraken_Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LVG437_HYtLC8Eh1XUNp5o-5bGiZmyCQ
"""

import requests
import pandas as pd
from datetime import datetime
import time
import numpy as np
import krakenex

# Get TOP20 sorted by price (EUR) list
def get_top20EUR():
    api = krakenex.API()
    ticker_data = api.query_public('Ticker')
    if 'error' in ticker_data and ticker_data['error']:
        print(f"API error: {ticker_data['error']}")
        return pd.DataFrame()
    coins_EUR = []
    for pair, data in ticker_data['result'].items():
        if pair.endswith('EUR'):
            try:
                coin = pair.replace('EUR', '')
                last_price = float(data['c'][0])
                coins_EUR.append({'Coin': coin, 'Pair': pair, 'Price (EUR)': last_price})
            except (KeyError, ValueError):
                print(f"Error processing pair {pair}")
    df = pd.DataFrame(coins_EUR)
    return df.sort_values(by='Price (EUR)', ascending=False).head(20).reset_index(drop=True)

# Date format
def date_unix(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(time.mktime(dt.timetuple()))

# Fetch OHLC data from Kraken
def get_kraken_data(pair, since=None, interval=1440):
    k = krakenex.API()
    ohlc = k.query_public('OHLC', data={'pair': pair, 'interval': interval, 'since': since})
    if ohlc and ohlc['error'] == []:
        df = pd.DataFrame(ohlc['result'][pair], columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df[['open', 'high', 'low', 'close', 'vwap']] = df[['open', 'high', 'low', 'close', 'vwap']].astype(float)
        return df
    else:
        print(f"Error obtaining data from Kraken: {ohlc['error']}")
        return pd.DataFrame()

# Fetch top coins' data
def fetch_top_coins(since_date, interval_1440=1440, interval_60=60):
    top20 = get_top20EUR()
    if top20.empty:
        print("Failed to fetch TOP20")
        return pd.DataFrame(), pd.DataFrame()
    dataframes_1440 = []
    dataframes_60 = []
    for _, row in top20.iterrows():
        pair = row['Pair']
        df_1440 = get_kraken_data(pair, since=since_date, interval=int(interval_1440))
        if not df_1440.empty:
            df_1440['Coin'] = row['Coin']
            dataframes_1440.append(df_1440)
        df_60 = get_kraken_data(pair, since=since_date, interval=int(interval_60))
        if not df_60.empty:
            df_60['Coin'] = row['Coin']
            dataframes_60.append(df_60)
    kraken_1440 = pd.concat(dataframes_1440, ignore_index=True) if dataframes_1440 else pd.DataFrame()
    kraken_60 = pd.concat(dataframes_60, ignore_index=True) if dataframes_60 else pd.DataFrame()
    return kraken_1440, kraken_60

# Bollinger Bands calculation
def bollinger_bands(data, window=20):
    data['mean'] = data['close'].rolling(window).mean()
    data['std'] = data['close'].rolling(window).std()
    data['upper_band'] = data['mean'] + (data['std'] * 2)
    data['lower_band'] = data['mean'] - (data['std'] * 2)
    data['buy_signal'] = np.where(data['close'] < data['lower_band'], 1, 0)
    data['sell_signal'] = np.where(data['close'] > data['upper_band'], 1, 0)
    return data