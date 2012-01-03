'''
Created on Nov 7, 2011

@author: ppa
'''
from ultrafinance.backTest.metric.baseMetric import BaseMetric

import logging
LOG = logging.getLogger()

class HighestMetric(BaseMetric):
    ''' Highest metric class '''

    def __init__(self):
        ''' constructor '''
        super(HighestMetric, self).__init__()
        self.__highest = 0
        self.__time = None

    def getHighest(self):
        ''' get highest '''
        return self.__highest

    def record(self, curTime):
        ''' keep record of the account '''
        totalValue = self.account.getTotalValue()
        if totalValue > self.__highest:
            self.__highest = totalValue
            self.__time = curTime

    def printResult(self):
        ''' print result '''
        LOG.debug("Highest account value %.2f at %s" % (self.__highest, self.__time) )
