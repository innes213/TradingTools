# Indicator usage (from Investopedia)
# For example, many up days occurring with high volume in a downtrend could signal the demand
# for the underlying is starting to increase. In practice, this indicator is used to find
# situations in which the indicator is heading in the opposite direction as the price. Once
# this divergence is identified, the trader waits to confirm the reversal and makes his
# transaction decisions using other technical indicators. Although the accumulation/distribution
# line helps to determine a security's trend, the indicator does not take into account price
# gaps that may occur.

from ..indicators import Indicator
from ..indicators import SignalTypes
from ...analysis import find_gaps, trend_length_and_slope
from tradingtools.utils.equitydata import PastQuoteDataKeys

from numpy import divide, multiply, subtract

from datetime import datetime

NUM_PERIODS = 10
TREND_SLOPE_THRESHHOLD = 0.02

class AD(Indicator):

    def __init__(self, num_periods=NUM_PERIODS):
        super(AD, self).__init__()
        self._num_periods = num_periods

    _title = 'Accumulation/Distribution'
    _description_url = 'http://www.investopedia.com/terms/a/accumulationdistribution.asp'

    def window(self, window_size=None):
        if window_size is not None:
            if window_size > 0:
                self._window_size = window_size
        else:
            return self._window_size

    def calculate(self, high_data, low_data, close_data, volume_data):
        """
        Accumulation/Distribution
        :param high_data:
        :param low_data:
        :param close_data:
        :param volume_data:
        :return: List of Floats
        """
        if (len(high_data) - len(low_data)) + (len(close_data) - len(volume_data)) != 0:
            raise ValueError('Error: Accumulation/Distribution data length mismatch')

        # calculate money flow multiplier
        close_minus_low = subtract(close_data, low_data)
        high_minus_close = subtract(high_data, close_data)
        high_minus_low = subtract(high_data, low_data)
        cml_minus_hmc = subtract(close_minus_low, high_minus_close)
        mfm = divide(cml_minus_hmc, high_minus_low)
        # return money flow multiplier by volume
        ad = multiply(mfm, volume_data)
        sum = 0
        for i in range(0, len(ad)):
            ad[i] = ad[i] + sum
            sum = sum + ad[i]
        return ad

    def calculate_for_symbol(self, symbol, end_date=datetime.today()):
        historic_data = self._data_for_symbol(symbol, self._num_periods, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in historic_data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in historic_data]
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in historic_data]
        volume_data = [x[PastQuoteDataKeys.VOLUME] for x in historic_data]
        return self.calculate(high_data, low_data, close_data, volume_data)

    def analyze(self, high_data, low_data, open_data, close_data, volume_data):
        gaps = find_gaps(open_data, close_data, 0.5 / 100.0)  # threshold = 0.05%
        if gaps != []:
            last_gap = gaps[-1]
            if len(open_data) - last_gap < 3:
                print "Recent gap in price data makes A/D unreliable"
            high_data = high_data[last_gap:]
            low_data = low_data[last_gap:]
            close_data = close_data[last_gap:]
            volume_data = volume_data[last_gap:]
        ad = self.calculate(high_data, low_data, close_data, volume_data)
        ad_trend_length, ad_slope = trend_length_and_slope(ad)
        ad_signal = SignalTypes.NEUTRAL
        if ad_trend_length > 2:
            if ad_slope > TREND_SLOPE_THRESHHOLD:
                ad_signal = SignalTypes.BULLISH
            elif ad_slope < -TREND_SLOPE_THRESHHOLD:
                ad_signal = SignalTypes.BEARISH

        result = { 'signal':ad_signal,
                  'trend_length':ad_trend_length,
                  'trend_slope':ad_slope }

        return result

    def analyze_for_symbol(self, symbol, end_date=datetime.today()):
        historic_data = self._data_for_symbol(symbol, self._num_periods, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in historic_data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in historic_data]
        open_data = [x[PastQuoteDataKeys.ADJ_OPEN] for x in historic_data]
        close_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in historic_data]
        volume_data = [x[PastQuoteDataKeys.VOLUME] for x in historic_data]
        return self.analyze(high_data, low_data, open_data, close_data, volume_data)

