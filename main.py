from binance.client import Client
import sys
try:
    from config import api_key,api_secret
except:
    print("Make config.py\npaste your api_key='<YOUR_KEY>' and api_secret='<YOUR_SECRETE_KEY>'")
    sys.exit()
from binance.websockets import BinanceSocketManager
from binance.enums import *


def process_message(msg):
    # print("message type: {}".format(msg['e']))
    global last_order
    print(msg['p'])
    if msg['p'] <= buy_price and last_order == 'sell':
        print('Buying {1} coins at {0} price'.format(msg['p'],quantity))
        order = client.order_limit_buy(symbol=coin,quantity=quantity,price=msg['p'])
        last_order = 'buy'
    elif msg['p'] >= sell_price and last_order == 'buy':
        print('Selling {1} coins at {0} price'.format(msg['p'],quantity))
        order = client.order_limit_sell(symbol=coin,quantity=quantity,price=msg['p'])
        last_order = 'sell'
def average_price(prices):
    total = 0
    for i in prices:total+=float(i['p'])
    return total/len(prices)

client = Client(api_key, api_secret)

coin = input('Enter coin to trade(Ex:- BNBBTC ): ')
prices = client.get_aggregate_trades(symbol=coin)
print("Current average price of",coin,"is",average_price(prices))
print("Last price of",coin,"is",prices[-1]['p'])

last_order = input('What was your last order buy/sell: ')
buy_price = input('Enter your buying price: ')
sell_price = input('Enter your selling price: ')
quantity = input('Enter quantity: ')
print("Profit margin: ",(((int(sell_price)-int(buy_price))/int(buy_price))*100),"%")

bm = BinanceSocketManager(client)
bm.start_aggtrade_socket(coin, process_message)
bm.start()
