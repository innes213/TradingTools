from  ..indicators import Indicator

from pyhoofinance.defs import *
from numpy import mean as nmean

from datetime import datetime

WINDOW_SIZE = 20
NUM_PERIODS = 1

class SMA(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        self._window_size = window_size
        self._num_periods = num_periods

    _description_url = 'http://www.investopedia.com/terms/s/sma.asp'

    def window(self, window_size=None):
        if window_size is not None:
            if window_size > 0:
                self._window_size = window_size
        else:
            return self._window_size

    def calculate(self, historic_data):
        """
        Calculates the simple moving average for historic data
        :param historic_data: List of floats representing past data (price, volume, etc)
        :return: List of floats representing the averages
        """
        if len(historic_data) < self._window_size:
            print 'Window size exceeds length of data!'
            return []
        return [nmean(historic_data[n:n+self._window_size]) for n in range(len(historic_data) - self._window_size + 1)]

    def calculate_for_symbol(self, symbol, end_date=datetime.today(), key=LAST_TRADE_PRICE_ONLY_STR):
        """
        Simple moving average across day_range days for numdays
        :param symbol: String Stock symbol for which to calculare SMA
        :param enddate: Date most recent date over which to calculate
        :param key: String key in historic data for which to calculate sma
        :return: List of floats
        """
        return self.calculate(self._data_for_symbol(symbol, self._num_periods + self._window_size - 1, end_date, key))
