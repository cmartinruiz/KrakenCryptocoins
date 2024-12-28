# -*- coding: utf-8 -*-
# Data Fetching and Processing

import requests
import pandas as pd
from datetime import datetime
import time
import krakenex
import numpy as np
import pytz

def date_unix(date_string):
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    dt = pytz.utc.localize(dt)
    return int(dt.timestamp())


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
    return pd.DataFrame(coins_EUR).sort_values(by='Price (EUR)', ascending=False).head(20).reset_index(drop=True)

# Convert date string to UNIX timestamp
def date_unix(date_string):
    # Ensure the datetime object is in UTC
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    dt = pytz.utc.localize(dt)
    return int(dt.timestamp())

# Fetch historical data from Kraken
def get_kraken_data(pair, since=None, interval=1440):
    try:
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
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

# Fetch data for top coins
def fetch_top_coins(since_date, interval_1440=1440, interval_60=60):
    try:
        top20 = get_top20EUR()
        if top20.empty:
            print("Failed to fetch TOP20")
            return pd.DataFrame(), pd.DataFrame()

        dataframes_1440 = []
        dataframes_60 = []

        for _, row in top20.iterrows():
            pair = row['Pair']
            print(f"Fetching historical data for: {pair}")
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
    except Exception as e:
        print(f"Error in fetch_top_coins: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Main execution
if __name__ == "__main__":
    since_date = date_unix("2023-01-01 00:00:00")
    kraken_1440, kraken_60 = fetch_top_coins(since_date)

    if not kraken_1440.empty:
        print("Saving Kraken 1440 data...")
        kraken_1440.to_csv("kraken_1440.csv", index=False)

    if not kraken_60.empty:
        print("Saving Kraken 60 data...")
        kraken_60.to_csv("kraken_60.csv", index=False)
