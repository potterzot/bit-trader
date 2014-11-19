==========
Bit Trader
==========

About
=====
A Python 3 package that provides standardized APIs to trade on the following exchanges:

`Bitfloor <http://www.bitfloor.com>, (API Documentation <https://bitfloor.com/docs/api>)`
`Mt Gox <http://www.mtgox.com>, (API Documentation <https://mtgox.com/api>)`
`CampBX <http://www.campbx.com>, (API Documentation <https://campbx.com/api.php>)`

Includes a curses interface for trading in addition to packages that allow for use in python scripts to employ automated trading strategies.


Installation
============

``pip install bittrader``


Documentation
=============


Usage
=====

API Keys must be added to the file located at "./keys/keys.json"

Initializing the API::
    
    import bittrader as bt
    trader = bt.platform(keys, exchange)


Donations
=========
If you find this software useful please donate to: 17GRViZR6kqcTpHJrh1e7eEsZkvngUtaZK

