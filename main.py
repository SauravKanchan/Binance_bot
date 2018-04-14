from binance.client import Client
import sys
try:
    from config import api_key,api_secret
except:
    print("Make config.py\npaste your api_key='<YOUR_KEY>' and api_secret='<YOUR_SECRETE_KEY>'")
    sys.exit()
client = Client(api_key, api_secret)
depth = client.get_order_book(symbol='BNBBTC')
print(depth)
