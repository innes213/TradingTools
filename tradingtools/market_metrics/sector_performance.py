from tradingtools.technicals import performance_for_symbol

from operator import itemgetter

def sector_performance(day_ranges=1):
    sp_sector_symbols = ['XLK', 'XLB', 'XLV', 'XLF', 'XLI','XLY', 'XLP', 'XLU', 'XLE']

    data = [(symbol, performance_for_symbol(symbol, day_ranges)) for symbol in sp_sector_symbols]
    if type(day_ranges) is int:
        return sorted(data, key=itemgetter(1), reverse=True)
    return sorted(data, key=itemgetter(0))  # sort by symbol