'''
Created on Feb 26, 2010

@author: ppa
'''
from ultrafinance.processChain.baseModule import BaseModule
from ultrafinance.lib.tradingStrategyFactory import TradingStrategyFactory
from ultrafinance.lib.tradingStrategy.automaticInvestmentPlan import adjustFixAmountPerPeriod
from ultrafinance.lib.tradingStrategy.automaticInvestmentPlan import fixAmountPerPeriod
from ultrafinance.lib.tradingStrategy.automaticInvestmentPlan import fixAmountPerPeriodWithAddtionWhenDrop

import logging
LOG = logging.getLogger(__name__)

class TradingStrategyProcessor(BaseModule):
    ''' Calculate average and standard deviation '''
    def __init__(self):
        ''' constructor '''
        super(TradingStrategyProcessor, self).__init__()

    def execute(self, dateValueList):
        ''' processing input'''
        output = {}
        tradingStrategyFactory = TradingStrategyFactory(fixAmountPerPeriod)
        output['fixAmountPerPeriod'] = tradingStrategyFactory.calculateReturn(dateValueList, 1)

        tradingStrategyFactory = TradingStrategyFactory(fixAmountPerPeriodWithAddtionWhenDrop)
        output['fixAmountPerPeriodWithAddtionWhenDrop'] = tradingStrategyFactory.calculateReturn(dateValueList, 1, 5)

        tradingStrategyFactory = TradingStrategyFactory(adjustFixAmountPerPeriod)
        output['adjustFixAmountPerPeriod'] = tradingStrategyFactory.calculateReturn(dateValueList, 5, 5)
        return output