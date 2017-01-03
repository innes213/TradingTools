# On Balance Volume - Leading indicator

from .SMA import SMA
from ..indicators import Indicator, SignalStrengthTypes, SignalTypes
from ...analysis import trend_length_and_slope
from ...utils.equitydata import PastQuoteDataKeys

from numpy import abs

from datetime import datetime

NUM_PERIODS = 20

class OBV(Indicator):

    def __init__(self, num_periods=NUM_PERIODS):
        self._num_periods = num_periods

    _title = 'On-Balance Volume'
    _description_url = 'http://www.investopedia.com/terms/o/onbalancevolume.asp'

    def calculate(self, price_data, volume_data):
        if len(price_data) != len(volume_data):
            #todo: throw exception
            print 'Error: OBV list length mismatch'
            return []

        if len(price_data) < 2:
            #todo: throw exception
            print "Error: OBV requires data for at least two periods of data"
            return []

        obv = 0
        obv_data = []
        for i in range(1,len(price_data)):
            if price_data[i] > price_data[i-1]:
                obv = obv + volume_data[i]
            elif price_data[i] < price_data[i-1]:
                obv = obv - volume_data[i]
            obv_data.append(obv)
        return obv_data

    def calculate_for_symbol(self, symbol, end_date=datetime.today()):
        historic_data = self._data_for_symbol(symbol, self._num_periods + 1, end_date=end_date, key=None)
        price_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in historic_data]
        volume_data = [x[PastQuoteDataKeys.VOLUME] for x in historic_data]
        return self.calculate(price_data, volume_data)[-self._num_periods:]

    def analyze(self, obv_data, price_data):
        sma = SMA(window_size=3)
        smoothed_obv = sma.calculate(obv_data)
        smoothed_price = sma.calculate(price_data)
        _, obv_slope = trend_length_and_slope(smoothed_obv)
        _, price_slope = trend_length_and_slope(smoothed_price)
        signal_type = SignalTypes.NEUTRAL
        signal_strength = SignalStrengthTypes.NA
        # if the OBV and prices are moving in opposite directions, we have a signal
        if obv_slope * price_slope < 0:
            if obv_slope < 0:
                signal_type = SignalTypes.BEARISH
            else:
                signal_type = SignalTypes.BULLISH
            magnitude = obv_slope * price_slope
            # todo: Is this right? I'm pulling this out of my butt
            if magnitude > 25:
                signal_strength = SignalStrengthTypes.STRONG
            elif magnitude > 10:
                signal_strength = SignalStrengthTypes.MODEST
            else:
                signal_strength = SignalStrengthTypes.WEAK

        return dict(signal_strength=signal_strength, signal_type=signal_type, obv_slope=obv_slope, price_slope=price_slope)

    def analyze_for_symbol(self, symbol, end_date=datetime.today()):
        historic_data = self._data_for_symbol(symbol, self._num_periods + 1, end_date=end_date, key=None)
        price_data = [x[PastQuoteDataKeys.ADJ_CLOSE] for x in historic_data]
        volume_data = [x[PastQuoteDataKeys.VOLUME] for x in historic_data]
        return self.analyze(self.calculate(price_data, volume_data)[-self._num_periods:],price_data)
