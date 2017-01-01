from ..indicators import Indicator, SignalStrengthTypes, SignalTypes
from ...analysis import trend_length_and_slope
from tradingtools.utils.equitydata import PastQuoteDataKeys

from numpy import abs

from datetime import datetime

WINDOW_SIZE = 20
NUM_PERIODS = 10

class EMA(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        super(EMA, self).__init__()
        self._window_size = window_size
        self._num_periods = num_periods

    _title = 'Exponential Moving Average'
    _description_url = 'http://www.investopedia.com/terms/e/ema.asp'

    def window(self, window_size=None):
        if window_size is not None:
            if window_size > 0:
                self._window_size = window_size
        else:
            return self._window_size

    def _calculate_ema(self, current_value, k, last_ema):
        return current_value * k + last_ema * (1 - k)

    def calculate(self, historic_data):
        """
        Calculate EMA (exponential moving average) for given data
        :param historic_data: List of Floats for which to calculate EMA
        :return: List of Floats
        """
        if len(historic_data) <= self._window_size:
            raise ValueError('Not enough data to calulate ema!')

        if len(historic_data) < 5 * self._window_size:
            print 'Warn: EMA may not have enouugh history to be valid'

        i = 0
        last_ema = historic_data[0]
        ema_data = []
        k = 2.0 / (self._window_size + 1)
        for current_value in historic_data:
            ema_data.append(self._calculate_ema(current_value, k, last_ema))
            last_ema = ema_data[i]
            i = i + 1
        return ema_data

    def calculate_for_symbol(self, symbol, end_date=datetime.today(), key=PastQuoteDataKeys.ADJ_CLOSE):
        """
        Calculates the EMA for a given symbol for a number of days across a window
        :param symbol: String Stock symbol for which to calculate EMA
        :param end_date: Date Most recent day to calculate EMA (default = today)
        :param key: String key in historic data for which to calculate EMA
        :return: List of Floats
        """
        return self.calculate(self._data_for_symbol(symbol, self._num_periods + 5 * self._window_size, end_date, key))[-self._num_periods:]

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
