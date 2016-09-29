from numpy import sign
from numpy import abs, subtract

def _slope(x1, x2, n):
    if x1 == 0:
        return float('inf') * sign(x2)
    if n == 0:
        raise ZeroDivisionError('Calculating zlope: n must not be zero.')
    return 100.0 * ((x2 - x1) / float(n)) / float(abs(x1))

def trend_length_and_slope(data):
    #todo warn or exception
    if len(data) < 2:
        return 0, 0
    if len(data) == 2:
        return 1, data[1] - data[0]
    zcd = zero_crossings(subtract(data[1:], data[:-1]))
    if zcd == []:
        return len(data) - 1, _slope(data[0], data[1], len(data) - 1)
    length = len(data) - zcd[-1] - 1
    return length, _slope(data[zcd[-1]], data[-1], length)

def zero_crossings(data):
    """
    Returns list of indexes where data crosses zero. That is, from negative to positive
    and positive to negative. Zeros are ignored.
    :param data:
    :return: List of Int64
    """
    signs = sign(data)
    zcd = []
    last_sign = None
    for n in range(len(data)):
        if signs[n] != 0:
            if last_sign is None:
                last_sign = signs[n]
            elif last_sign != signs[n]:
                zcd.append(n)
                last_sign = signs[n]
    return zcd