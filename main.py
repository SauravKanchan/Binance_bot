from binance.client import Client
import sys
try:
    from config import api_key,api_secret
except:
    print("Make config.py\npaste your api_key='<YOUR_KEY>' and api_secret='<YOUR_SECRETE_KEY>'")
    sys.exit()
from binance.websockets import BinanceSocketManager
from binance.enums import *

coin = raw_input('Enter coin to trade(Ex:- BNBBTC ): ')
last_order = raw_input('What was your last order buy/sell: ')
buy_price = raw_input('Enter your buying price: ')
sell_price = raw_input('Enter your selling price: ')
quantity = raw_input('Enter quantity: ')

def process_message(msg):
    # print("message type: {}".format(msg['e']))
    global last_order
    print(msg['p'])
    if msg['p'] <= buy_price and last_order == 'sell':
        print('Buying {0} coins at {1} price'.format(msg['p'],quantity))
        order = client.order_limit_buy(symbol=coin,quantity=quantity,price=buy_price)
        last_order = 'buy'
    elif msg['p'] >= sell_price and last_order == 'buy':
        print('Selling {0} coins at {1} price'.format(msg['p'],quantity))
        order = client.order_limit_sell(symbol=coin,quantity=quantity,price=sell_price)
        last_order = 'sell'
client = Client(api_key, api_secret)

bm = BinanceSocketManager(client)
bm.start_aggtrade_socket(coin, process_message)
bm.start()
