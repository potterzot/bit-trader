#!/usr/bin/env python
"""
Automatic trader for bitfloor.
"""

import sys
import os
import json
import time
#import urwid
from bittrader.lib import BitFloor, MtGox, CampBX, BitCE

class API():
    """
    Standardized API interface for multiple exchanges providing functions to interface with an exchange using the same function and variable names.
    """
    def __init__(self, keyfile, exchange):
        self._keyfile = keyfile
        self.exchange = exchange
        self.api = self.getAPI()

    def getAPI(self):  
        path = os.path.join(os.path.join(os.path.dirname(__file__), '../keys'), self._keyfile)
        with open(path) as f:
            config = json.load(f)[self.exchange]

        if self.exchange == "bitfloor":
            api = BitFloor(product_id=1, key=config['key'], secret=config['secret'], passphrase=config['passphrase'])
        elif self.exchange == "mtgox":
            api = MtGox(key=config['key'], secret=config['secret'])
        elif self.exchange == "campbx":
            api = CampBX(username=config['username'], password=config['password'])
        elif self.exchange == "bitce":
            api = BitCE(key=config['key'], secret=config['secret'])

        else:
            pass
        return api
    
    def buy(self, price, size):
        order = self.api.buy(size=size, price=price)
        return order.get('order_id')

    def sell(self, price, size):
        order = self.api.sell(size=size, price=price)
        return order.get('order_id')

    def cancel(self, id):
        return self.api.order_cancel(id) 

    def ticker(self):
        return self.api.ticker()

    def book(self):
        return self.api.book()

    def orders(self):
        return self.api.orders()

    def balance(self):
        return self.api.balances()

