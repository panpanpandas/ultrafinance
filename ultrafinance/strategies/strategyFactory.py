'''
Created on Dec 26, 2011

@author: ppa
'''

from ultrafinance.strategies.periodStrategy import PeriodStrategy

from ultrafinance.lib.errors import Errors, UfException

class StrategyFactory:
    ''' Strategy factory '''
    strategyDict = {'period': PeriodStrategy}

    @staticmethod
    def createStrategy(name, configDict):
        ''' create a metric '''
        if name not in StrategyFactory.strategyDict:
            raise UfException(Errors.INVALID_STRATEGY_NAME,
                              "Strategy name is invalid %s" % name)
        return StrategyFactory.strategyDict[name](configDict)

    @staticmethod
    def getAvailableTypes(self):
        ''' return all available types '''
        return StrategyFactory.metricDict.keys()
