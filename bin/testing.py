#!/usrbin/env python

from bittrader.api import API
from bittrader.lib.mtgox import MtGox
from bittrader.lib.campbx import CampBX
from bittrader.lib.bitce import BitCE

keyfile = '/home/potterzot/git/bittrader/keys/keys.json'

apigox = API(keyfile, 'mtgox')
apibx  = API(keyfile, 'campbx')
apice  = API(keyfile, 'bitce')

gox = MtGox(apigox.api._key, apigox.api._secret)
bx  = CampBX(apibx.api._username, apibx.api._password)
ce  = BitCE(apice.api._key, apice.api._secret)





