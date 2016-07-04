from pyhoofinance import historicdata as h
from pyhoofinance import quotedata as q
from pyhoofinance import defs
from numpy import mean as nmean

def sector_performance():
    print '\nS & P Sector performance\n'
    symbollistfile="../symbol_lists/SPDRSectorSelects.csv"
    f = open(symbollistfile)
    symbols = f.read().splitlines()
    f.close()

    spyquote = q.get_quote('SPY')
    spylast = spyquote[defs.LAST_TRADE_PRICE_ONLY_STR]
    d0 = spyquote[defs.LAST_TRADE_DATE_STR]

    #[TODO: replace number of days with 1 month and 1 year]
    historicnumdays = 22
    # get S&P 500 1 year performance and moving average
    spymadays = 240 # values greater than 36 diverge from yahoo and etrade sma calculations
    spydata = h.get_number_of_historical_quotes('SPY', spymadays, d0)
    spysma = nmean([x[defs.LAST_TRADE_PRICE_ONLY_STR] for x in spydata])

    spymadelta = 100 * (spylast - spysma) / spysma

    # get 1 month performance for SPDR sector etfs
    quotes = q.get_quotes(symbols)
    for quote in quotes:
        # get most recent quote
        last = quote[defs.LAST_TRADE_PRICE_ONLY_STR]
        # Get quote from
        past = h.get_number_of_historical_quotes(quote[defs.SYMBOL_STR], historicnumdays, d0)[0][defs.LAST_TRADE_PRICE_ONLY_STR]
        quote['performance'] = 100 * (last - past)/past

    print d0.strftime('As of %d %b, %Y')
    print 'SPY difference from %i moving average: %3.2f%% ' % (spymadays, spymadelta)
    quotes = sorted(quotes, key = lambda k: k['performance'],reverse = True)
    print 'Sector %i day performance:' % historicnumdays

    for quote in quotes:
        print '\t' + quote[defs.SYMBOL_STR] + ': %3.2f%%' % quote['performance']

if __name__ == '__main__':
    sector_performance()