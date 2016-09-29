from finsymbols import get_nasdaq_symbols, get_nyse_symbols, get_sp500_symbols
from pyhoofinance.defs import *
from pyhoofinance.historicdata import get_number_of_historical_quotes
from pyhoofinance.quotedata import get_quote, get_quotes

from datetime import datetime

class QuoteDataKeys:
    """
    Mapping of pyhoofinance defs.
    see https://github.com/innes213/pyhoofinance/blob/master/pyhoofinance/defs.py
    and https://github.com/innes213/pyhoofinance/blob/master/pyhoofinance/historicdata.py
    """
    OPEN = OPEN_STR
    LAST = LAST_TRADE_PRICE_ONLY_STR
    HIGH = DAY_HIGH_STR
    LOW = DAY_LOW_STR
    VOLUME = VOLUME_STR
    DATE = LAST_TRADE_DATE_STR

class PastQuoteDataKeys:
    OPEN = OPEN_STR
    CLOSE = LAST_TRADE_PRICE_ONLY_STR
    ADJ_CLOSE = ADJUSTED_CLOSE_STR
    HIGH = DAY_HIGH_STR
    LOW = DAY_LOW_STR
    VOLUME = VOLUME_STR
    DATE = TRADE_DATE_STR

class SymbolList:
    SP500 = 'sp500'
    NASDAQ = 'nasdaq' #  sector and industry data are bad
    NYSE = 'nyse'

class FinSymbolsKeys:
    SYMBOL = 'symbol'
    INDUSTRY = 'industry'
    HEADQUARTERS = 'headquarters'
    SECTOR = 'sector'
    COMPANY = 'company'

def get_company_data_from_source(source):
    dispatch = { SymbolList.NASDAQ: get_nasdaq_symbols,
                 SymbolList.SP500: get_sp500_symbols,
                 SymbolList.NYSE: get_nyse_symbols }
    return dispatch[source]()

def get_symbol_list(source):
    return [s[FinSymbolsKeys.SYMBOL] for s in get_company_data_from_source(source)]

def get_symbols_by_key_from_source(key, source=SymbolList.SP500):
    key_set = {}
    companies = get_company_data_from_source(source)
    for s in companies:
        # if key is `Headquarters`, strip off ciry and only look at state/country
        if key == FinSymbolsKeys.HEADQUARTERS:
            new_key = s[key].split(',')[-1].strip().split('[')[0]
            # handle Wikipedioa inconsistencies
            if new_key == 'UT':
                new_key = 'Utah'
            elif new_key == 'UK':
                new_key = 'United Kingdom'
            elif new_key == 'Netherlands':
                new_key = 'Kingdom of the Netherlands'
        else:
            new_key = s[key]
        if new_key not in key_set:
            key_set[new_key] = []
        # add symbol to key list
        key_set[new_key].append(s[FinSymbolsKeys.SYMBOL])

    # return list of tuples
    return [(k, key_set[k]) for k in key_set]

def get_data_for_symbol(symbol, data_keys=STANDARDQUOTE):
    return get_quote(symbol, data_keys)

def get_data_for_symbols(symbol_list, data_keys=STANDARDQUOTE):
    return get_quotes(symbol_list, data_keys)

def get_historic_data_for_symbol(symbol, num_days, enddate=datetime.today(), key=None):
    data = get_number_of_historical_quotes(symbol, num_days, enddate)
    if key is not None:
        data = [x[key] for x in data]
    return data