from tradingtools.utils.equitydata import get_historic_data_for_symbol, PastQuoteDataKeys
from tradingtools.strategies import get_sma_crossing_trade_signals, model_trades
from tradingtools.utils.equitydata import get_symbol_list
from numpy import max

def sma_crossing_sweep(close_data, max_window=400, trade_delay=1):

    data_length = len(close_data)
    if data_length < num_periods:
        return None
    trials = []
    max_window_size = min([data_length - 1, max_window])
    for window_size in range (3, max_window_size+1):
        trade_vector = get_sma_crossing_trade_signals(close_data, window_size, trade_delay)
        trials.append((window_size, trade_vector))
    return trials

if __name__ == '__main__':
    # TODO: display/capture best over all settings and best best by segments to find trend and correlate to volatility
    MAX_WINDOW = 500
    MAX_PERIODS = 5000
    SEGMENT_SIZE = 20
    STEP_SIZE = 1
    TRADE_ON_CLOSE = False  # Trade on close of period with  otherrwise on following open

    symbols = ['SPY', 'MDY', 'SLY', 'GLD', 'SLV', 'AAPL', 'P', 'GOOG', 'DLB', 'FB', 'ONVO']
    # symbols = get_symbol_list('sp500') + ['SPY', 'MDY', 'SLY', 'GLD', 'SLV']
    # symbols = ['SPY']
    for symbol in symbols:
        data = get_historic_data_for_symbol(symbol, MAX_PERIODS)
        if len(data) < SEGMENT_SIZE:
            break
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in data]
        if TRADE_ON_CLOSE:
            trade_prices = close_data
            trade_delay = 0
        else:
            trade_prices = [x[PastQuoteDataKeys.ADJ_OPEN] for x in data]
            trade_delay = 1
        data = [] # get rid of data we no longer need!

        max_window = min(MAX_WINDOW, len(close_data)-1)
        num_periods = min((len(close_data)-max_window+1), MAX_PERIODS)
        if num_periods < SEGMENT_SIZE:
            break
        print '\nModeling SMA crossing strategy for %s using windows up to %i for %i perionds' % (symbol, max_window, num_periods)
        models = sma_crossing_sweep(close_data, max_window, trade_delay)
        # todo: should these always be on the open?
        buy_price = trade_prices[-num_periods]
        sell_price = trade_prices[-1]
        b_s_delta = sell_price - buy_price
        b_s_percent = 100.0 * b_s_delta / buy_price
        good_results = []
        for window_size, trade_vector in models:
            latest_profit, latest_count = model_trades(trade_prices[-num_periods:], trade_vector[-num_periods:])
            profit_percent = 100.0 * latest_profit / buy_price
            if profit_percent < b_s_percent:
                break
            good_results.append((profit_percent, latest_count, window_size))

        print '\t%i of %i models outperform buy and hold bought @ $%3.2f sold @ $%3.2f (%3.1f%%)' % (len(good_results), len(models), buy_price, sell_price, b_s_percent)
        for profit, count, window in good_results[-5:]:
            print '\twindow = %i yields %3.1f%% with %i transactions' % (window, profit, count)

        # # Examine each model
        # # step through data by STEP_SIZE, looking at SEGMENT_SIZE intervals, getting best settings for each interval
        # n = 0
        # while (n + SEGMENT_SIZE) <= num_periods:
        #     segment_results = []
        #     for window_size, vector in models:
        #         # analyze windows of each vector to determine best settings
        #         profit, count = model_trades(open_data[-(n + SEGMENT_SIZE):(len(open_data) - n - 1)], vector[-(n + SEGMENT_SIZE):(len(vector) - n - 1)])
        #         profit_percent = 100.0 * profit / open_data[-(n+SEGMENT_SIZE)]
        #         segment_results.append((profit_percent, count, window_size))
        #     # sort by profit
        #     segment_results.sort(key=lambda k: k[0])
        #     #output best result
        #     print segment_results[-1]
        #     n += STEP_SIZE
        #     buy_price = open_data[-n]
        #     sell_price = open_data[-(n-SEGMENT_SIZE+1)]
        #     b_s_delta = sell_price - buy_price
        #     b_s_percent = 100.0 * b_s_delta / buy_price
        #     good_results = []
        #     for profit, count, window_size, trade_vector in models:
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
