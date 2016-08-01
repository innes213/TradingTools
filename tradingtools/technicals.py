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
