from pyhoofinance.historicdata import get_number_of_historical_quotes
from pyhoofinance import defs

import numpy as np

from datetime import datetime

def _get_data_by_key(data, key):
    return [x[key] for x in data]

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

def sma_for_symbol(symbol, num_days=1, window_size=20, enddate=datetime.today(), key=defs.LAST_TRADE_PRICE_ONLY_STR):
    """
    Simple moving average across day_range days for numdays
    :param symbol: String Stock symbol for which to calculare SMA
    :param num_days: number of days for which average is calculated
    :param window_size: Int days to average across
    :param enddate: Date most recent date over which to calculate
    :param key: String key in historic data for which to calculate sma
    :return: List of floats
    """
    historic_data = get_number_of_historical_quotes(symbol, num_days + window_size - 1, enddate)
    return sma(_get_data_by_key(historic_data, key), window_size)

def _calculate_ema(current_value, k, last_ema):
    return current_value * k + last_ema * (1 - k)

def ema(historic_data, window_size=16):
    """
    Calculate EMA (exponential moving average) for given data
    :param historic_data: List of Floats for which to calculate EMA
    :param window_size: Int EMA window size (default = 16)
    :return: List of Floats
    """
    if len(historic_data) <= window_size:
        # todo: make this an exception
        print 'Not enough data to calulate ema!'
        return []

    if len(historic_data) < 5 * window_size:
        print 'Warn: EMA may not have enouugh history to be valid'

    i = 0
    last_ema = historic_data[0]
    ema_data = []
    k = 2.0 / (window_size + 1)
    for current_value in historic_data:
        ema_data.append(_calculate_ema(current_value, k, last_ema))
        last_ema = ema_data[i]
        i = i + 1

    return ema_data

def ema_for_symbol(symbol, num_days=1, window_size=22, enddate=datetime.today(), key=defs.LAST_TRADE_PRICE_ONLY_STR):
    """
    Calculates the EMA for a given symbol for a number of days across a window
    :param symbol: String Stock symbol for which to calculate EMA
    :param num_days: Int Number of days for which to calculate EMA
    :param window_size: Int EMA window size
    :param enddate: Date Most recent day to calculate EMA (default = today)
    :param key: String key in historic data for which to calculate EMA
    :return: List of Floats
    """
    historic_data = get_number_of_historical_quotes(symbol, 5 * window_size + num_days, enddate)
    return ema(_get_data_by_key(historic_data, key))[-num_days:]

def macd(historic_data, slow_window=26, fast_window=12, signal_window=9):
    """
    Calculates MACD of given data
    :param historic_data: List of Floats MACD source data
    :param slow_window: Slow EMA signal window size (default = 26)
    :param fast_window: Fast EMA signal window size (default = 12)
    :param signal_window: Signal EMA window size (default = 9)
    :return: Tuple MACD, signal, Histogram
    """
    delta = np.subtract(ema(historic_data, fast_window), ema(historic_data, slow_window))
    signal = ema(delta, signal_window)
    histogram = np.subtract(delta, signal)
    return delta, signal, histogram

def macd_for_symbol(symbol, num_days=1, slow_window=26, fast_window=12, signal_window=9, enddate=datetime.today(), key=defs.LAST_TRADE_PRICE_ONLY_STR):
    """
    MACD (macd, signal and histogram) for a given symbol
    :param symbol: String Stock symbol for which to calculate MACD
    :param num_days: Int Total number of periods (days) for which to calculate MACD over
    :param slow_window: Slow EMA signal window size (default = 26)
    :param fast_window: Fast EMA signal window size (default = 12)
    :param signal_window: Signal EMA window size (default = 9)
    :param enddate: Date Most recent date for which to calculate MACD (default = today)
    :param key: String Key in historic data for which to calculate MACD
    :return: Tuple MACD, signal, Histogram
    """
    historic_data = get_number_of_historical_quotes(symbol, 5 * slow_window + num_days, enddate)
    price_data = _get_data_by_key(historic_data, key)
    delta, signal, histogram = macd(price_data, slow_window, fast_window, signal_window)
    return delta[-num_days:], signal[-num_days:], histogram[-num_days:]

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

def performance_for_symbol(symbol, day_ranges=1, key=defs.LAST_TRADE_PRICE_ONLY_STR):
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
    historic_data = get_number_of_historical_quotes(symbol, num_days)
    data = _get_data_by_key(historic_data, key)
    return performance(data, day_ranges)

def is_doji():
    pass
