#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Financial ratio scan and sort

"""

# Import modules
import time
import requests
import pandas as pd

from fmp_key import fmp_key

params = {'apikey': fmp_key}

ticker_request = requests.get(
    'https://financialmodelingprep.com/api/v3/stock/list',
    params = params
)
all_tickers = pd.DataFrame(ticker_request.json())

fs_ticker_request = requests.get(
    'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists',
    params = params
)
fs_tickers = fs_ticker_request.json()

print(all_tickers.type.unique())
print(all_tickers.exchange.unique())

all_tickers_sorted = all_tickers.sort_values(
    by=['symbol'], 
    ignore_index=True
)

exchanges = [
    'NASDAQ',
    'Nasdaq',
    'NASDAQ Capital Market',
    'NASDAQ Global Market',
    'NASDAQ Global Select',
    'New York Stock Exchange',
    'New York Stock Exchange Arca',
    'American Stock Exchange',
    'NASDAQ Stock Exchange',
    'NASDAQ Stock Market', 
    'BATS'
]

asset_types = ['stock']

filtered_tickers = all_tickers[
    (all_tickers['exchange'].isin(exchanges)) & 
    (all_tickers['type'].isin(asset_types))
]

filtered_tickers = filtered_tickers.reset_index(drop=True)
filtered_tickers_list = list(filtered_tickers.symbol)

common_tickers = sorted(list(set(fs_tickers) & set(filtered_tickers_list)))

# Remove items with '-'
common_tickers = [i for i in common_tickers if '-' not in i]

# Shorten list
req_list = common_tickers[:2]

# Set endpoint and params
metrics_endpoint = 'https://financialmodelingprep.com/api/v3/key-metrics/'
metrics_params = {
    'apikey': fmp_key,
    'period': 'annual'
}

# Dictionary for metric data
all_metrics = []

for ticker in req_list:
    res = requests.get(url=f'{metrics_endpoint}{ticker}', params=metrics_params)
    for fs in res.json():
        if (fs['calendarYear'] == '2023' and fs['period'] == 'FY'):
            all_metrics.append(fs)
    # time.sleep(13)

fs_metrics = pd.DataFrame(all_metrics)
fs_metrics.to_excel('fs_metrics.xlsx', index=False)

sorted_by_ratio = fs_metrics[['symbol', 'debtToEquity']].sort_values(
    'debtToEquity', 
    ascending=False
    )

sorted_by_ratio.to_excel('sorted_ratio.xlsx', index=False)