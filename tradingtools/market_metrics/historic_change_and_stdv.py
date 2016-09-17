'''
Created on July 3, 2016

@author: Rob Innes Hislop
'''
from tradingtools.utils import SymbolList, get_symbol_list

import numpy as np
from pyhoofinance import historicdata as h
from pyhoofinance.defs import *

from datetime import date

def historic_delta_sigma(symbollist, enddate, numdays = 1):
    """
    historic_delta_sigma takes a list of symbols, enddate and numdays
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
            change = historicquotedata[daynum][ADJUSTED_CLOSE_STR] - historicquotedata[daynum - 1][ADJUSTED_CLOSE_STR]
            if change > 0:
                gaincount += 1
            else:
                if change < 0:
                    declinecount += 1
                else:
                    unchangedcount += 1
            if not tradedate:
                tradedate = historicquotedata[daynum][TRADE_DATE_STR]

            volumecount += historicquotedata[daynum][VOLUME_STR]
            percentchangelist.append(100 * change / ((historicquotedata[daynum][ADJUSTED_CLOSE_STR] - change)) )
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

def s_and_p_historic(nday_range=1):
    return historic_delta_sigma(get_symbol_list(SymbolList.SP500), date.today(), numdays=nday_range)


