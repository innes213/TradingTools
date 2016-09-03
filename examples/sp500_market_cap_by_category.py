from tradingtools.utils import FinSymbolsKeys, get_sp500_symbol_list, get_sp500_symbols_by_key
from pyhoofinance.quotedata import get_quotes
from pyhoofinance.defs import *

def sp500_market_cap_by_category(category):
    quote_data = {}

    # fromat S&P 500 data as a single dictionary
    for q in get_quotes(get_sp500_symbol_list(), [MARKET_CAPITALIZATION_STR]):
        quote_data[q[SYMBOL_STR]] = q[MARKET_CAPITALIZATION_STR]

    # build list of catebory: market cap
    out = []
    for group,symbols in get_sp500_symbols_by_key(category):
        # add up the market caps for each symbol in a group
        sum = 0
        for s in symbols:
            if quote_data[s] is not None:
                sum = sum + quote_data[s]
        out.append((group, sum))
    out.sort(key=lambda tup: tup[1], reverse=True)

    # print output
    i = 0
    for cat, cap in out:
        i = i + 1
        print '%i. %s: $%4.2fB' % (i, cat, cap/1000000000.0)

if __name__ == '__main__':
    for category in [FinSymbolsKeys.HEADQUARTERS, FinSymbolsKeys.SECTOR, FinSymbolsKeys.INDUSTRY]:
        print '\n=== S&P 500 Market Cap by %s ===' % category.title()
        sp500_market_cap_by_category(category)