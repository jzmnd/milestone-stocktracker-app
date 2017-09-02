# -*- coding: utf-8 -*-
"""
fetchdatalib.py
Functions for fetching stock data from QUANDL and parsing to dataframe

Created by Jeremy Smith on 2017-08-29
"""

import os
import simplejson as json
import requests
import pandas as pd
import yaml
from datetime import timedelta


# Load the config file
try:
    with open('config.yml', 'r') as f:
        config = yaml.load(f)
    QUANDL_API_KEY = config['quandl']['apikey']
except IOError:
    QUANDL_API_KEY = os.environ.get("QUANDL_API_KEY")

# Set global variables
QUANDL_URL = "https://www.quandl.com/api/v3/datatables/WIKI/PRICES"
COLUMNS = "ticker,date,open,high,low,close"


def generate_date_str(date, days=30):
    """Generates date string from python datetime for a given number of days"""
    dates = [(date - timedelta(days=d)).isoformat() for d in xrange(days)]
    return ','.join(dates)


def parseJSONresponse(response):
    """Parse JSON response and status to a data dictionary"""
    data = None
    status = response.status_code
    if status == 200:
        data = json.loads(response.text)
    return data, status


def getEODprice(ticker, date):
    """Get EOD price for a given ticker and date string and output dataframe"""
    url = "{:s}?qopts.columns={:s}&date={:s}&ticker={:s}&api_key={:s}".format(QUANDL_URL,
                                                                              COLUMNS,
                                                                              date,
                                                                              ticker,
                                                                              QUANDL_API_KEY)
    response = requests.get(url)
    datatext, status = parseJSONresponse(response)
    cols = [c['name'] for c in datatext['datatable']['columns']]
    data = datatext['datatable']['data']
    df = pd.DataFrame(data, columns=cols)
    df['date'] = pd.to_datetime(df['date'])
    return df, status
