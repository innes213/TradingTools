from ..indicators import Indicator

from numpy import abs as nabs
from numpy import add as nadd
from numpy import divide as ndivide
from numpy import max as nmax
from numpy import mean as nmean
from numpy import multiply as nmultiply
from numpy import subtract as nsubtract
from numpy import sum as nsum
from pyhoofinance.defs import *

from datetime import datetime

WINDOW_SIZE = 14
NUM_PERIODS = 1

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
            b = nabs(high_data[n] - close_data[n-1])
            c = nabs(low_data[n] - close_data[n-1])
            tr.append(nmax([a, b, c]))
        return tr

    def _smooth1(self,data):
        output = [nsum(data[:self._window_size])]
        for n in range(len(data) - self._window_size):
            output.append(output[n] - output[n]/self._window_size + data[n+self._window_size])
        return output

    def _smooth2(self, data):
        output = [nmean(data)]
        for n in range(1, len(data)):
            output.append((output[n-1] * (self._window_size - 1) + data[n]) / self._window_size)
        return output

    def calculate(self, high_data, low_data, close_data):
        upmoves = nsubtract(high_data[1:], high_data[0:-1])
        downmoves = nsubtract(low_data[0:-1], low_data[1:])
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
        plus_di = nmultiply(100, ndivide(smooth_pdm, atr))
        minus_di = nmultiply(100, ndivide(smooth_mdm, atr))
        # calculate directional index
        dx = nmultiply(100, ndivide(nabs(nsubtract(plus_di, minus_di)), nadd(plus_di, minus_di)))
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
        data = self._data_for_symbol(symbol, self._num_periods + self._window_size + 150, end_date, key=None)
        high_data = [x[DAY_HIGH_STR] for x in data]
        low_data = [x[DAY_LOW_STR] for x in data]
        close_data = [x[LAST_TRADE_PRICE_ONLY_STR] for x in data]
        adx, plus, minus = self.calculate(high_data, low_data, close_data)
        return adx[-self._num_periods:], plus[-self._num_periods:], minus[-self._num_periods:]
    