'''
Created on Dec 3, 2011

@author: ppa
'''

from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.metric.metricFactory import MetricFactory
from ultrafinance.strategies.strategyFactory import StrategyFactory
from ultrafinance.tradingCenter import TradingCenter
from ultrafinance.tickFeeder import TickFeeder
from ultrafinance.tickFeeder.subManager import SubManager
from ultrafinance.config.pyConfig import PyConfig
from ultrafinance.dam.DAMFactory import DAMFactory

#from ultrafinance.strategies.movStrategy import MovStrategy

import logging
LOG = logging.getLogger(__name__)

class BackTester(object):
    CASH = 1000000 #  a million to start

    ''' back testing '''
    def __init__(self):
        self.__tradingCenter = TradingCenter()
        self.__config = PyConfig()
        self.__strategyFactory = StrategyFactory()
        self.__metricFactory = MetricFactory()
        self.__metricName = ["lowest", "highest"]
        self.__tickFeeder = TickFeeder()
        self.__strategies = []
        self.__dam = None

    def setup(self):
        ''' set up metrics '''
        self.__config.setSource("backtest_mov.ini")

        self.setupDam()
        self.setupLog()
        self.setupStrategies()
        self.setupMetrix()
        self.setupTickFeeder()

    def setupDam(self):
        ''' set up Dam'''
        damFactory = DAMFactory()
        self.__dam = damFactory.createDAM('hbase')
        self.__dam.setSymbol('EBAY')

    def setupTradingCenter(self):
        self.__tradingCenter.start = 0
        self.__tradingCenter.end = None

    def setupMetrix(self):
        ''' setup  metrix '''
        for strategy in self.__strategies:
            accountId = self.__tradingCenter.createAccount(BackTester.CASH)
            # associate accoutnId with strategy
            strategy.accountId = accountId
            # associate metrix with account
            self.__tradingCenter.addMetrixToAccount([self.__metricFactory.createMetric(name) for name in self.__metricName],
                                                    accountId)


    def setupLog(self):
        pass

    def setupStrategies(self):
        ''' set up strategies '''
        strategy = self.__strategyFactory.createStrategy("period", {'symbolRe': "EBAY", "period": 30})
        strategy.tradingCenter = self.__tradingCenter
        self.__strategies.append(strategy)

    def setupTickFeeder(self):
        ''' set up tickFeeder'''
        self.__tickFeeder.addSource(self.__dam)
        self.__tickFeeder.register(self.__tradingCenter)
        for strategy in self.__strategies:
            self.__tickFeeder.register(strategy)

        self.__tickFeeder.inputType = 'quote'

    def execute(self):
        ''' run backtest '''
        self.__tickFeeder.inputType = 'quote'
        self.__tickFeeder.execute()

    def printResult(self):
        ''' print result'''
        for account in self.__tradingCenter.getAccounts('.*'):
            print account.orderHistory

if __name__ == "__main__":
    backTester = BackTester()
    backTester.setup()
    backTester.execute()
    backTester.printResult()
