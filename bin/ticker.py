#!/usr/bin/env python
from bittrader.api import API
from bittrader.lib.mtgox import MtGox
from bittrader.lib.campbx import CampBX
from bittrader.lib.bitce import BitCE
from matplotlib import pyplot as plt
import pandas
import time
import csv
import numpy as np



datafile = 'prices.csv'
keyfile = '/home/potterzot/git/bittrader/keys/keys.json'
delay = 5.0


mtgox = API(keyfile, 'mtgox')
campbx  = API(keyfile, 'campbx')
bitce  = API(keyfile, 'bitce')


def analyze():
    """Analyzes prices at exchanges to see if one follows the other."""
    # load the data file to numpy array / data frame
    data = np.genfromtxt(datafile, delimiter=',', names=True)
    
    print(data)
    df = pandas.DataFrame(data)

    # graph the data
    try:
        plot(df['time'], df['mtgox'])
        plot(df['time'], df['campbx'])
        plot(df['time'], df['bitce'])
        show()
    except:
        print("Couldn't plot.")

    return data

def loop():
    """Gets the ticker from each exchange and saves the data."""
    
    i = 0
    n = 1
    
    f = open(datafile, 'w')
    f.write('time,mtgox,campbx,bitce,\n') #headers
    f.close()
    
    f = open(datafile, 'a')
     
    
    while True:
        i+=1
        goxtick = mtgox.ticker()
        bxtick = campbx.ticker()
        cetick = bitce.ticker()
        
        price = []
        price.append(i)
        price.append(float(goxtick['Last']))
        price.append(float(bxtick['Last']))
        price.append(float(cetick['Last']))
        
        [f.write(str(x)+',') for x in price]
        f.write('\n')
        
        if i == ((100/delay)*n):
            f.close()
            data = analyze()    
            f = open(datafile, 'a')
            n+=1
        
        time.sleep(delay)
        
    f.close()
    return

if __name__ == '__main__':
    loop()






