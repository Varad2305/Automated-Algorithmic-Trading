from kiteconnect import KiteConnect
import os

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


# Fetch quote details
quote = kite.quote("NSE:INFY")

# Fetch last trading price of an instrument
ltp = kite.ltp("NSE:INFY")

# Fetch order details
orders = kite.orders()

# Fetch position details
positions = kite.positions()

# Fetch holding details
holdings = kite.holdings()
