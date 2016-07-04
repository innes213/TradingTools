'''
Created on July 3, 2016

@author: Rob Innes Hislop
'''

from datetime import date
import numpy as np
from pyhoofinance import historicdata as h
from pyhoofinance import defs

def historicsigma(symbollist, enddate, numdays = 1):
    """
    historicalsigma takes a list of symbols, enddate and numdays
    returns list of dictionaries containing number of gaining, losing, and total volume)
    """

    quotelist = []
    sigmadata = []
    numquotes = 0

    for symbol in symbollist:
        data = h.get_number_of_historical_quotes(symbol, numdays + 1, enddate)
        if len(data) == numdays + 1:
            quotelist.append(data)
            numquotes += 1

    for daynum in range(1,numdays + 1):
        print daynum
        #Reset analytic data for each day
        gaincount         = 0
        declinecount      = 0
        unchangedcount    = 0
        volumecount       = 0
        percentchangelist = []
        tradedate = None
        daydata = {}

        # for each list of quotes for each symbol, update data for the current day
        for historicquotedata in quotelist:
            change = historicquotedata[daynum][defs.ADJUSTED_CLOSE_STR] - historicquotedata[daynum - 1][defs.ADJUSTED_CLOSE_STR]
            if change > 0:
                gaincount += 1
            else:
                if change < 0:
                    declinecount += 1
                else:
                    unchangedcount += 1
            if not tradedate:
                tradedate = historicquotedata[daynum][defs.TRADE_DATE_STR]

            volumecount += historicquotedata[daynum][defs.VOLUME_STR]
            percentchangelist.append(100 * change / ((historicquotedata[daynum][defs.ADJUSTED_CLOSE_STR] - change)) )
        daydata['gainers'] = gaincount
        daydata['decliners'] = declinecount
        daydata['volume'] = volumecount
        daydata['avgpercentchange'] = np.mean( percentchangelist )
        daydata['percentchangestdev'] = np.std( percentchangelist )
        daydata['tradedate'] = tradedate
        daydata['unchanged'] = unchangedcount
        sigmadata.append(daydata)

    #print numquotes

    return sigmadata

def s_and_p_historic():
    symbollistfile="../symbol_lists/SandP500.csv"

    f = open(symbollistfile)
    symbols = f.read().splitlines()
    f.close()

    print '\nHistoric Change Info for S&P 500\n'

    data = historicsigma(symbols, date.today(), 20)
    for daydata in data:
        outstr = '%12s: '           % str(daydata['tradedate']) + \
                 'Advancers: %5i \t'           % daydata['gainers'] + \
                 'Decliners: %5i \t'           % daydata['decliners'] + \
                 'Average change: %2.2f%% \t'  % daydata['avgpercentchange'] + \
                 'Std Dev: %2.2f%% \t'         % daydata['percentchangestdev'] + \
                 'Total Volume: %i \t'         % int(daydata['volume'])

        print outstr

if __name__ == '__main__':
    s_and_p_historic()

