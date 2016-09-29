from ..indicators import Indicator
from ...equitydata import PastQuoteDataKeys

from numpy import divide, multiply, subtract

from datetime import datetime

NUM_PERIODS = 10

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
            #todo: throw exception
            print 'Error: Accumulation/Distribution data length mismatch'
            return []

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
        high_data = [x[PastQuoteDataKeys.HIGH] for x in historic_data]
        low_data = [x[PastQuoteDataKeys.LOW] for x in historic_data]
        close_data = [x[PastQuoteDataKeys.CLOSE] for x in historic_data]
        volume_data = [x[PastQuoteDataKeys.VOLUME] for x in historic_data]
        return self.calculate(high_data, low_data, close_data, volume_data)

