from tradingtools.utils import get_sp500_symbols_by_region
from pyhoofinance.quotedata import get_quotes
from pyhoofinance.defs import *

out = []
for state,symbols in get_sp500_symbols_by_region():
    sum = 0
    for quote in get_quotes(symbols,[MARKET_CAPITALIZATION_STR]):
        if quote[MARKET_CAPITALIZATION_STR] is not None:
            sum = sum + quote[MARKET_CAPITALIZATION_STR]
    out.append((state, sum))
    out.sort(key=lambda tup: tup[1], reverse=True)
i = 1
for state, cap in out:
    print '%i. %s: $%4.2fB' % (i, state, cap/1000000000.0)
    i = i + 1