from finsymbols import get_nasdaq_symbols, get_nyse_symbols, get_sp500_symbols

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

def get_company_data(source):
    dispatch = { SymbolList.NASDAQ: get_nasdaq_symbols,
                SymbolList.SP500: get_sp500_symbols,
                SymbolList.NYSE: get_nyse_symbols }
    return dispatch[source]()

def get_symbol_list(source):
    return [s[FinSymbolsKeys.SYMBOL] for s in get_company_data(source)]

def get_symbols_by_key(key, source=SymbolList.SP500):
    key_set = {}
    companies = get_company_data(source)
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
