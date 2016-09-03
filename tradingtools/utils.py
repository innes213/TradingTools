from finsymbols import get_sp500_symbols

class FinSymbolsKeys:
    SYMBOL = 'symbol'
    INDUSTRY = 'industry'
    HEADQUARTERS = 'headquarters'
    SECTOR = 'sector'
    COMPANY = 'company'

def get_sp500_symbol_list():
    return [s[FinSymbolsKeys.SYMBOL] for s in get_sp500_symbols()]

def get_sp500_symbols_by_industry():
    return get_sp500_symbols_by_key(FinSymbolsKeys.INDUSTRY)

def get_sp500_symbols_by_sector():
    return get_sp500_symbols_by_key(FinSymbolsKeys.SECTOR)

def get_sp500_symbols_by_region():
    return get_sp500_symbols_by_key(FinSymbolsKeys.HEADQUARTERS)

def get_sp500_symbols_by_key(key):
    key_set = {}
    symbols = get_sp500_symbols()
    for s in symbols:
        # if key is `Headquarters`, strip off ciry and only look at state/country
        if key == FinSymbolsKeys.HEADQUARTERS:
            new_key = s[key].split(',')[-1].strip().split('[')[0]
            # handle Wikipedioa inconsistencies
            if new_key == 'UT':
                new_key = 'Utah'
            else:
                if new_key == 'UK':
                    new_key = 'United Kingdom'
                else:
                    if new_key == 'Netherlands':
                        new_key = 'Kingdom of the Netherlands'
        else:
            new_key = s[key]
        if new_key not in key_set:
            key_set[new_key] = []
        # add symbol to key list
        key_set[new_key].append(s[FinSymbolsKeys.SYMBOL])

    # return list of tuples
    return [(k, key_set[k]) for k in key_set]
