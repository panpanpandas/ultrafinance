'''
Created on Nov 8, 2011

@author: ppa
'''
from ultrafinance.metric.baseMetric import BaseMetric

import time

class LowestMetric(BaseMetric):
    ''' Lowest metric class '''

    def __init__(self):
        ''' constructor '''
        self.__lowest = 0
        self.__time = None

    def getLowest(self):
        ''' get highest '''
        return self.__lowest

    def record(self, account):
        ''' keep record of the account '''
        totalValue = account.getTotalValue()
        if totalValue < self.__lowest:
            self.__lowest = totalValue
            self.__time = time.ctime()

    def printResult(self):
        ''' print result '''
        print "Lowest account value %.2f at %s" % (self.__lowest, self.__time)
