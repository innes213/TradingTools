from ..indicators import Indicator, SignalStrengthTypes, SignalTypes
from ..indicators.SMA import SMA
from tradingtools.utils.equitydata import PastQuoteDataKeys

from numpy import max, min

from datetime import datetime

WINDOW_SIZE = 14
SMOOTHING_WINDOW_SIZE = 3
NUM_PERIODS = 20

class Stochastic(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE, smoothing_window_size=SMOOTHING_WINDOW_SIZE):
        self._window_size = window_size
        self._num_periods = num_periods
        self._smoothing_window_size = smoothing_window_size

    _title = 'Stochastic Oscillator (Fast)'
    _description_url = 'http://www.investopedia.com/terms/s/stochasticoscillator.asp'

    def window(self, window_size=None, smoothing_window_size=None):
        """
        Set or get K window size and/pr smoothing window size
        :param window_size: Integer - K window size
        :param smoothing_window_size: Integer - smoothing window size
        :return: If no params given, returns K window-size, smoothing window size
        """
        if (window_size, smoothing_window_size) == (None, None):
            return window_size, smoothing_window_size
        if window_size is not None and window_size > 0:
            self._window_size = window_size
        if smoothing_window_size is not None and smoothing_window_size > 0:
            self._smoothing_window_size = smoothing_window_size

    def calculate(self, high_data, low_data, close_data):
        """
        Calculates stocastic oscillator given high, low, and close data
        :param high_data: List of Floates
        :param low_data: List of Floats
        :param close_data: List of Floats
        :return: Tuple of %k and %D List of Floats
        """
        if len(high_data) != len(low_data) and len(close_data) != len(high_data):
            #todo: throw exception
            print 'Error: Stochastic data length mismatch'
            return []
        k = []
        for n in range(len(high_data) - self._window_size + 1):
            close = close_data[n+self._window_size - 1]
            high = max(high_data[n:n+self._window_size])
            low = min(low_data[n:n+self._window_size])
            k.append(100 * (close - low) / (high - low))
        return k, SMA(window_size=self._smoothing_window_size).calculate(k)

    def calculate_for_symbol(self, symbol, end_date=datetime.today()):
        """
        Gets high, low and close data for an equity and calcualtes Stocastic Oscillator
        :param symbol:
        :param end_date:
        :return: Tuple of %k and %D List of Floats
        """
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size + self._smoothing_window_size - 2, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in data]
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in data]
        k, d = self.calculate(high_data, low_data, close_data)
        return k[-self._num_periods:], d[-self._num_periods:]

    def analyze(self, k, d):
        signal_type = SignalTypes.NEUTRAL
        signal_strength = SignalStrengthTypes.NA
        if k[-1] > 80 and d[-1] > 80:
            signal_type = SignalTypes.OVERBOUGHT
        elif k[-1] < 20 and d[-1] < 20:
            signal_type = SignalTypes.OVERSOLD
        return dict(signal_strength=signal_strength, signal_type=signal_type, k=k[-1], d= d[-1])
    
    def analyze_for_symbol(self, symbol, end_date=datetime.today()):
        k, d = self.calculate_for_symbol(symbol, end_date)
        return self.analyze(k, d)
        