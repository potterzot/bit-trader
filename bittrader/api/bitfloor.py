import hmac
import hashlib
import base64
import urllib
from http.client import HTTPSConnection as HTTPConn
import time
import json
import copy
from decimal import Decimal
import decimal
import os
import sys

config_file = os.path.join(os.path.dirname(__file__), 'config.json')

with open(config_file) as f:
    config = json.load(f)['bitfloor']

class BitFloor(object):
    """
    Bitfloor API Class
    """
    def __init__(self, product_id, key, secret, passphrase):
        self._api_version = 1
        self._host = config['host']
        self._data_port = config['data_port']
        self._order_port = config['order_port']
        self._key = key
        self._secret = secret.encode()
        self._passphrase = passphrase
        self._product_id = product_id
        self._inc = Decimal('0.01') # TODO: get from bitfloor

    def book(self, level=1):
        url = '/book/L{1}/{0}'.format(self._product_id, level)
        return self._send_get(url)

    def ticker(self):
        url = '/ticker/{0}'.format(self._product_id)
        return self._send_get(url)

    def trades(self):
        url = '/trades/{0}'.format(self._product_id)
        return self._send_get(url)

    def order_new(self, side, size, price):
        return self._send_post('/order/new', {
            'product_id': self._product_id,
            'side': side,
            'size': size,
            'price': price
        })

    def buy(self, **kwargs):
        return self.order_new(side=0, **kwargs)

    def sell(self, **kwargs):
        return self.order_new(side=1, **kwargs)

    def order_cancel(self, order_id):
        return self._send_post('/order/cancel', {
            'product_id': self._product_id,
            'order_id': order_id
        })

    def orders(self):
        return self._send_post('/orders')

    def accounts(self):
        return self._send_post('/accounts')

    def floor_inc(self, n):
        return (Decimal(str(n))/self._inc).quantize(Decimal('1'), rounding=decimal.ROUND_DOWN)*self._inc

    def ceil_inc(self, n):
        return (Decimal(str(n))/self._inc).quantize(Decimal('1'), rounding=decimal.ROUND_UP)*self._inc

    def round_inc(self, n):
        return (Decimal(str(n))/self._inc).quantize(Decimal('1'))*self._inc

    def _send_get(self, url, payload={}):
        body = urllib.parse.urlencode(payload)
        conn = HTTPConn(self._host, self._data_port)
        conn.request("GET", url, body)
        resp = conn.getresponse()
        s = resp.read().decode() # comes as a bytes-type object, decode to string
        conn.close()
        print(s)
        return json.loads(s)

    def _send_post(self, url, payload={}):
        payload = copy.copy(payload) # avoid modifying the original dict

        # add some stuff to the payload
        payload['nonce'] = int(time.time()*1e6)

        body = urllib.parse.urlencode(payload).encode() # convert to bytes object

        sig = hmac.new(base64.b64decode(self._secret), body, hashlib.sha512).digest()
        sig_b64 = base64.b64encode(sig)

        headers = {
            'bitfloor-key': self._key,
            'bitfloor-sign': sig_b64,
            'bitfloor-passphrase': self._passphrase,
            'bitfloor-version': self._api_version,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': len(body)
        }

        conn = HTTPConn(self._host, self._order_port)
        conn.request("POST", url, body, headers)
        resp = conn.getresponse()
        s = resp.read().decode() # comes as a bytes object, decode to a string
        conn.close()
        return json.loads(s)

