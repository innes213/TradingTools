from tradingtools.technicals.indicators.AD import AD
from tradingtools.technicals.indicators.Aroon import Aroon
from tradingtools.technicals.indicators.EMA import EMA
from tradingtools.technicals.indicators.MACD import MACD
from tradingtools.technicals.indicators.OBV import OBV
from tradingtools.technicals.indicators.SMA import SMA

print 'Default SMA for GOOGL', str(SMA().calculate_for_symbol('GOOGL'))
print 'Default EMA for GOOGL', str(EMA().calculate_for_symbol('GOOGL'))
print 'Default MACD for GOOGL', str(MACD().calculate_for_symbol('GOOGL'))
print 'Default OBV for GOOGL', str(OBV().calculate_for_symbol('GOOGL'))
print 'Default A/D for GOOGL', str(AD().calculate_for_symbol('GOOGL'))
print 'Default Aroon for GOOGL', str(Aroon().calculate_for_symbol('GOOGL'))

