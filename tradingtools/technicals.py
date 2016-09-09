from pyhoofinance.historicdata import get_number_of_historical_quotes
from pyhoofinance import defs

import numpy as np

from datetime import datetime

def _get_last_price_list(historic_data):
    return [x[defs.LAST_TRADE_PRICE_ONLY_STR] for x in historic_data]

def sma(historic_data, window_size=20):
    """
    Calculates the simple moving average for day_range days over historic data
    :param historic_data: List of floats representing past data (price, volume, etc)
    :param day_range: number of days to average over
    :return: List of floats representing the averages
    """
    if len(historic_data) < window_size:
        print 'Window size exceeds length of data!'
        return []
    return [np.mean(historic_data[n:n+window_size]) for n in range(len(historic_data) - window_size + 1)]

def price_sma_for_symbol(symbol, num_days=1, window_size=20, enddate=datetime.today()):
    """
    Simple moving price average across day_range days for numdays
    :param symbol:
    :param num_days: number of days for which average is calculated
    :param window_size: days to average across
    :param enddate:
    :return: List of floats
    """
    historic_data = get_number_of_historical_quotes(symbol, num_days + window_size - 1, enddate)
    return sma(_get_last_price_list(historic_data), window_size)

def _calculate_ema(current_value, k, last_ema):
    return current_value * k + last_ema * (1 - k)


def ema(historic_data, window_size=16):
    if len(historic_data) <= window_size:
        # todo: make this an exception
        print 'Not enough data to calulate ema!'
        return []

    if len(historic_data) < 6 * window_size:
        print 'Warn: EMA may not have enouugh history to be valid'

    i = 0
    last_ema = 0
    ema_data = []
    k = 2.0 / (window_size + 1)
    for current_value in historic_data:
        ema_data.append(_calculate_ema(current_value, k, last_ema))
        last_ema = ema_data[i]
        i = i + 1

    return ema_data

def price_ema_for_symbol(symbol, num_days=1, window_size=22, enddate=datetime.today()):
    historic_data = get_number_of_historical_quotes(symbol, np.max([5 * window_size, window_size + num_days - 1]), enddate)
    return ema(_get_last_price_list(historic_data))[-num_days:]

def macd(historic_data, slow_window=26, fast_window=12, signal_window=9):
    delta = np.subtract(ema(historic_data, fast_window), ema(historic_data, slow_window))
    signal = ema(delta, signal_window)
    histogram = np.subtract(delta, signal)
    return delta, signal, histogram

def price_macd_for_symbol(symbol, num_days=1, slow_window=26, fast_window=12, signal_window=9, enddate=datetime.today()):
    historic_data = get_number_of_historical_quotes(symbol, np.max([6 * slow_window, slow_window + num_days - 1]), enddate)
    price_data = _get_last_price_list(historic_data)
    delta, signal, histogram = macd(price_data, slow_window, fast_window, signal_window)
    return delta[-num_days:], signal[-num_days:], histogram[-num_days:]

def performance(historic_data, day_ranges=1):
    """
    Calculates the performance (most recent - reference)/reference
    :param historic_data: array of historic quote data
    :param day_ranges: int or list of day ranges to calculate across
    :return: Int or List (depending on day_ranges) of performance for each number of ays in numdays
    """
    price_list = _get_last_price_list(historic_data)  # sorted oldest to newest data
    if type(day_ranges) is int:
        return (price_list[-1] - price_list[-(day_ranges + 1)]) / price_list[-(day_ranges + 1)]
    return [(price_list[-1] - price_list[-(n+1)])/price_list[-(n + 1)] for n in day_ranges]

def performance_for_symbol(symbol, day_ranges=1):
    """
    Calculates the price performance of a symbol across one or more day ranges
    :param symbol: String representing ticker symbol
    :param day_ranges: Int or List of day ranges
    :return: Float or List of floats (depending on day_ranges)
    """
    if type(day_ranges) is int:
        num_days = day_ranges + 1
    else:
        num_days = max(day_ranges) + 1
    historic_data = get_number_of_historical_quotes(symbol, num_days)
    return performance(historic_data, day_ranges)

def is_doji():
    pass

if __name__ == '__main__':
    print '\nGOOGL 1, 5, 100 day performance'
    for x in performance_for_symbol('GOOGL', [1, 5, 100]):
        print '%3.2f%%' % (x * 100)
    print '\nGOOGL SMA'
    for s in price_sma_for_symbol('GOOGL'):
        print '$%3.2f' % s
