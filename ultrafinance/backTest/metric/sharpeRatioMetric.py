'''
Created on Jan 10, 2012

@author: ppa
Note: this one only works for quote and calculate yearly sharp ratio
'''
from ultrafinance.backTest.metric.baseMetric import BaseMetric
from ultrafinance.pyTaLib import stddev, mean
from ultrafinance.lib.errors import Errors, UfException

import logging
LOG = logging.getLogger()

class SharpeRatioMetric(BaseMetric):
    ''' SharpeRatio metric class '''

    def __init__(self):
        ''' constructor '''
        super(SharpeRatioMetric, self).__init__()
        self.__riskFreeReturn = 0
        self.__calculated = False
        self.__accountValues = []
        self.__sharpeRatio = 0
        self.__interval = 250

    def setRiskFreeReturn(self, riskFreeReturn):
        ''' set risk free return '''
        if 0 <= riskFreeReturn < 1:
            self.__riskFreeReturn = riskFreeReturn
        else:
            raise UfException(Errors.INVALID_RISK_FREE_RETURN,
                              "risk free return must between 0 and 1")

    def setInterval(self, interval):
        ''' set interval '''
        self.__interval = interval

    def getSharpeRatio(self):
        ''' get highest '''
        if not self.__calculated:
            returns = []

            if len(self.__accountValues) > 1:
                pre = self.__accountValues[0]
                for post in self.__accountValues[1:self.__interval:]:
                    if pre:
                        oneReturn = (float(post) - float(pre)) / float(pre)
                        returns.append(oneReturn)
                    else:
                        returns.append(0)
                    pre = post

                std = stddev(returns)
                return mean(returns)/std
            else:
                return 0
        else:
            self.__calculated = True
            return self.__sharpeRatio

    def record(self, curTime):
        ''' keep record of the account '''
        totalValue = self.account.getTotalValue()
        self.__accountValues.append(totalValue)
        self.__calculated = False

    def printResult(self):
        ''' print result '''
        LOG.debug("Sharpe Ratio is %.2f" % self.getSharpeRatio())
