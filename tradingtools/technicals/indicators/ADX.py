# From Stockcharts.com:
# The Average Directional Index (ADX), Minus Directional Indicator (-DI) and Plus Directional
# Indicator (+DI) represent a group of directional movement indicators that form a trading
# system developed by Welles Wilder. Wilder designed ADX with commodities and daily prices in
# mind, but these indicators can also be applied to stocks. The Average Directional Index
# (ADX) measures trend strength without regard to trend direction. The other two indicators,
# Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI), complement ADX by
# defining trend direction. Used together, chartists can determine both the direction and
# strength of the trend.
#
# Wilder put forth a simple system for trading with these directional movement indicators.
# The first requirement is for ADX to be trading above 25. This ensures that prices are
# trending. Many traders, however, use 20 as the key level. A buy signal occurs when +DI
# crosses above - DI. Wilder based the initial stop on the low of the signal day. The signal
# remains in force as long as this low holds, even if +DI crosses back below - DI. Wait for this
# low to be penetrated before abandoning the signal. This bullish signal is reinforced if/when
# ADX turns up and the trend strengthens. Once the trend develops and becomes profitable,
# traders will have to incorporate a stop-loss and trailing stop should the trend continue. A sell
# signal triggers when - DI crosses above +DI. The high on the day of the sell signal becomes the
# initial stop-loss.

from ..indicators import Indicator, SignalTypes, SignalStrengthTypes
from ...analysis import trend_length_and_slope
from ...analysis import zero_crossings
from tradingtools.utils.equitydata import PastQuoteDataKeys

from numpy import abs, add, divide, max, mean, multiply, subtract, sum

from datetime import datetime

WINDOW_SIZE = 14
NUM_PERIODS = 20
JUNK_PERIODS = 150

class ADX(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        super(ADX, self).__init__()
        self._window_size = window_size
        self._num_periods = num_periods

    _title = 'Average Direction Index'
    _description_url = 'http://www.investopedia.com/terms/a/adx.asp'

    def window(self, window_size=None):
        if window_size is not None:
            if window_size > 0:
                self._window_size = window_size
        else:
            return self._window_size

    def _get_true_range(self, high_data, low_data, close_data):
        tr=[]
        for n in range(1,len(high_data)):
            a = high_data[n] - low_data[n]
            b = abs(high_data[n] - close_data[n-1])
            c = abs(low_data[n] - close_data[n-1])
            tr.append(max([a, b, c]))
        return tr

    def _smooth1(self,data):
        output = [sum(data[:self._window_size])]
        for n in range(len(data) - self._window_size):
            output.append(output[n] - output[n]/self._window_size + data[n+self._window_size])
        return output

    def _smooth2(self, data):
        output = [mean(data)]
        for n in range(1, len(data)):
            output.append((output[n-1] * (self._window_size - 1) + data[n]) / self._window_size)
        return output

    def calculate(self, high_data, low_data, close_data):
        if len(high_data) - len(low_data) != 0 or len(low_data) - len(close_data) != 0:
            raise ValueError('Array lengths must match.')
        if len(high_data) <= JUNK_PERIODS:
            print 'WARNING: ADX requires at least %i periods of data!' % JUNK_PERIODS
        upmoves = subtract(high_data[1:], high_data[0:-1])
        downmoves = subtract(low_data[0:-1], low_data[1:])
        # calculate +DM and -DM
        plus_dm = []
        minus_dm = []
        for n in range(len(upmoves)):
            if upmoves[n] > 0 and upmoves[n] > downmoves[n]:
                plus_dm.append(upmoves[n])
            else:
                plus_dm.append(0)
            if downmoves[n] > 0 and downmoves[n] > upmoves[n]:
                minus_dm.append(downmoves[n])
            else:
                minus_dm.append(0)
        # get smoothed TR, +DM and -DM
        atr = self._smooth1(self._get_true_range(high_data, low_data, close_data))
        smooth_pdm = self._smooth1(plus_dm)
        smooth_mdm = self._smooth1(minus_dm)
        # calculate plus and minus direction indicators
        plus_di = multiply(100.0, divide(smooth_pdm, atr))
        minus_di = multiply(100.0, divide(smooth_mdm, atr))
        # calculate directional index
        dx = multiply(100.0, divide(abs(subtract(plus_di, minus_di)), add(plus_di, minus_di)))
        # calculate average directional index
        adx = self._smooth2(dx)
        return adx, plus_di, minus_di

    def calculate_for_symbol(self, symbol, end_date=datetime.today()):
        """
        Average Directional Index given an equite symbol
        :param symbol: String Stock symbol for which to calculare SMA
        :param end_date: Date most recent date over which to calculate
        :return: List of floats
        """
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size + JUNK_PERIODS, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in data]
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in data]
        adx, plus, minus = self.calculate(high_data, low_data, close_data)
        return adx[-self._num_periods:], plus[-self._num_periods:], minus[-self._num_periods:]

    def analyze(self, high_data, low_data, close_data):
        adx, plus_di, minus_di = self.calculate(high_data, low_data, close_data)
        adx = adx[JUNK_PERIODS:]
        plus_di = plus_di[JUNK_PERIODS:]
        minus_di = minus_di[JUNK_PERIODS:]
        di_delta = subtract(plus_di, minus_di)

        _, adx_slope = trend_length_and_slope(adx)
        adx_momentum = 'flat'
        if adx_slope > 0:
            adx_momentum = 'accelerating'
        elif adx_slope < 0:
            adx_momentum = 'slowing'

        if adx[-1] >= 30:
            trend_strength = SignalStrengthTypes.STRONG
        elif adx[-1] >= 20:
            trend_strength = SignalStrengthTypes.MODEST
        else:
            trend_strength = SignalStrengthTypes.WEAK

        # determine if bullish or bearish
        if di_delta[-1] > 0:
            signal_type = SignalTypes.BULLISH
        elif di_delta[-1] < 0:
            signal_type = SignalTypes.BEARISH
        # +di and -di are crossing
        else:
            _, plus_di_slope = trend_length_and_slope(plus_di)
            if plus_di_slope > 0:
                signal_type = SignalTypes.BULLISH
            else:
                signal_type = SignalTypes.BEARISH

        # get low price of +di and -di intersection
        # todo: should we return high price if trend is bearish?
        zcd = zero_crossings(di_delta)
        if zcd != []:
            di_cross_low = low_data[zcd[-1]]
        else:
            di_cross_low = -1

        return dict(adx=adx[-1], plus_di=plus_di[-1], minus_di=minus_di[-1], signal_type=signal_type,
                    adx_momentum=adx_momentum, trend_strength=trend_strength, di_cross_low=di_cross_low)

    def analyze_for_symbol(self, symbol, end_date=datetime.today()):
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size + JUNK_PERIODS, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in data]
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in data]
        return self.analyze(high_data, low_data, close_data)
