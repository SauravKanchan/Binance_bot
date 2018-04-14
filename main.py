from binance.client import Client
import sys
try:
    from config import api_key,api_secret
except:
    print("Make config.py\npaste your api_key='<YOUR_KEY>' and api_secret='<YOUR_SECRETE_KEY>'")
    sys.exit()
from binance.websockets import BinanceSocketManager
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
import os

orders = []
def process_message(msg):
    # print("message type: {}".format(msg['e']))
    # global orders,buy_price,sell_price
    os.system('clear')
    print('Trading:',coin)
    print('Quantity:',quantity)
    print('Buying price:',buy_price)
    print('Selling price:',sell_price)
    print('Current price: ',msg['p'])
    for i in orders:print(i)

    if msg['p'] <= buy_price :
        try:
            order = client.order_limit_buy(symbol=coin,quantity=quantity,price=msg['p'])
            orders.append('Bought {1} coins at {0} price'.format(msg['p'],quantity))
        except:
            # print(e.message)
            pass
    elif msg['p'] >= sell_price:
        try:
            order = client.order_limit_sell(symbol=coin,quantity=quantity,price=msg['p'])
            orders.append('Sold {1} coins at {0} price'.format(msg['p'],quantity))
        except:
            # print(e.message)
            pass
def average_price(prices):
    total = 0
    for i in prices:total+=float(i['p'])
    return total/len(prices)

client = Client(api_key, api_secret)

coin = input('Enter coin to trade(Ex:- BNBBTC ): ')
prices = client.get_aggregate_trades(symbol=coin)
print("Current average price of",coin,"is",average_price(prices))
print("Last price of",coin,"is",prices[-1]['p'])
buy_price = input('Enter your buying price: ')
sell_price = input('Enter your selling price: ')
quantity = input('Enter quantity: ')

profit=(((float(sell_price)-float(buy_price))/float(buy_price))*100)
if profit<=0.2:
    choice = input('Do you want to continue as profit is less than 0.2%')
    if choice == "no":
        sys.exit()
print("Profit margin: ",profit,"%")

bm = BinanceSocketManager(client)
bm.start_aggtrade_socket(coin, process_message)
bm.start()
