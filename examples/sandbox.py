from tradingtools.technicals import ema_for_symbol, \
    sma_for_symbol, \
    macd_for_symbol, \
    on_balance_volume_for_symbol

num_days = 2
window_size = 10
print 'SMA for GOOGL: ', str(sma_for_symbol('GOOGL', num_days=num_days, window_size=window_size))
print 'EMA for GOOGL: ', str(ema_for_symbol('GOOGL', num_days=num_days, window_size=window_size))
print 'MACD for GOOGL: ', str(macd_for_symbol('GOOGL', num_days=num_days))
print 'OBV for GOOGL: ', str(on_balance_volume_for_symbol('GOOGL', num_days=num_days))
