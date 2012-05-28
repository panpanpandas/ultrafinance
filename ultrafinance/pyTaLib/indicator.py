'''
Created on May 26, 2012

@author: ppa
'''
import numpy
from math import *

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
        returns.append((float(post) - float(pre)) / pre)
        pre = post

    return sqrt(n) * mean(returns) / stddev(returns)

