import base64
import time
import contextlib
import math
import datetime
import json
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import URLError
from hashlib import sha512
from hmac import HMAC

# Use this class to interact with Mt.Gox API
class MtGox(object):
    """
    Mt Gox API Class.
    """
    def __init__(self, key, secret):
        self.base = 'https://data.mtgox.com/api/2/'
        self._key = key 
        self._secret = secret
        self.agent = 'MtGox API'

    def book(self):
        response = self._send_post('BTCUSD/money/depth/fetch')
        book = {}
        book['Asks'] = [[[x['price'], x['amount']] for x in response['asks']]]
        book['Bids'] = [[[x['price'], x['amount']] for x in response['bids']]]
        return book

    def ticker(self):
        response = self._send_post('BTCUSD/money/ticker')
        tick = {
            'Average': response['avg']['value'],
            'Buy': response['buy']['value'],
            'Sell': response['sell']['value'],
            'High': response['high']['value'],
            'Low': response['low']['value'],
            'Volume': response['vol']['value'],
            'VWAP': response['vwap']['value'],
            'Last': response['last']['value'],
            'Now': response['now']
            }
        return tick

    def buy(self, size, price):
        return self.order(order_type='bid', size=size, price=price)

    def sell(self, size, price):
        return self.order(order_type='ask', size=size, price=price)

    def quote(self, order_type, size):
        """Provides a quote of the price for an order of a given size."""
        size_int = int(size*1e8)
        params = {'type': order_type, 'amount': size_int}
        return self._send_post('BTCUSD/money/order/quote', params)

    def order(self, order_type, size, price=None):
        size_int = int(size*1e8)
        if price:
            price_int = int(price*1e5)
        else:
            price_int = None

        params = {'type': order_type,
            'amount_int': size_int,
            'price_int': price_int
        }
        return self._send_post('BTCUSD/money/order/add', params)

    def order_cancel(self, oid):
        return self._send_post('BTCUSD/money/order/cancel', {'oid': oid})

    def orders(self):
        return self._send_post('BTCUSD/money/orders')
        
    def all_trades(self):
        return self._send_post('BTCUSD/money/trades/fetch')
    
    def balances(self):
        response = self._send_post('BTCUSD/money/info')

    def info(self):
        return self._send_post('BTCUSD/money/info')

    def _nonce(self):
        return str(int(time.time()*1e6))

    def _make_request(self, path, data):
        hash_data = (path + chr(0) + data).encode()
        bsecret = base64.b64decode(self._secret)
        sign = HMAC(bsecret, hash_data, sha512).digest()

        header = {
            'User-Agent': self.agent,
            'Rest-Key': self._key,
            'Rest-Sign': base64.b64encode(sign)
            # 'Accept-Encoding': 'GZIP'
        }
        
        return Request(self.base+path, data, header)
    

    def _send_post(self, path, post_params = {}):
        """
        Make a request to the API and return data in a pythonic object
        """
        post_params.update({'nonce': self._nonce()})
        data = urlencode(post_params) # url encoding of post parameters

        request = self._make_request(path, data)

        try:
            response = urlopen(request, data.encode('utf-8'))
            data = json.loads(response.read().decode('utf-8'))
            if data['result'] == 'success':
                return data['data']
            else:
                return 'Error'
        except (URLError) as e:
            print('Full error: %s' % e)
       

