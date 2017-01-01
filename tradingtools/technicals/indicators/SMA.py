from ..indicators import Indicator, SignalStrengthTypes, SignalTypes
from ...analysis import trend_length_and_slope
from tradingtools.utils.equitydata import PastQuoteDataKeys

from numpy import abs, mean

from datetime import datetime

WINDOW_SIZE = 20
NUM_PERIODS = 10

class SMA(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        self._window_size = window_size
        self._num_periods = num_periods

    _title = 'Simple Moving Average'
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
        if self._window_size == 1:
            return historic_data
        if len(historic_data) < self._window_size:
            print 'Window size exceeds length of data!'
            return []
        return [mean(historic_data[n:n+self._window_size]) for n in range(len(historic_data) - self._window_size + 1)]

    def calculate_for_symbol(self, symbol, end_date=datetime.today(), key=PastQuoteDataKeys.ADJ_CLOSE):
        """
        Simple moving average across day_range days for numdays
        :param symbol: String Stock symbol for which to calculare SMA
        :param enddate: Date most recent date over which to calculate
        :param key: String key in historic data for which to calculate sma
        :return: List of floats
        """
        return self.calculate(self._data_for_symbol(symbol, self._num_periods + self._window_size - 1, end_date, key))

    def analyze(self, data):
        trend_length, slope = trend_length_and_slope(data)
        signal_type = SignalTypes.NEUTRAL
        signal_strength = SignalStrengthTypes.NA
        if trend_length > 1:
            if slope > 0:
                signal_type = SignalTypes.BULLISH
            elif slope < 0:
                signal_type = SignalTypes.BEARISH
            magnitude = abs(slope)
            if magnitude > 1.0:
                signal_strength = SignalStrengthTypes.STRONG
            elif magnitude > 0.1:
                signal_strength = SignalStrengthTypes.MODEST
            else:
                signal_strength = SignalStrengthTypes.WEAK
        return dict(signal_strength=signal_strength, signal_type=signal_type, trend_length=trend_length, slope=slope)

    def analyze_for_symbol(self, symbol, end_date=datetime.today()):
        return self.analyze(self.calculate_for_symbol(symbol, end_date))
