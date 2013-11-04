'''
Created on May 26, 2012

@author: ppa
'''
import numpy
from numpy import polyval, polyfit
from math import sqrt
from collections import deque

def mean(array):
    ''' average '''
    return numpy.mean(array, axis = 0)

def stddev(array):
    ''' Standard Deviation '''
    return numpy.std(array, axis = 0)

def sharpeRatio(array, n = 252):
    ''' calculate sharpe ratio '''
    #precheck
    if (array is None or len(array) < 2 or n < 1):
        return -1

    returns = []
    pre = array[0]
    for post in array[1:]:
        returns.append((float(post) - float(pre)))
        pre = post

    return sqrt(n) * mean(returns) / stddev(returns)

''' refer to http://rosettacode.org/wiki/Averages/Simple_moving_average#Python '''
class Sma(object):
    def __init__(self, period):
        assert period == int(period) and period > 0, "Period must be an integer > 0"
        self.__period = period
        self.__stream = deque()
        self.__value = None

    def getLastValue(self):
        return self.__value

    def __call__(self, n):
        self.__stream.append(n)
        if len(self.__stream) > self.__period:
            self.__stream.popleft()
            self.__value = sum(self.__stream) / float(len(self.__stream) )
            return self.__value
        else:
            return None


class LinearRegression(object):
    def __init__(self, period):
        assert period == int(period) and period > 0, "Period must be an integer > 0"
        self.__period = period
        self.__stream = deque()
        self.__value = None

    def getLastValue(self):
        return self.__value

    def __call__(self, n):
        self.__stream.append(n)
        if len(self.__stream) > self.__period:
            self.__stream.popleft()
            (m, b) = polyfit(range(0, self.__period), self.__stream, 1)
            self.__value = polyval([m, b], self.__period)
            return self.__value
        else:
            return None


class MovingLow(object):
    def __init__(self, period):
        assert period == int(period) and period > 0, "Period must be an integer > 0"
        self.__period = period
        self.__stream = deque()
        self.__value = None

    def getLastValue(self):
        return self.__value

    def __call__(self, n):
        self.__stream.append(n)
        if len(self.__stream) > self.__period:
            self.__stream.popleft()
            self.__value = min(self.__stream)
            return self.__value
        else:
            return None


class Vwap(object):
    def __init__(self, period):
        assert period == int(period) and period > 0, "Period must be an integer > 0"
        self.__period = period
        self.__prices = deque()
        self.__volumes = deque()
        self.__value = None

    def getLastValue(self):
        return self.__value

    def __call__(self, price, volume):
        if volume <= 0 or price <= 0:
            return

        self.__prices.append(price)
        self.__volumes.append(volume)

        if len(self.__prices) > self.__period:
            self.__prices.popleft()
            self.__volumes.popleft()
            self.__value = sum(self.__prices[i] * self.__volumes[i] for i in range(len(self.__prices))) / float(sum(self.__volumes) )
            return self.__value
        else:
            return None