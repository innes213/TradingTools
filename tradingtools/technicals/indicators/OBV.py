from ..indicators import Indicator
from ...equitydata import PastQuoteDataKeys

from datetime import datetime

NUM_PERIODS = 2

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

