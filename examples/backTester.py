'''
Created on Dec 3, 2011

@author: ppa
'''

from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.metric.metricFactory import MetricFactory
from ultrafinance.backTest.tickSubscriber.strategies.strategyFactory import StrategyFactory
from ultrafinance.backTest.tradingCenter import TradingCenter
from ultrafinance.backTest.tickFeeder import TickFeeder
from ultrafinance.configLib.pyConfig import PyConfig
from ultrafinance.dam.DAMFactory import DAMFactory

#from ultrafinance.strategies.movStrategy import MovStrategy

import logging
import logging.config
LOG = logging.getLogger()

class BackTester(object):
    CASH = 1000000 #  a million to start

    ''' back testing '''
    def __init__(self):
        self.__tradingCenter = TradingCenter()
        self.__config = PyConfig()
        self.__strategyFactory = StrategyFactory()
        self.__metricFactory = MetricFactory()
        #self.__metricName = ["lowest", "highest"]
        self.__tickFeeder = TickFeeder()
        self.__strategies = []
        self.__dam = None

    def setup(self):
        ''' set up metrics '''
        self.__config.setSource("backtest_period.ini")
        self.setupLog()
        self.setupTradingCenter()
        self.setupDam()
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
        metricNames = [name.strip() for name in self.__config.getOption('app_main', "metricNames").split(',') ]
        self.__tradingCenter.setMetricNames(metricNames)

    def setupMetrix(self):
        ''' setup  metrix '''
        for strategy in self.__strategies:
            accountId = self.__tradingCenter.createAccountWithMetrix(BackTester.CASH)
            strategy.accountId = accountId

    def setupLog(self):
        ''' setup logging '''
        logging.config.fileConfig(self.__config.getFullPath())

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
        for accountId, metrix in self.__tradingCenter.getMetrix().items():
            account = self.__tradingCenter.getCopyAccount(accountId)
            LOG.debug("account %s" % account)
            LOG.debug([str(order) for order in account.orderHistory])
            for metric in metrix:
                metric.printResult()


if __name__ == "__main__":
    backTester = BackTester()
    backTester.setup()
    backTester.execute()
    backTester.printResult()
