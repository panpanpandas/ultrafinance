'''
Created on Dec 25, 2011

@author: ppa
'''
from ultrafinance.tickFeeder.tickSubsriber import TickSubsriber

import logging
LOG = logging.getLogger(__name__)

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
