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
class BitCE(object):
    """
    BitC-E API Class. Most calls support the following options:
        from = order number to start displaying with (default is 0)
        count = number of orders for displaying (default is 1000)
        from_id = first order id to select for (default is 0)
        end_id = last order id to select for (default is all)
        order = sorting "ASC" or "DESC" (default is "DESC")
        since = start time to select orders for (default is 0)
        end = end time to select orders from (default is all)
        pair = all, currency pairing to find orders for (btc_usd).
        active = 0/1, display active orders only
    """
    def __init__(self, key, secret):
        self.base = 'https://btc-e.com/tapi'
        self.public_base = 'https://btc-e.com/api/2/'
        self.pair = 'btc_usd'
        self._key = key 
        self._secret = secret
        self.content_type = 'application/x-www-form-urlencoded'

    def book(self, pair='btc_usd'):
        response = self._send_public(pair=pair, path='depth')
        book = {}
        book['Asks'] = [[[x[0], x[1]] for x in response['asks']]]
        book['Bids'] = [[[x[0], x[1]] for x in response['bids']]]
        return book

    def ticker(self, pair='btc_usd'):
        response = self._send_public(pair=pair, path='ticker')
        data = {
            'Average': response['ticker']['avg'],
            'Last': response['ticker']['last'],
            'Buy': response['ticker']['buy'],
            'Sell': response['ticker']['sell'],
            'High': response['ticker']['high'],
            'Low': response['ticker']['low'],
            'Volume': response['ticker']['vol'],
            'Volume Cur': response['ticker']['vol_cur'],
            'Now': response['ticker']['server_time']
        }
        return data

    def all_trades(self, pair='btc_usd'):
        response = self._send_public(pair=pair, path='ticker')
        data = response
        return data

    def buy(self, **kwargs):
        """Issue a buy order for a currency pair (default is BTC for USD)."""
        return self.order(order_type='buy', **kwargs)

    def sell(self, **kwargs):
        """Issue a sell order for a currency pair (defualt is BTC for USD)."""
        return self.order(order_type='sell', **kwargs)

    def order(self,  **kwargs):
        params = {'method':'Trade'}
        params.update(kwargs)
        return self._send_post(params)

    def order_cancel(self, oid):
        """Cancel and order with the given order id."""
        params = {'method':'CancelOrder', 'order_id': oid}
        return self._send_post(params)

    def orders(self, **kwargs):
        """Returns a list of orders."""
        params = {'method':'OrderList'}
        params.update(kwargs)
        return self._send_post(params)
        
    def trades(self, **kwargs):
        """Returns a list of trades."""
        params = {'method':'TradeHistory'}
        params.update(kwargs)
        return self._send_post(params)
    
    def balances(self):
        """Returns current account balances for all fiat and coins."""
        params = {'method':'getInfo'}
        response = self._send_post(params)
        balances = response['return']['funds']
        return balances

    def info(self):
        """Returns some basic info on the account."""
        params = {'method':'getInfo'}
        return self._send_post(params)

    def _nonce(self):
        return str(int(time.time()))

    def _make_request(self, data):
        bsecret = self._secret.encode('ascii')
        sign = HMAC(bsecret, digestmod=sha512)
        sign.update(data.encode('ascii'))
    
        header = {
            'Content-type': self.content_type,
            'Key': self._key,
            'Sign': sign.hexdigest()
        }
        
        return Request(self.base, data, header)
    
    def _send_public(self, pair, path):
        """Returns a json object from a requested public API path."""
        if pair in ['btc_usd', 'ltc_btc', 'ltc_usd']:
            url = self.public_base + pair + "/" + path
            request = Request(url)
            try:
                response = urlopen(request)
                data = json.loads(response.read().decode('ascii'))
                return data
            except:
                print("Connection Error" % e)
        else:
            print('%s is not a valid currency pair.' % pair)

    def _send_post(self, post_params = {}):
        """Make a request to the API and return data in a pythonic object"""
        post_params.update({'nonce': self._nonce()})
        data = urlencode(post_params) # url encoding of post parameters
        request = self._make_request(data)

        try:
            response = urlopen(request, data.encode('utf-8'))
            data = json.loads(response.read().decode('utf-8'))
            if data['success'] == 1:
                return data['return']
            else:
                return 'Error %s' % data['error']
        except (URLError) as e:
            print('Full error: %s' % e)
       

