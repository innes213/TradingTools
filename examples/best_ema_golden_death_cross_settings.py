from tradingtools.equitydata import get_historic_data_for_symbol, PastQuoteDataKeys
from tradingtools.technicals.strategies import ema_golden_death_cross_sweep

if __name__ == '__main__':

    #symbols = ['SPY'] #, 'MDY', 'SLY', 'GLD', 'SLV', 'AAPL', 'P', 'GOOG', 'DLB']
    # symbols = get_symbol_list('sp500')[-10:]
    symbols = ['SPY', 'MDY', 'SLY', 'GLD', 'SLV']
    for symbol in symbols:
        data = get_historic_data_for_symbol(symbol, 5000)
        open_data = [x[PastQuoteDataKeys.ADJ_OPEN] for x in data]
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in data]
        data = [] # get rid of data we no longer need!

        periods = [10, 20, 50, 100, 250, 500, 1000, 2000]
        #periods = [10]
        for num_periods in periods:
            if len(close_data) > num_periods:
                results = ema_golden_death_cross_sweep(open_data, close_data, num_periods)
                results.sort(key=lambda k: k[0], reverse=True)
                buy_price = close_data[-num_periods]
                sell_price = open_data[-1]
                b_s_delta = sell_price - buy_price

                print '%s Window Settings that beat buy-and-hold for the past %i days:' % (symbol, num_periods)
                print 'Total Trials: %i' % len(results)
                for profit, slow, fast, count in results[:3]:
                    if b_s_delta < profit and count > 0:
                        print '\tfast = %i, slow = %i yields $%3.2f with %i transactions' % (fast, slow, profit, count)

                print 'Buy and hold yielded: $%3.2f ($%3.2f - $%3.2f)\n' % (b_s_delta, sell_price, buy_price)
