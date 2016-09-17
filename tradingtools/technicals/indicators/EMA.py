from  ..indicators import Indicator

from pyhoofinance.defs import *

from datetime import datetime

WINDOW_SIZE = 20
NUM_PERIODS = 1

class EMA(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        self._window_size = window_size
        self._num_periods = num_periods

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
            # todo: make this an exception
            print 'Not enough data to calulate ema!'
            return []

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

    def calculate_for_symbol(self, symbol, end_date=datetime.today(), key=LAST_TRADE_PRICE_ONLY_STR):
        """
        Calculates the EMA for a given symbol for a number of days across a window
        :param symbol: String Stock symbol for which to calculate EMA
        :param end_date: Date Most recent day to calculate EMA (default = today)
        :param key: String key in historic data for which to calculate EMA
        :return: List of Floats
        """
        return self.calculate(self._data_for_symbol(symbol, self._num_periods + 5 * self._window_size, end_date, key))[-self._num_periods:]
