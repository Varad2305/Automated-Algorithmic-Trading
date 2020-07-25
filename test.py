import pandas as pd
import requests
import sys

def getMultiplier(tradingsymbol):
    print("TRADING SYMBOL:",tradingsymbol)
    url = "https://api.kite.trade/margins/equity"
    response = requests.get(url)
    response_json = response.json()
    print(response_json[tradingsymbol])
    return response_json['tradingsymbol' == tradingsymbol]['mis_multiplier']

print(getMultiplier(sys.argv[1]))