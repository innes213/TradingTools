from tradingtools.technicals.indicators.AD import AD
from tradingtools.technicals.indicators.ADX import ADX
from tradingtools.technicals.indicators.Aroon import Aroon
from tradingtools.technicals.indicators.Bollinger import Bollinger
from tradingtools.technicals.indicators.EMA import EMA
from tradingtools.technicals.indicators.MACD import MACD
from tradingtools.technicals.indicators.OBV import OBV
from tradingtools.technicals.indicators.RSI import RSI
from tradingtools.technicals.indicators.SMA import SMA
from tradingtools.technicals.indicators.Stochastic import Stochastic

symbols = ['SPY', 'SDS', 'GLD', 'AAPL', 'P', 'FB', 'ONVO', 'DLB']
indicators = [SMA(), EMA(), MACD(), OBV(), AD(), Aroon(), Stochastic(), RSI(), ADX()]

for symbol in symbols:
    print '\nTechnical Indicators for %s\n' % symbol
    for i in indicators:
        title, _ = i.info()
        print '%s for %s = %s' % (title, symbol, str(i.analyze_for_symbol(symbol)['signal_type']))
