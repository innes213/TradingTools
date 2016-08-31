from tradingtools.market_metrics.market_cap_index_performance import market_cap_index_performance
from tradingtools.market_metrics.historic_change_and_stdv import s_and_p_historic
from tradingtools.market_metrics.sector_performance import sector_performance
from tradingtools.technicals import price_sma_for_symbol
from pyhoofinance.defs import *
from pyhoofinance.quotedata import get_quote

if __name__ == '__main__':
    day_ranges = [1, 2, 5, 10, 20, 100, 200, 500]
    print '\n================= S&P Dashboard =================\n'
    print '\nMarket Cap index performance:\n'
    data = market_cap_index_performance(dayranges=day_ranges)
    if data is not None:
        outstr = 'Index\t'
        for i in day_ranges:
            outstr = outstr + str(i) + '-day\t'
        print outstr
        for idx, perf_list in data:
            outstr = '%s: \t' % idx
            for perf in perf_list:
                outstr = outstr + '%5.2f%%\t' % (100 * perf)
            print outstr

    print '\nSummary of price changes\n'
    data = s_and_p_historic(1)
    for daydata in data:
        outstr = '%12s: ' % str(daydata['tradedate']) + \
                 'Advancers: %5i \t'           % daydata['gainers'] + \
                 'Decliners: %5i \t'           % daydata['decliners'] + \
                 'Average change: %2.2f%% \t'  % daydata['avgpercentchange'] + \
                 'Std Dev: %2.2f%% \t'         % daydata['percentchangestdev'] + \
                 'Total Volume: %i \t'         % int(daydata['volume'])

    print outstr

    print '\nS & P Sector Performance\n'
    data = sector_performance(day_ranges)
    if data is not None:
        outstr = 'Sector'
    for i in day_ranges:
        outstr = outstr + '\t%i-day' % i
    print outstr

    for symbol, perf_data in data:
        outstr = '%s:' % symbol
        for perf in perf_data:
            outstr = outstr + '\t%3.2f%%' % (100 * perf)
        print outstr

    # Sector Rotation triggers
    print '\nS & P Sector Rotation\n'

    spyquote = get_quote('SPY')
    spylast = spyquote[LAST_TRADE_PRICE_ONLY_STR]
    d0 = spyquote[LAST_TRADE_DATE_STR]
    #[TODO: replace number of days with 1 month and 1 year
    # get S&P 500 1 year performance and moving average
    spymadays = 240 # values greater than 36 diverge from yahoo and etrade sma calculations
    spysma = price_sma_for_symbol('SPY',window_size=spymadays)[0]

    spymadelta = 100 * (spylast - spysma) / spysma
    num_days = 22
    data = sector_performance(num_days)
    print d0.strftime('As of %d %b, %Y')
    print 'SPY difference from %i moving average: %3.2f%% ' % (spymadays, spymadelta)
    print '%i-Day Performance' % num_days
    for symbol, perf in data:
        print '%s: %3.2f%%' % (symbol, 100 * perf)