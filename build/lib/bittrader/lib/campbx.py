import urllib
import base64
import json
import time
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import URLError

class CampBX(object):
    """
    Camp BX API Class
    """
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
        self.base = 'https://campbx.com/api/'
    
    def book(self):
        return self._send_post('xdepth', False)

    def ticker(self):
        response = self._send_post('xticker', False)
        tick = {
            'Buy': response['Best Bid'],
            'Sell': response['Best Ask'],
            'Last': response['Last Trade']
        }
        return tick

    def trades(self):
        self._send_post()

    def history(self):
        self._send_post()

    def buy(self, size, price):
        return order_simple(True, size, price)

    def sell(self, size, price):
        return order_simple(False, size, price) # 0 if filled immediately, otherwise returns order id

    def buy_advanced(self, size, price, filltype='Incremental', darkpool='No', expire=''):
        order_advanced(True, size, price, filltype, darkpool, expire)
        
    def sell_advanced(self, size, price, filltype='Incremental', darkpool='No', expire=''):
        order_advanced(False, size, price, filltype, darkpool, expire)

    def orders(self):
        return self._send_post('myorders', True)

    def margins(self):
        return self._send_post('mymargins', True)

    def send_instant(self, address, amount):
        params = {'CBXCode': address, 'BTCAmt': amount}
        return self._send_post('sendinstant', True, params)

    def send_btc(self, address, amount):
        params = {'BTCTo': address, 'BTCAmt': amount}
        return self._send_post('sendbtc', True, params)

    def order_cancel(self, buyorder, id):
        if buyorder == True:
            params = {'BuyOrderID': id} 
        elif buyorder == False:
            params = {'SellOrderID': id} 
        
        return self._send_post('tradecancel', True, params)

    def order_simple(self, buyorder, size, price):
        if buyorder == True:
            params = {'TradeMode': 'QuickBuy', 'Quantity': size, 'Price': price}
        elif buyorder == False:
            params = {'TradeMode': 'QuickSell', 'Quantity': size, 'Price': price}
        return self._send_post('tradeenter', True, params)

    def order_advanced(self, buyorder, size, price, filltype='Incremental', darkpool='No', expire=''):
        if buyorder == True:
            params = {'TradeMode': 'AdvancedBuy'}
        elif buyorder == False:
            params = {'TradeMode': 'AdvancedSell'}
        
        params.update({ 
            'Quantity': size, #decimal 
            'Price': price, #price can be decimal or 'Market'
            'FillType': filltype, #options are 'Incremental', 'AON', and 'FOK'
            'DarkPool': darkpool, #options are 'No' or 'Yes'
            'Expiry': expire # YYYYMMDD and other formats as well, including relative - no information
            })
        
        return self._send_post('tradeadv', True, params) # returns 0 if filled immediately, otherwise order id
        
    def balances(self):
        return self._send_post('myfunds', True)
    
    def _nonce(self):
        return str(int(time.time()*1e6))
    
    def _send_post(self, endpoint, requires_auth, post_params={}):
        """
        Make a request to the API and return data in a pythonic object
        """
        # setup the url and the request objects
        url = '%s%s.php' % (self.base, endpoint)
        request = Request(url)
        
        post_params.update({'nonce': self._nonce()})
        if requires_auth: #add authentication if the api request requires it
            post_params.update({
                'user': self._username,
                'pass': self._password
            })

        data = urlencode(post_params).encode('utf-8') #encoded parameters for post

        try:
            response = urlopen(request, data)
            return json.loads(response.read().decode('utf-8'))
        except (URLError) as e:
            print('Full error: %s' % e)
            if hasattr(e, 'reason'):
                print('Could not reach host. Reason: %s' % e.reason)
            elif hasattr(e, 'code'):
                print('Could not fulfill request. Error Code: %s' % e.code)
            return None







