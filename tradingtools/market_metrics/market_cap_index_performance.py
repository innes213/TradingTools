'''
Created on July 3, 2016

@author: Rob Innes Hislop
'''

from ..technicals import performance_for_symbol

def market_cap_index_performance(dayranges=[1]):
    """
    Returns performance for daychanges for SP600, SP400 and SP500 index ETFs
    :param daychanges: List of number of days for which to calculate performance
    :return: List of tuples in form of (index, [performance for days])
    """
    output = []
    for idx in ('SLY','MDY','SPY'):
        perf = performance_for_symbol(idx,dayranges)
        output.append((idx,perf))
    return output
