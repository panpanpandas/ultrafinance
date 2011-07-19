'''
Created on Feb 26, 2011

@author: ppa
'''
from ultrafinance.lib.errors import ufException, Errors
import traceback

import logging
LOG = logging.getLogger(__name__)

class TradingStrategyFactory():
    ''' Factory method for trading Strategies '''
    def __init__(self, strategy):
        ''' constructor '''
        self.strategy = strategy

    def calculateReturn(self, dateValues, *args):
        try:
            return self.strategy(dateValues, *args)

        except ufException as excep:
            raise excep
        except BaseException as excep:
            raise ufException(Errors.UNKNOWN_ERROR, "tradingStrategyFactory.calculateReturn got unknown error %s" % traceback.print_exc())