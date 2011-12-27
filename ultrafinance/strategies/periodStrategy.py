'''
Created on Dec 25, 2011

@author: ppa
'''
from ultrafinance.model import Side, Order
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.strategies.baseStrategy import BaseStrategy

import logging
LOG = logging.getLogger(__name__)

class PeriodStrategy(BaseStrategy):
    ''' trading center '''
    def __init__(self, configDict):
        ''' constructor '''
        super(PeriodStrategy, self).__init__("periodStrategy")
        self.configDict = configDict

        assert int(configDict['period']) >= 1
        self.perAmount = 1000 # buy $100p per period
        self.period = int(configDict['period'])
        self.symbol = configDict['symbolRe']
        self.counter = 0

    def increaseAndCheckCounter(self):
        ''' increase counter by one and check whether a period is end '''
        self.counter += 1
        self.counter %= self.period
        if not self.counter:
            return True
        else:
            return False

    def consume(self, tickDict):
        ''' consume ticks '''
        #should only have one symbol in dict
        for symbol, tick in tickDict.iteritems():
            print "period strategy get symbol %s with tick %s" % (symbol, tick)

        if self.accountId is None:
            raise UfException(Errors.NONE_ACCOUNT_ID,
                              "Account id is none")

        assert self.symbol in tickDict.keys()
        tick = tickDict[self.symbol]

        if self.increaseAndCheckCounter():
            self.tradingCenter.placeOrder(Order(accountId = self.accountId,
                                                side = Side.BUY,
                                                symbol = self.symbol,
                                                price = tick.close,
                                                share = self.perAmount/float(tick.close) ))


