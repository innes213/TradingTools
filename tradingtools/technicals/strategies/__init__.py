from tradingtools.technicals.indicators.EMA import EMA

from numpy import max, min, subtract

def model_ema_golden_death_cross(open_data, close_data, slow_window, fast_window, num_periods):

    # accounting setup
    share_count = 0
    cash = 0
    count = 0
    # get fast and slow EMA
    fast_result = EMA(window_size=fast_window).calculate(close_data[-(5*slow_window + num_periods):])[-num_periods:]
    slow_result = EMA(window_size=slow_window).calculate(close_data[-(5*slow_window + num_periods):])[-num_periods:]
    offset = len(open_data) - num_periods
    delta = subtract(slow_result, fast_result)
    # step through delta[:-1] from oldest to newest, looking at 2 at a time
    for n in range(1, len(delta) - 1):
        if delta[n] * delta[n-1] < 0:
            count += 1
            if delta[n] >= 0:
                share_count -= 1
                #print 'selling at $%3.2f on day %i' % (open_data[offset+n+1], n+1)
                cash += open_data[offset+n+1]
            else:
                share_count += 1
                #print 'buying at $%3.2f on day %i' % (open_data[offset+n+1], n+1)
                cash -= open_data[offset+n+1]
    # when at end of data, rectify
    #print 'Rectifying %i shares at $%3.2f' % (share_count, open_data[-1])
    cash += share_count * open_data[-1]
    return cash, count

def ema_golden_death_cross_sweep(open_data, close_data, num_periods, max_window=400):

    data_length = len(open_data)
    if data_length < num_periods:
        return None
    trials = []
    #gather some info
    max_window_size = min([(data_length - num_periods) / 6, max_window])

    for fast_window in range(3, max_window_size / 4):
        for slow_window in range(fast_window + 1, fast_window * 4, 2):
            cash, count = model_ema_golden_death_cross(open_data, close_data, slow_window, fast_window, num_periods)
            trials.append((cash, slow_window, fast_window, count))

    return trials
