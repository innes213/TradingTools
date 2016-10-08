from  ..indicators import Indicator
from ...equitydata import PastQuoteDataKeys

from numpy import subtract, sum

from datetime import datetime

WINDOW_SIZE = 14
NUM_PERIODS = 1

class RSI(Indicator):

    def __init__(self, num_periods=NUM_PERIODS, window_size=WINDOW_SIZE):
        self._window_size = window_size
        self._num_periods = num_periods

    _title = 'Relative Strength Index'
    _description_url = 'http://www.investopedia.com/terms/r/rsi.asp'

    def window(self, window_size=None):
        if window_size is not None and window_size > 0:
                self._window_size = window_size
        else:
            return self._window_size

    def _calculate_avg_gains_and_losses(self, gain_data):
        # Create gain and loss vectos
        gains = []
        losses = []
        for x in gain_data:
            if x > 0:
                gains.append(x)
                losses.append(0)
            elif x < 0:
                gains.append(0)
                losses.append(-x)
            else:
                gains.append(0)
                losses.append(0)
        # calculate avg gains and losses per Wiley
        avg_gains = [sum(gains[0:self._window_size]) / self._window_size]
        avg_losses = [sum(losses[0:self._window_size]) / self._window_size]
        gains = gains[self._window_size:]
        losses = losses[self._window_size:]
        for n in range(0, len(gains)):
            avg_gains.append((avg_gains[n] * (self._window_size - 1) + gains[n]) / self._window_size)
            avg_losses.append((avg_losses[n] * (self._window_size - 1) + losses[n]) / self._window_size)
        return avg_gains, avg_losses

    def calculate(self, gain_data):
        if len(gain_data) < self._window_size:
            #todo: throw exception
            print "RSI Error: Data length less than window size"
            return []
        avg_gains, avg_losses = self._calculate_avg_gains_and_losses(gain_data)
        rsi = []
        for n in range(0, len(avg_losses)):
            if avg_losses[n] == 0:
                rsi.append(100.0)
            else:
                rsi.append(100.0 - 100.0 / (1.0 + avg_gains[n] / avg_losses[n]))
        return rsi

    def calculate_for_symbol(self, symbol, end_date=datetime.today()):
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size + 250, end_date, key=PastQuoteDataKeys.ADJ_CLOSE)
        return self.calculate(subtract(data[1:], data[0:-1]))[-self._num_periods:]
