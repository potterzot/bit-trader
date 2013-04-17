#!/usr/bin/env python
"""
Automatic trader for bitfloor.
"""

import sys
import os
import json
from lib import bitfloor
import time
from lib import json_ascii
#import urwid

class api():
    
    def __init__(self, keyfile, exchange):
        self._keyfile = keyfile
        self.exchange = exchange
        self.api = self.getAPI()
        self.orders = []
        self.profit = 0

    def getAPI(self):  
        path = os.path.join(os.path.join(os.path.dirname(__file__), '../keys'), self._keyfile + '.json')
        with open(path) as f:
            config = json.load(f, object_hook=json_ascii.decode_dict)[self.exchange]
        api = bitfloor.RAPI(product_id=1, key=config['key'], secret=config['secret'], passphrase=config['passphrase'])

        return api
    
    def buy(self, price, size):
        order = self.api.buy(size=size, price=price)
        return order.get('order_id')

    def sell(self, price, size):
        order = self.api.sell(size=size, price=price)
        return order.get('order_id')

    def cancel(self, id):
        return self.api.order_cancel(id) 

    def get_ticker(self):
        return self.api.ticker()

    def get_book(self, L=2):
        return self.api.book(L)

    def get_orders(self):
        return self.api.orders()

    def get_assets(self):
        return self.api.accounts()

    def print_book(self):
        book = self.get_book()
        asks = [[float(x), float(y)] for x,y in book['asks']]
        bids = [[float(x), float(y)] for x,y in book['bids']]
        
            #print("%6.2f" % asks[i][0]) # price
            #print("%11.6f" % asks[i][1]) # size
            #print("%6.2f" % (asks[i][0] * asks[i][1])) # value


class safeBot(api):

    def __init__(self, keyfile, exchange):
        bot.__init__(self, keyfile, exchange)
        self.mode = 'safe'

    def run(self):
        self.print_book()
        #orders = self.get_orders()
        #print("%s" % orders)
        #accounts = self.get_accounts()
        #print("%s" % accounts)


class evenBot(api):

    def __init__(self, keyfile, exchange):
        bot.__init__(self, keyfile, exchange)
        self.mode = 'even'
    
    def run(self):
        book = self.get_book()


class riskBot(api):

    def __init__(self, keyfile, exchange):
        bot.__init__(self, keyfile, exchange)
        self.mode = 'risk'
    
    def run(self):
        book = self.get_book()



def main():
    bot1 = safeBot("keys", "bitfloor") # create a new bot
    bot1.run()


if __name__ == '__main__':
    main()



