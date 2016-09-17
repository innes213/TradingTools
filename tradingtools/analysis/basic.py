from tradingtools.utils import get_historic_data_for_symbol
from pyhoofinance.defs import *

from datetime import datetime

def _get_data_by_key(data, key):
    return [x[key] for x in data]

def performance(data, day_ranges=1):
    """
    Calculates the performance (most recent - reference)/reference
    :param historic_data: array of historic quote data
    :param day_ranges: int or list of day ranges to calculate across
    :return: Int or List (depending on day_ranges) of performance for each number of ays in numdays
    """
    if type(day_ranges) is int:
        return (data[-1] - data[-(day_ranges + 1)]) / data[-(day_ranges + 1)]
    return [(data[-1] - data[-(n+1)])/data[-(n + 1)] for n in day_ranges]

def performance_for_symbol(symbol, day_ranges=1, key=LAST_TRADE_PRICE_ONLY_STR):
    """
    Calculates the price performance of a symbol across one or more day ranges
    :param symbol: String representing ticker symbol
    :param day_ranges: Int or List of day ranges
    :param key: String key in historic data for which to calculate sma
    :return: Float or List of floats (depending on day_ranges)
    """
    if type(day_ranges) is int:
        num_days = day_ranges + 1
    else:
        num_days = max(day_ranges) + 1
    historic_data = get_historic_data_for_symbol(symbol, num_days)
    data = _get_data_by_key(historic_data, key)
    return performance(data, day_ranges)

def is_doji():
    pass
