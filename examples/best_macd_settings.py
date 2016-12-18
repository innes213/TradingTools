from tradingtools.utils.equitydata import get_historic_data_for_symbol, PastQuoteDataKeys
from tradingtools.strategies import get_macd_crossing_trade_signals, model_trades
from tradingtools.utils.equitydata import get_symbol_list
from numpy import max

def macd_crossing_sweep(open_data, close_data, num_periods, max_window=400):

    data_length = len(open_data)
    if data_length < num_periods:
        return None
    trials = []
    max_window_size = min([data_length / 6, max_window])
    for signal_window in range (3, max_window_size / 8):
        for fast_window in range(signal_window + 1, signal_window * 2):
            for slow_window in range(fast_window + 1, fast_window * 4):
                trade_vector = get_macd_crossing_trade_signals(close_data, slow_window, fast_window, signal_window, num_periods)
                trials.append((slow_window, fast_window, signal_window, trade_vector))
    return trials

if __name__ == '__main__':
    MAX_WINDOW = 200
    MAX_PERIODS = 1000
    SEGMENT_SIZE = 20
    STEP_SIZE = 1

    # symbols = ['SPY'] #, 'MDY', 'SLY', 'GLD', 'SLV', 'AAPL', 'P', 'GOOG', 'DLB']
    # symbols = get_symbol_list('sp500') + ['SPY', 'MDY', 'SLY', 'GLD', 'SLV']
    symbols = ['SPY']
    for symbol in symbols:
        data = get_historic_data_for_symbol(symbol, 5000)
        if len(data) < SEGMENT_SIZE:
            break
        print '\nMACD Crossing trials for %s (%i days of data):' % (symbol, len(data))
        open_data = [x[PastQuoteDataKeys.ADJ_OPEN] for x in data]
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in data]
        data = [] # get rid of data we no longer need!

        max_window = min(MAX_WINDOW, len(open_data) / 6)
        num_periods = min((len(open_data) - 5 * max_window), MAX_PERIODS)
        if num_periods < SEGMENT_SIZE:
            break
        models = macd_crossing_sweep(open_data, close_data, num_periods, max_window)
        # step through data by STEP_SIZE, looking at SEGMENT_SIZE intervals, getting best settings for each interval
        n = 0
        while (n + SEGMENT_SIZE) <= num_periods:
            segment_results = []
            for slow, fast, signal, vector in models:
                # analyze windows of each vector to determine best settings
                profit, count = model_trades(open_data[-(n + SEGMENT_SIZE):(len(open_data) - n - 1)], vector[-(n + SEGMENT_SIZE):(len(vector) - n - 1)])
                profit_percent = 100.0 * profit / open_data[-(n+SEGMENT_SIZE)]
                segment_results.append((profit_percent, count, slow, fast, signal))
            segment_results.sort(key=lambda k: k[0])
            print segment_results[-1]
            n += STEP_SIZE
        #     buy_price = open_data[-n]
        #     sell_price = open_data[-(n-SEGMENT_SIZE+1)]
        #     b_s_delta = sell_price - buy_price
        #     b_s_percent = 100.0 * b_s_delta / buy_price
        #     good_results = []
        #     for profit, count, slow_window, fast_window, signal_window, trade_vector in models:
        #         if len(trade_vector) > SEGMENT_SIZE:
        #             latest_profit, latest_count = model_trades(open_data[-SEGMENT_SIZE:], trade_vector[-SEGMENT_SIZE:])
        #             profit_percent = 100.0 * latest_profit / buy_price
        #             if profit_percent < b_s_percent:
        #                 break
        #             good_results.append((profit_percent, latest_count, slow_window, fast_window, signal_window, trade_vector))
        #
        # print '\t%i of %i models outperform buy and hold (%3.1f%%)' % (len(good_results), len(models), b_s_percent)
        # for profit, count, slow, fast, signal, _ in good_results[-5:]:
        #     print '\tslow = %i, fast = %i, signal = %i yields %3.1f%% with %i transactions' % (slow, fast, signal, profit, count)
