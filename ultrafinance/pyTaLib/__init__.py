''' ultraFinance TA-Lib implementation'''
from collections import deque

def min():
    ''' Lowest value over a specified period '''
    pass

def max():
    ''' Highest value over a specified period '''
    pass

def macd():
    ''' Moving Average Convergence/Divergence '''
    pass

def stddev():
    ''' Standard Deviation '''
    pass

def beta():
    ''' beta '''
    pass

''' refer to http://rosettacode.org/wiki/Averages/Simple_moving_average#Python '''
class Sma(object):
    ''' simple moving average '''
    def __init__(self, period):
        assert period == int(period) and period > 0, "Period must be an integer > 0"
        self.__period = period
        self.__stream = deque()

    def __call__(self, n):
        self.__stream.append(n)
        if len(self.__stream) > self.__period:
            self.__stream.popleft()

        return sum(self.__stream) / float(len(self.__stream) )
