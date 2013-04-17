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


License
=======

`MIT License <http://www.opensource.org/licenses/mit-license.php>`_

Copyright (c) 2011 Glen Zangirolami

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject 
to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.







