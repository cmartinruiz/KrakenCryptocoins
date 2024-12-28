# -*- coding: utf-8 -*-

# Extracción y manejo de datos
import requests
import pandas as pd
from datetime import datetime
import time
import numpy as np

# Krakenex
import krakenex

# Vsiualización de datos
import matplotlib.pyplot as plt
import plotly.graph_objs as go

## Dash app for the interactive plot
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import shutil
import os
import io
import itertools
from itertools import cycle

# Testing y manejo de errores
import unittest

"""## Extracción de datos"""

# Get TOP20 sorted by price (EUR) list
def get_top20EUR():
    # Initialize Kraken API client
    api = krakenex.API()

    # Fetch ticker information for all pairs
    ticker_data = api.query_public('Ticker')

    # Check if the API call was successful
    if 'error' in ticker_data and ticker_data['error']:
        print(f"API error: {ticker_data['error']}")
        return pd.DataFrame()

    # Extract and filter pairs with 'USD'
    coins_EUR = []
    for pair, data in ticker_data['result'].items():
        # Only consider pairs ending with "EUR"
        if pair.endswith('EUR'):
            try:
                # Extract the coin name (e.g., BTC, ETH)
                coin = pair.replace('EUR', '')

                # Get the last trade price
                last_price = float(data['c'][0])

                coins_EUR.append({
                    'Coin': coin,
                    'Pair': pair,
                    'Price (EUR)': last_price
                })
            except (KeyError, ValueError):
                print(f"Error processing pair {pair}")

    # Convert to a DataFrame
    df = pd.DataFrame(coins_EUR)
    df_sorted = df.sort_values(by='Price (EUR)', ascending=False).head(20).reset_index(drop=True)

    return df_sorted

# Define a class for Coins to check which coins are available
class Coin:
    def __init__(self, name, pair):
        self.name = name
        self.pair = pair

    def __repr__(self):
        return f"Coin(name='{self.name}', pair='{self.pair}')"

# Fetch and display the top 20 coins in USD
top20 = get_top20EUR()
coins = [Coin(row['Coin'], row['Pair']) for _, row in top20.iterrows()]
print(top20)
print(coins)


#Date format
def date_unix(date_string):
    # Example implementation
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(dt.timetuple()))

