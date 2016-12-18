from tradingtools.technicals.indicators.EMA import EMA
from tradingtools.technicals.indicators.MACD import MACD
from tradingtools.technicals.indicators.SMA import SMA
from tradingtools.analysis import zero_crossings
from numpy import abs, max, min, multiply, sign, subtract, sum, zeros_like

def model_trades(price_data, trade_vector):
    """
    Returns the cash value given price data and a list of of asset quantities to trade
    as well as the number of transactions (sum of buy and sells)
    :param price_data: array of floats representing the price of an asset
    :param trade_vector: array of ints representing the number of
    :return:
    """
    if price_data is None or trade_vector is None:
        raise ValueError("One or more arrays is None")
    if len(price_data) != len(trade_vector):
        raise ValueError("Array lengths must match! price_data: %i, trade_vector: %i" % (len(price_data), len(trade_vector)))
    profit =  -1 * sum(multiply(price_data, trade_vector))
    # settle up last period by calculating value of open positions
    profit += price_data[-1] * sum(trade_vector)
    return profit, sum(abs(sign(trade_vector)))


def model_ema_golden_death_cross(open_data, close_data, slow_window, fast_window, num_periods):
    # get fast and slow EMA
    fast_result = EMA(window_size=fast_window).calculate(close_data[-(5*slow_window + num_periods):])[-num_periods:]
    slow_result = EMA(window_size=slow_window).calculate(close_data[-(5*slow_window + num_periods):])[-num_periods:]
    delta = subtract(fast_result, slow_result)
    # find zero-crossings,
    zcd = zero_crossings(delta[:-1])
    shares_to_trade = zeros_like(delta)
    for z in zcd:
        shares_to_trade[z+1] = sign(delta[z])  # 1 share per trade
    # model the trades
    profit, count = model_trades(open_data[-num_periods:], shares_to_trade)
    #settle up on last day
    profit += open_data[-1] * sum(shares_to_trade)
    return profit, count

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

def model_sma_golden_death_cross(open_data, close_data, slow_window, fast_window, num_periods):
    # get fast and slow EMA
    fast_result = SMA(window_size=fast_window).calculate(close_data[-(fast_window + num_periods - 1):])
    slow_result = SMA(window_size=slow_window).calculate(close_data[-(slow_window + num_periods - 1):])
    delta = subtract(fast_result, slow_result)
    # find zero-crossings,
    zcd = zero_crossings(delta[:-1])
    shares_to_trade = zeros_like(delta)
    for z in zcd:
        shares_to_trade[z+1] = sign(delta[z])  # 1 share per trade
    # model the trades
    profit, count = model_trades(open_data[-num_periods:], shares_to_trade)
    #settle up on last day
    profit += open_data[-1] * sum(shares_to_trade)
    return profit, count

def sma_golden_death_cross_sweep(open_data, close_data, num_periods, max_window=400):

    data_length = len(open_data)
    if data_length < num_periods:
        return None
    trials = []
    #gather some info
    max_window_size = min([(data_length - num_periods), max_window])

    for fast_window in range(3, max_window_size / 4):
        for slow_window in range(fast_window + 1, fast_window * 4, 2):
            cash, count = model_sma_golden_death_cross(open_data, close_data, slow_window, fast_window, num_periods)
            trials.append((cash, slow_window, fast_window, count))

    return trials

def get_sma_crossing_trade_signals(close_data, window_size):
    sma = SMA(window_size=window_size).calculate(close_data)
    delta = subtract(close_data[window_size-1:],sma)
    # find zero-crossings, where price crosses sma
    zcd = zero_crossings(delta[:-1])
    trade_vector = zeros_like(delta)
    # buy/sell on next period after signal, 1 share per trade
    for z in zcd:
        trade_vector[z+1] = sign(delta[z])
    return trade_vector

def get_macd_crossing_trade_signals(close_data, slow_window, fast_window, signal_window, num_periods):
    # get fast and slow EMA
    _, _, delta = MACD(slow_window_size=slow_window, fast_window_size=fast_window, signal_window_size=signal_window).calculate(close_data[-(5*slow_window + num_periods):])
    delta = delta[-num_periods:]
    # find zero-crossings
    zcd = zero_crossings(delta[:-1])
    trade_vector = zeros_like(delta)
    for z in zcd:
        trade_vector[z+1] = sign(delta[z])  # buy/sell on next period after signal, 1 share per trade
    return trade_vector
