'''
Created on Nov 8, 2011

@author: ppa
'''
from ultrafinance.metric.baseMetric import BaseMetric

import logging
LOG = logging.getLogger()

class LowestMetric(BaseMetric):
    ''' Lowest metric class '''

    def __init__(self):
        ''' constructor '''
        super(LowestMetric, self).__init__()
        self.__lowest = None
        self.__time = None

    def getLowest(self):
        ''' get highest '''
        return self.__lowest

    def record(self, curTime):
        ''' keep record of the account '''
        totalValue = self.account.getTotalValue()
        if not None or totalValue < self.__lowest:
            self.__lowest = totalValue
            self.__time = curTime

    def printResult(self):
        ''' print result '''
        LOG.debug("Lowest account value %.2f at %s" % (self.__lowest, self.__time) )