#Get data
def get_kraken_data(pair, since=None, interval=1440):
  try:
    k = krakenex.API()
    ohlc = k.query_public('OHLC', data={'pair': pair, 'interval': interval, 'since': since})
    if ohlc and ohlc['error'] == []:
      df = pd.DataFrame(ohlc['result'][pair], columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume','count'])
      df['time'] = pd.to_datetime(df['time'], unit='s')
      df[['open', 'high', 'low', 'close', 'vwap']] = df[['open', 'high', 'low', 'close', 'vwap']].astype(float)
      return df
    else:
      print(f"Error obtaining data from Kraken: {ohlc['error']}")
      return pd.DataFrame(), pd.DataFrame()
  except Exception as e:
    print(f"Error: {e}")
    return pd.DataFrame()

#Fetch data
def fetch_top_coins(since_date, interval_1440=1440, interval_60=60):
    try:
        top20 = get_top20EUR()
        if top20.empty:
          print("Failed to fetch TOP20")
          return pd.DataFrame, pd.DataFrame()

        dataframes_1440=[]
        dataframes_60=[]

        for _, row in top20.iterrows():
          pair=row['Pair']
          print(f"Fetching historical data for: {pair}")

          df_1440 = get_kraken_data(pair, since=since_date, interval=int(interval_1440))
          if not df_1440.empty:
              df_1440['Coin'] = row['Coin']  # Add coin name to the dataframe
              dataframes_1440.append(df_1440)

          df_60 = get_kraken_data(pair, since=since_date, interval=int(interval_60))
          if not df_60.empty:
              df_60['Coin'] = row['Coin']  # Add coin name to the dataframe
              dataframes_60.append(df_60)

        kraken_1440 = pd.concat(dataframes_1440, ignore_index=True) if dataframes_1440 else pd.DataFrame()
        kraken_60 = pd.concat(dataframes_60, ignore_index=True) if dataframes_60 else pd.DataFrame()

        return kraken_1440, kraken_60

    except Exception as e:
        print(f"Error in fetch_top_coins: {e}")
        return pd.DataFrame(), pd.DataFrame()

#Parameters
since_date = date_unix("2023-01-01 00:00:00")

#Final df
kraken_1440, kraken_60 = fetch_top_coins(since_date)
if not kraken_1440.empty:
    print("Kraken 1440 data:")
    print(kraken_1440.head())

if not kraken_60.empty:
    print("Kraken 60 data:")
    print(kraken_60.head())

"""## Visualización de datos"""

# Bollinger Bands Calculation

def bollinger_bands(data, window=20):
    if 'mean' not in data or 'upper_band' not in data or 'lower_band' not in data:  # Check if already calculated
        data['mean'] = data['close'].rolling(window).mean()
        data['std'] = data['close'].rolling(window).std()
        data['upper_band'] = data['mean'] + (data['std'] * 2)
        data['lower_band'] = data['mean'] - (data['std'] * 2)

    # Create Buy/Sell signals
    data['buy_signal'] = np.where(data['close'] < data['lower_band'], 1, 0)  # Buy when price crosses below the lower band
    data['sell_signal'] = np.where(data['close'] > data['upper_band'], 1, 0)  # Sell when price crosses above the upper band

    return data

# Dash Application
colors = itertools.cycle(['#6f42c1', '#007bff', '#6610f2', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#fd7e14'])

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        # Header Section
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Coins selected", style={"font-weight": "bold", "color": "dimgray"}),
                            dcc.Dropdown(
                                id="coin-dropdown",
                                options=[{'label': coin, 'value': coin} for coin in kraken_1440['Coin'].unique()],
                                value=['TBTC', 'XETHZ'],  # Default coins
                                multi=True,
                                style={'backgroundColor': '#FFFFFF', 'color': '#6c757d'}
                            ),
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Values", style={"font-weight": "bold", "color": "dimgray"}),
                            dcc.Dropdown(
                                id="yaxis-column",
                                options=[{'label': col, 'value': col} for col in kraken_1440.columns if col not in ['time', 'Coin', 'vwap', 'count']],
                                value='close',
                                style={'backgroundColor': '#FFFFFF', 'color': '#6c757d'}
                            ),
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Interval", style={"font-weight": "bold", "color": "dimgray"}),
                            dcc.Dropdown(
                                id="interval-dropdown",
                                options=[
                                    {'label': 'Daily (24h)', 'value': '1440'},
                                    {'label': 'Hourly (1h)', 'value': '60'},
                                ],
                                value='1440',  # Default interval
                                style={'backgroundColor': '#FFFFFF', 'color': '#6c757d'}
                            ),
                        ]
                    ),
                    width=4,
                ),
            ],
            justify="around",
            style={"marginBottom": "20px"},
        ),

        # Date Picker Range
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=kraken_1440['time'].min().strftime('%Y-%m-%d'),
                            end_date=kraken_1440['time'].max().strftime('%Y-%m-%d'),
                            display_format='YYYY-MM-DD',
                            style={
                                'backgroundColor': '#F5F5F5',
                                'color': '#6c757d',
                                'padding': '10px',
                                'width': '100%',
                            },
                            day_size=30
                        ),
                    ]
                ),
                width=4,
            ),
            justify="end",
            style={"marginBottom": "20px"},
        ),

        # Main Chart and Bollinger Band Chart
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="cryptocurrency-chart", config={'displayModeBar': False}),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(id="bollinger-chart", config={'displayModeBar': False}),
                    width=6,
                ),
            ]
        ),
    ],
    fluid=True,
    style={'backgroundColor': '#F5F5F5', 'padding': '20px'},
)

