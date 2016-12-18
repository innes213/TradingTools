from  ..indicators import Indicator
from tradingtools.utils.equitydata import PastQuoteDataKeys

from numpy import max, min

from datetime import datetime

WINDOW_SIZE = 20
NUM_PERIODS = 1

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
            #todo: throw exception
            print 'Aroon error: high and low data have different lengths'
            return []
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
        Calculates Aroon for
        :param symbol: String Stock symbol for which to calculare SMA
        :param end_date: Date most recent date over which to calculate
        :param key: String key in historic data for which to calculate sma
        :return: Tuple consisting of 2 lists (aroon_up, aroon_down)
        """
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size, end_date, key=None)
        high_data = [x[PastQuoteDataKeys.ADJ_HIGH] for x in data]
        low_data = [x[PastQuoteDataKeys.ADJ_LOW] for x in data]
        return self.calculate(high_data, low_data)
