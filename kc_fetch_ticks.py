# -*- coding: utf-8 -*-
"""
Zerodha Kite Connect - fetching tick data from db and converting to candles

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""
from kiteconnect import KiteConnect
import pandas as pd
import os
import sqlite3

cwd = os.chdir("D:\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)


def instrumentLookup(instrument_df,symbol):
    """Looks up instrument token for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1

db = sqlite3.connect('D:/Udemy/Zerodha KiteConnect API/7_streaming_data/ticks.db')

def get_hist(ticker,db):
    token = instrumentLookup(instrument_df,ticker)
    data = pd.read_sql('''SELECT * FROM TOKEN%s WHERE ts >=  date() - '12 day';''' %token, con=db)                
    data = data.set_index(['ts'])
    data.index = pd.to_datetime(data.index)
    ticks = data.loc[:, ['price']]   
    df=ticks['price'].resample('5min').ohlc().dropna()
    return df


get_hist("INFY",db)