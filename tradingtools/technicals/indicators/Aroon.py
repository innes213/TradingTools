# From stockcharts.com:
#
# Interpretation
#
# The Aroon indicators fluctuate above/below a centerline (50) and
# are bound between 0 and 100. These three levels are important for
# interpretation. At its most basic, the bulls have the edge when
# Aroon-Up is above 50 and Aroon-Down is below 50. This indicates a
# greater propensity for new x-day highs than lows. The converse is
# true for a downtrend. The bears have the edge when Aroon-Up is
# below 50 and Aroon-Down is above 50.
#
# A surge to 100 indicates that a trend may be emerging. This can
# be confirmed with a decline in the other Aroon indicator. For
# example, a move to 100 in Aroon-Up combined with a decline below
# 30 in Aroon-Down shows upside strength. Consistently high readings
# mean prices are regularly hitting new highs or new lows for the
# specified period. Prices are moving consistently higher when Aroon-Up
# remains in the 70-100 range for an extended period. Conversely,
# consistently low readings indicate that prices are seldom hitting new
# highs or lows. Prices are NOT moving lower when Aroon-Down remains in
# the 0-30 range for an extended period. This does not mean prices are
#  moving higher though. For that we need to check Aroon-Up.
#
# New Trend Emerging
#
# There are three stages to an emerging trend signal. First, the Aroon
# lines will cross. Second, the Aroon lines will cross above/below 50.
# Third, one of the Aroon lines will reach 100. For example, the first
# stage of an uptrend signal is when Aroon-Up moves above Aroon-Down. This
# shows new highs becoming more recent than new lows. Keep in mind that
# Aroon measures the time elapsed, not the price. The second stage is when
# Aroon-Up moves above 50 and Aroon-Down moves below 50. The third stage is
# when Aroon-Up reaches 100 and Aroon-Down remains at relatively low levels.
# The first and second stages do not always occur in that order. Sometimes
# Aroon-Up will break above 50 and then above Aroon-Down. Reverse engineering
# the uptrend stages will give you the emerging downtrend signal. Aroon-Down
# breaks above Aroon-Up, breaks above 50 and reaches 100.

from ..indicators import Indicator, SignalStrengthTypes, SignalTypes
from tradingtools.utils.equitydata import PastQuoteDataKeys

from numpy import max, min, subtract

from datetime import datetime

WINDOW_SIZE = 20
NUM_PERIODS = 5

class Aroon(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        super(Aroon, self).__init__()
        self._num_periods = num_periods
        self._window_size = window_size

    _title = 'Aroon'
    _description_url = 'http://www.investopedia.com/terms/a/aroon.asp'

    def window(self, window_size=None):
        if window_size is not None:
            if window_size > 0:
                self._window_size = window_size
        else:
            return self._window_size

    def calculate(self, high_data, low_data):
        """
        Calculates the Aroon for historic data
        :param historic_data: List of floats representing past data (price, volume, etc)
        :return: List of floats representing the averages
        """
        if len(high_data) != len(low_data):
            raise ValueException('Aroon error: high and low data have different lengths')
        if len(high_data) < self._window_size:
            print 'Aroon requires data for at least one window'
            return []
        aroon_up = []
        aroon_down = []
        for n in range(len(high_data) - self._window_size):
            high_segment = high_data[n:n+self._window_size + 1]
            low_segment = low_data[n:n+self._window_size + 1]
            max_index = high_segment.index(max(high_segment))
            min_index = low_segment.index(min(low_segment))
            aroon_up.append(100.0 * max_index / self._window_size)
            aroon_down.append(100.0 * min_index / self._window_size)
        return aroon_up, aroon_down

    def calculate_for_symbol(self, symbol, end_date=datetime.today()):
        """
        Calculates Aroon for a given symbol
        :param symbol: String Stock symbol for which to calculare SMA
        :param end_date: Date most recent date over which to calculate
        :param key: String key in historic data for which to calculate sma
        :return: Tuple consisting of 2 lists (aroon_up, aroon_down)
        """
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in data]
        return self.calculate(high_data, low_data)

    def analyze(self, high_data, low_data):
        aroon_up, aroon_down = self.calculate(high_data, low_data)
        aroon_delta = subtract(aroon_up, aroon_down)
        signal_type = SignalTypes.NEUTRAL
        if aroon_down[-1] < 50 < aroon_up[-1]:
            signal_type = SignalTypes.BULLISH
        elif aroon_up[-1] < 50 < aroon_down[-1]:
            signal_type = SignalTypes.BEARISH
        if aroon_delta[-1] > 50:
            signal_strength = SignalStrengthTypes.STRONG
        elif aroon_delta[-1] > 20:
            signal_strength = SignalStrengthTypes.MODEST
        else:
            signal_strength = SignalStrengthTypes.WEAK

        return dict(signal_type=signal_type, signal_strength=signal_strength, aroon_up=aroon_up[-1], aroon_down=aroon_down[-1])

    def analyze_for_symbol(self, symbol, end_date=datetime.today()):
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in data]
        return self.analyze(high_data, low_data)

