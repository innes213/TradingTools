'''
Created on July 3, 2016

@author: Rob Innes Hislop
'''

from pyhoofinance import historicdata as h
from pyhoofinance import defs
from datetime import datetime

def market_cap_index_performance(daychanges=[1,2,5,20,100,200]):

    d0 = datetime.today()
    key = defs.LAST_TRADE_PRICE_ONLY_STR
    numdays = max(daychanges) + 1

    smallcapindexdata = [x[key] for x in h.get_number_of_historical_quotes('SLY', numdays, d0)]
    midcapindexdata   = [x[key] for x in h.get_number_of_historical_quotes('MDY', numdays, d0)]
    largecapindexdata = [x[key] for x in h.get_number_of_historical_quotes('SPY', numdays, d0)]

    alldata = [('SLY', smallcapindexdata),
               ('MDY', midcapindexdata),
               ('SPY', largecapindexdata)]

    outstr = 'index | '
    for num in daychanges:
        outstr = outstr + '%i day change\t' % num
    print outstr
    #print 'Index\t\t\t1 day change\t5 day change\t20 day change\t100 day change\t200 day change'
    for idx, data in alldata:
        p0 = data[-1]
        outstr = '  %s | ' % idx
        for daynum in daychanges:
            change = 100 * ( p0 - data[-(daynum + 1)] ) / data[-(daynum + 1)]
            outstr = outstr + '%3.2f%%\t\t' % change
        print outstr

if __name__ == '__main__':
    print '\nMarket Cap index performance:\n'
    market_cap_index_performance()