@app.callback(
    [Output('cryptocurrency-chart', 'figure'),
     Output('bollinger-chart', 'figure')],
    [
        Input('coin-dropdown', 'value'),
        Input('yaxis-column', 'value'),
        Input('interval-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
    ]
)
def update_charts(selected_coins, y_column, interval, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Handle interval filtering
    if interval == '60':
        filtered_df = kraken_60[kraken_60['Coin'].isin(selected_coins)]
    else:
        filtered_df = kraken_1440[kraken_1440['Coin'].isin(selected_coins)]

    filtered_df = filtered_df[(filtered_df['time'] >= start_date) & (filtered_df['time'] <= end_date)]
    filtered_df['time'] = pd.to_datetime(filtered_df['time'])

    # Ensure valid candlestick data
    filtered_df = filtered_df[(filtered_df['low'] > 0) & (filtered_df['high'] > 0) & (filtered_df['close'] > 0) & (filtered_df['open'] > 0)]

    # Main Chart: Line chart for multiple coins
    traces = []
    if len(selected_coins) == 1:  # Single coin: Line chart for the main chart
        coin_df = filtered_df[filtered_df['Coin'] == selected_coins[0]]
        traces.append(
            go.Scatter(
                x=coin_df['time'],
                y=coin_df[y_column],
                mode='lines',
                name=f"{selected_coins[0]} {y_column.capitalize()}",
                line=dict(color='#007bff', width=2), #AQUI
            )
        )
    else:  # Multiple coins: Line charts for selected y_column
        for coin, color in zip(selected_coins, colors):
            coin_df = filtered_df[filtered_df['Coin'] == coin]
            traces.append(
                go.Scatter(
                    x=coin_df['time'],
                    y=coin_df[y_column],
                    mode='lines',
                    name=coin,
                    line=dict(color=color),
                )
            )

    main_chart = {
        'data': traces,
        'layout': go.Layout(
            title=f"Cryptocurrency {y_column.capitalize()} over Time",
            xaxis=dict(
                title="Time",
                type="date",  # Ensure the x-axis interprets datetime values
            ),
            yaxis=dict(title=y_column.capitalize()),
            paper_bgcolor='#F5F5F5',
            plot_bgcolor='#F5F5F5',
            font=dict(color='dimgray'),
        ),
    }

    # Bollinger Bands Chart: Candlestick + Bollinger Bands + Mean
    if len(selected_coins) == 1:
        single_coin_df = filtered_df[filtered_df['Coin'] == selected_coins[0]]
        single_coin_df = bollinger_bands(single_coin_df)

        bollinger_chart = {
            'data': [
                # Candlestick Chart
                go.Candlestick(
                    x=single_coin_df['time'],
                    open=single_coin_df['open'],
                    high=single_coin_df['high'],
                    low=single_coin_df['low'],
                    close=single_coin_df['close'],
                    name='Candlestick',
                    increasing_line_color='darkgreen',
                    decreasing_line_color='darkred',
                ),
                # Upper Band
                go.Scatter(
                    x=single_coin_df['time'],
                    y=single_coin_df['upper_band'],
                    mode='lines',
                    line=dict(color='rgba(0, 100, 80, 0)'),  # Transparent line
                    name='Upper Band',
                    showlegend=False
                ),
                # Lower Band (Shaded area between upper and lower bands)
                go.Scatter(
                    x=single_coin_df['time'],
                    y=single_coin_df['lower_band'],
                    mode='lines',
                    fill='tonexty',  # Fill area between this trace and the previous
                    fillcolor='rgba(0, 100, 80, 0.2)',  # Light green shading
                    line=dict(color='rgba(0, 100, 80, 0)'),  # Transparent line
                    name='Bollinger Bands',
                ),
                # Mean Line
                go.Scatter(
                    x=single_coin_df['time'],
                    y=single_coin_df['mean'],
                    mode='lines',
                    line=dict(color='darkblue', dash='dot', width=2),
                    name='Mean',
                ),
                # Buy Signal (mark with green dots)
                go.Scatter(
                    x=single_coin_df[single_coin_df['buy_signal'] == 1]['time'],
                    y=single_coin_df[single_coin_df['buy_signal'] == 1]['close'],
                    mode='markers',
                    name='Buy Signal',
                    marker=dict(color='green', size=7, symbol='triangle-up'),
                ),
                # Sell Signal (mark with red dots)
                go.Scatter(
                    x=single_coin_df[single_coin_df['sell_signal'] == 1]['time'],
                    y=single_coin_df[single_coin_df['sell_signal'] == 1]['close'],
                    mode='markers',
                    name='Sell Signal',
                    marker=dict(color='red', size=7, symbol='triangle-down'),
                ),
            ],
            'layout': go.Layout(
                title=f"Bollinger Bands for {selected_coins[0]}",
                xaxis=dict(
                    title="Time",
                    type="date",
                ),
                yaxis=dict(
                    title="Price",
                    fixedrange=False,  # Allow scaling
                ),
                paper_bgcolor='#F5F5F5',
                plot_bgcolor='#F5F5F5',
                font=dict(color='dimgray'),
            ),
        }
    else:
        bollinger_chart = {
            'data': [],
            'layout': go.Layout(
                title="Select a single coin to view Bollinger Bands",
                paper_bgcolor='#F5F5F5',
                plot_bgcolor='#F5F5F5',
                font=dict(color='dimgray'),
            ),
        }

    return main_chart, bollinger_chart


if __name__ == "__main__":
    app.run_server(debug=True)
