from tradingtools.technicals import ema, sma, macd, macd_for_symbol

data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
data = data + data + data + data + data + data + data + data + data + data
data = data + [10, 20, 30]
print 'SMA: ', str(sma(data, 22)[-10:])
print 'EMA: ', str(ema(data, 22)[-10:])
m,s,h = macd(data)
print 'MACD: ', str(m[-10:])
print 'Signal: ', str(s[-10:])
print 'Historgram', str(h[-10:])
print 'MACD for GOOGL:', str(macd_for_symbol('GOOGL', num_days=1))

