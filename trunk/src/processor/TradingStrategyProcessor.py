'''
Created on Feb 26, 2010

@author: ppa
'''
from BaseModule import BaseModule
from lib.TradingStrategyFactory import TradingStrategyFactory

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
        tradingStrategyFactory = TradingStrategyFactory('adjustFixAmountPerPeriod')
        ret = tradingStrategyFactory.calculateReturn(dateValuesDict, [1, 5])
        print 'adjustFixAmountPerPeriod %s' %ret
        return ret