from datetime import datetime
from numpy import subtract

from tradingtools.utils.equitydata import PastQuoteDataKeys
from .EMA import EMA
from ..indicators import Indicator

SLOW_WINDOW_SIZE = 26
FAST_WINDOW_SIZE = 12
SIGNAL_WINDOW_SIZE = 9
NUM_PERIODS = 1

class MACD(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, slow_window_size=SLOW_WINDOW_SIZE, fast_window_size=FAST_WINDOW_SIZE, signal_window_size=SIGNAL_WINDOW_SIZE):
        self._slow_window_size = slow_window_size
        self._fast_window_size = fast_window_size
        self._signal_window_size = signal_window_size
        self._num_periods = num_periods

    _title = 'Moving Average Convergence/Divergence'
    _description_url = 'http://www.investopedia.com/terms/m/macd.asp'

    def window(self, slow_window_size=None, fast_window_size=None, signal_window_size=None):
        """
        Sets or returns the MACD window sizes (slow, fast and signal)
        :param slow_window_size (optiona):
        :param fast_window_size (optional):
        :param signal_window_size (optional):
        :return: Tuple of Ints (slow_window, fast_window, signal_window)
        """
        if (slow_window_size, fast_window_size, signal_window_size) == (None, None, None):
            return self._slow_window_size, self._fast_window_size, self._signal_window_size
        if slow_window_size is not None:
            self._slow_window_size = slow_window_size
        if fast_window_size is not None:
            self._fast_window_size = fast_window_size
        if signal_window_size is not None:
            self._signal_window_size = signal_window_size

    def calculate(self, historic_data):
        """
        Calculates MACD of given data
        :param historic_data: List of Floats MACD source data
        :return: Tuple macd, signal, Histogram
        """
        fast_ema = EMA(self._num_periods, self._fast_window_size)
        slow_ema = EMA(self._num_periods, self._slow_window_size)
        signal_ema = EMA(self._num_periods, self._signal_window_size)

        macd = subtract(fast_ema.calculate(historic_data), slow_ema.calculate(historic_data))
        signal = signal_ema.calculate(macd)
        histogram = subtract(macd, signal)
        return macd, signal, histogram

    def calculate_for_symbol(self, symbol, end_date=datetime.today(), key=PastQuoteDataKeys.ADJ_CLOSE):
        """
        MACD (macd, signal and histogram) for a given symbol
        :param symbol: String Stock symbol for which to calculate MACD
        :param end_date: Date Most recent date for which to calculate MACD (default = today)
        :param key: String Key in historic data for which to calculate MACD
        :return: Tuple MACD, signal, Histogram
        """
        historic_data = self._data_for_symbol(symbol, 5 * self._slow_window_size + self._num_periods, end_date, key)
        macd, signal, histogram = self.calculate(historic_data)
        return macd[-self._num_periods:], signal[-self._num_periods:], histogram[-self._num_periods:]
