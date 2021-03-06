from ...utils.equitydata import get_historic_data_for_symbol, PastQuoteDataKeys

from datetime import datetime

class SignalTypes:
    BULLISH = 'bullish'
    BEARISH = 'bearish'
    NEUTRAL = 'neutral'
    OVERBOUGHT = 'overbought'
    OVERSOLD = 'oversold'

class SignalStrengthTypes:
    NA = 'n/a'
    WEAK = 'weak'
    MODEST = 'modest'
    STRONG = 'strong'

class TrendAgeTypes:
    NEW = 'new'
    OLD = 'old'

class Indicator(object):

    def __init__(self):
        pass

    _title = 'Indicator'
    _description_url = 'http://www.investopedia.com'

    def periods(self, num_periods=None):
        if num_periods is not None:
            if num_periods > 0:
                self._num_periods = num_periods
        else:
            return self._num_periods

    def calculate(self, historic_data):
        # Override with technical indicator/oscilator's computation
        pass

    def calculate_for_symbol(self, symbol, end_date=datetime.today(), key=None):
        # Override with retrieval of stock data and call self.calculate
        pass

    def analyze(self):
        pass

    def analyze_for_symbol(self):
        pass

    def info(self):
        """
        Returns the full title and informational URL of the indicator
        :return: title, url
        """
        return self._title, self._description_url

    def _data_for_symbol(self, symbol, num_periods, end_date=datetime.today(), key=PastQuoteDataKeys.ADJ_CLOSE):
        return get_historic_data_for_symbol(symbol, num_periods, end_date, key)


