from ..indicators import Indicator
from ...equitydata import PastQuoteDataKeys

from numpy import add, mean, multiply, subtract, std

from datetime import datetime

WINDOW_SIZE = 20
NUM_PERIODS = 1

class Bollinger(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        self._window_size = window_size
        self._num_periods = num_periods
        if self._window_size < 1 or self._num_periods < 1:
            raise ValueError('Invalid window size or number of periods')

    _title = 'Bollinger Bands (R)'
    _description_url = 'http://www.investopedia.com/terms/b/bollingerbands.asp'

    def window(self, window_size=None):
        if window_size is not None:
            if window_size > 0:
                self._window_size = window_size
        else:
            return self._window_size

    def calculate(self, historic_data):
        """
        Calculates Bollinger Bands (R) for historic data
        :param historic_data: List of floats representing past data (price, volume, etc)
        :return: List of floats representing the averages
        """
        if len(historic_data) < self._window_size:
            print 'Window size exceeds length of data!'
            return []
        if self._window_size == 1:
            middle = historic_data
        else:
            middle = [mean(historic_data[n:n+self._window_size]) for n in range(len(historic_data) - self._window_size + 1)]
        two_stdv = multiply(2, [std(historic_data[n:n+self._window_size]) for n in range(len(historic_data) - self._window_size + 1)])
        upper = add(middle, two_stdv)
        lower = subtract(middle, two_stdv)
        return middle, upper, lower

    def calculate_for_symbol(self, symbol, end_date=datetime.today(), key=PastQuoteDataKeys.ADJ_CLOSE):
        """
        Bollinger Bands (R) across window_size periods for num_periods
        :param symbol: String Stock symbol for which to calculare Bollinger Bands (R)
        :param enddate: Date most recent date over which to calculate
        :param key: String key in historic data for which to calculate
        :return: middle, upper, lower bands as lists of floats
        """
        return self.calculate(self._data_for_symbol(symbol, self._num_periods + self._window_size - 1, end_date, key))
