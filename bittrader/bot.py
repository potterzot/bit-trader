import time

from bittrader.api import API

class bot(API):
    """
    Parent Bot class for automated trading. Specific strategies are implemented as a subclass. See simpleBot for example.
    """
    def __init__(self, keyfile, exchange):
       api.__init__(self, keyfile, exchange)
       self.orders = []
       self.profit = 0
       self.basis = 0 #average cost basis = 
       self.positions = self.get_positions()

    def calc_profit(self):
        pass #todo


class simpleBot(bot):
    """
    Simple trading bot. Checks the price and standard deviation of the book every minute, and .
    """

    def __init__(self):
        self.prices = []    
        self.price_avg = 0
        self.price_sd = 0
        self.interval = 20.0 # for campbx, don't make this smaller than 500 milliseconds

    def average_price(self):
        pass

    def run(self):
        """
        Runs the automatic bot.
         
        We want to calculate both the profit (difference in value in USD) due to trading and profit if just buy and hold strategy was employed for comparison.
        """

        while True:
            tick = self.ticker()
            price = float(tick['Last Trade'])
            self.prices.append(price) # add the new price
            

            if len(self.prices) == int((60/self.interval)*60): #keep 1 hour worth of prices
                self.prices.pop(0)

            n_prices = len(prices)
            
            self.price_avg = sum(prices) / n_prices
            self.price_sd = sum([(a-self.price_avg)**2 for a in prices]) / n_prices


            if (criteria == True): # if stats indicate that the bot should buy
                order = self.buy(size, price) 
            
            elif (criteria == True): # if stats indicate that the bot should sell
                order = self.sell(size, price)
            else: # if no action is taken
               pass 

            time.sleep(20.0)

         




