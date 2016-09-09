from tradingtools.technicals import ema, sma

data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
data = data + data + data
data = data + [10, 20, 30]
print 'SMA: ', str(sma(data, 22))
print 'EMA: ', str(ema(data, 22))