'''
Created on May 26, 2012

@author: ppa
'''
import numpy
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