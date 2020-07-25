# -*- coding: utf-8 -*-
"""
Zerodha Kite Connect - auto square off

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""
from kiteconnect import KiteConnect
import os
import pandas as pd

cwd = os.chdir("D:\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)


def placeMarketOrder(symbol,buy_sell,quantity):    
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=kite.EXCHANGE_NSE,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_MARKET,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR)
    
def CancelOrder(order_id):    
    # Modify order given order id
    kite.cancel_order(order_id=order_id,
                    variety=kite.VARIETY_REGULAR)  

#fetching orders and position information   
a,b = 0,0
while a < 10:
    try:
        pos_df = pd.DataFrame(kite.positions()["day"])
        break
    except:
        print("can't extract position data..retrying")
        a+=1
while b < 10:
    try:
        ord_df = pd.DataFrame(kite.orders())
        break
    except:
        print("can't extract order data..retrying")
        b+=1

#closing all open position      
for i in range(len(pos_df)):
    ticker = pos_df["tradingsymbol"].values[i]
    if pos_df["quantity"].values[i] >0:
        quantity = pos_df["quantity"].values[i]
        placeMarketOrder(ticker,"sell", quantity)
    if pos_df["quantity"].values[i] <0:
        quantity = abs(pos_df["quantity"].values[i])
        placeMarketOrder(ticker,"buy", quantity)

#closing all pending orders
pending = ord_df[ord_df['status'].isin(["TRIGGER PENDING","OPEN"])]["order_id"].tolist()
drop = []
attempt = 0
while len(pending)>0 and attempt<5:
    pending = [j for j in pending if j not in drop]
    for order in pending:
        try:
            CancelOrder(order)
            drop.append(order)
        except:
            print("unable to delete order id : ",order)
            attempt+=1
            