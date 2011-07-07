'''
Created on Feb 26, 2010

@author: ppa
'''
from ultrafinance.processChain.baseModule import BaseModule
from ultrafinance.lib.tradingStrategyFactory import TradingStrategyFactory

import logging
LOG = logging.getLogger(__name__)

class TradingStrategyProcessor(BaseModule):
    ''' Calculate average and standard deviation '''
    def __init__(self):
        ''' constructor '''
        super(TradingStrategyProcessor, self).__init__()

    def execute(self, dateValuesDict):
        ''' processing input'''
        tradingStrategyFactory = TradingStrategyFactory('fixAmountPerPeriod')
        ret = tradingStrategyFactory.calculateReturn(dateValuesDict, 1)
        print 'fixAmountPerPeriod %s' %ret
        tradingStrategyFactory = TradingStrategyFactory('fixAmountPerPeriodWithAddtionWhenDrop')
        ret = tradingStrategyFactory.calculateReturn(dateValuesDict, 1, 5)
        print 'fixAmountPerPeriodWithAddtionWhenDrop %s' %ret
        tradingStrategyFactory = TradingStrategyFactory('adjustFixAmountPerPeriod')
        ret = tradingStrategyFactory.calculateReturn(dateValuesDict, 5, 5)
        print 'adjustFixAmountPerPeriod %s' %ret
        return ret