'''
Created on Dec 25, 2011

@author: ppa
'''
from ultrafinance.tickFeeder.tickSubsriber import TickSubsriber
from ultrafinance.lib.errors import Errors, UfException

import logging
LOG = logging.getLogger()

class BaseStrategy(TickSubsriber):
    ''' trading center '''
    def __init__(self, name):
        ''' constructor '''
        super(BaseStrategy, self).__init__(name)
        self.accountId = None
        self.tradingCenter = None
        self.configDict = {}

    def subRules(self):
        ''' override function '''
        return (self.configDict['symbolRe'], None)

    def preConsume(self, ticks):
        ''' override function '''
        if self.accountId is None:
            raise UfException(Errors.NONE_ACCOUNT_ID,
                              "Account id is none")

