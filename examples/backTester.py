'''
Created on Dec 3, 2011

@author: ppa
'''

from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.btUtil import OUTPUT_PREFIX
from ultrafinance.backTest.tickSubscriber.strategies.strategyFactory import StrategyFactory
from ultrafinance.backTest.tradingCenter import TradingCenter
from ultrafinance.backTest.tickFeeder import TickFeeder
from ultrafinance.backTest.tradingEngine import TradingEngine
from ultrafinance.backTest.accountManager import AccountManager
from ultrafinance.ufConfig.pyConfig import PyConfig
from ultrafinance.dam.DAMFactory import DAMFactory
from ultrafinance.backTest.stateSaver.stateSaverFactory import StateSaverFactory
from ultrafinance.backTest.appGlobal import appGlobal
from ultrafinance.backTest.constant import CONF_STRATEGY, CONF_STRATEGY_NAME, CONF_APP_MAIN, \
    CONF_METRIC_NAMES, STOP_FLAG, TRADE_TYPE, CONF_TRADE_TYPE, \
    CONF_INPUT_SECTION, CONF_DAM, CONF_SYMBOL, \
    CONF_OUTPUT_SECTION, CONF_SAVER

from threading import Thread
import logging
import logging.config
LOG = logging.getLogger()

class BackTester(object):
    ''' back testing '''
    CASH = 1000000 #  a million to start

    def __init__(self):
        self.__config = PyConfig()
        self.__accountManager = AccountManager()
        self.__tickFeeder = TickFeeder()
        self.__tradingCenter = TradingCenter()
        self.__tradingEngine = TradingEngine()
        self.__saver = None

    def setup(self):
        ''' setup '''
        self.__config.setSource("backtest_period.ini")
        appGlobal[TRADE_TYPE] = self.__config.getOption(CONF_APP_MAIN, CONF_TRADE_TYPE)
        appGlobal[STOP_FLAG] = False

        self.setupLog()
        self.setupTradingCenter()
        self.setupTickFeeder()
        self.setupSaver()
        self.setupTradingEngine()

        #wire things together
        self.setupStrategy()
        self.__tickFeeder.tradingCenter = self.__tradingCenter
        self.__tradingEngine.tickProxy = self.__tickFeeder
        self.__tradingEngine.orderProxy = self.__tradingCenter
        self.__tradingCenter.accountManager = self.__accountManager
        self.__tradingEngine.saver = self.__saver
        self.__accountManager.saver = self.__saver

    def setupLog(self):
        ''' setup logging '''
        logging.config.fileConfig(self.__config.getFullPath())

    def setupTradingCenter(self):
        self.__tradingCenter.start = 0
        self.__tradingCenter.end = None

    def setupTickFeeder(self):
        ''' setup tickFeeder'''
        dam = self.createDam()
        self.__tickFeeder.addSource(dam)

    def createDam(self):
        ''' setup Dam'''
        damName = self.__config.getOption(CONF_INPUT_SECTION, CONF_DAM)
        setting = self.__config.getSection(CONF_INPUT_SECTION)
        dam = DAMFactory.createDAM(damName, setting)
        dam.setSymbol(self.__config.getOption(CONF_APP_MAIN, CONF_SYMBOL))

        return dam

    def setupSaver(self):
        ''' setup Saver '''
        saverName = self.__config.getOption(CONF_OUTPUT_SECTION, CONF_SAVER)
        setting = self.__config.getSection(CONF_OUTPUT_SECTION)
        if saverName:
            self.__saver = StateSaverFactory.createStateSaver(saverName, setting)

    def setupTradingEngine(self):
        ''' setup trading engine '''
        pass

    def setupStrategy(self):
        ''' setup tradingEngine'''
        strategy = StrategyFactory.createStrategy(self.__config.getOption(CONF_STRATEGY, CONF_STRATEGY_NAME),
                                                  self.__config.getSection(CONF_STRATEGY))

        metricNames = [name.strip() for name in self.__config.getOption(CONF_APP_MAIN, CONF_METRIC_NAMES).split(',') ]

        #associate account
        accountId = self.__accountManager.createAccountWithMetrix(metricNames, BackTester.CASH)
        strategy.accountId = accountId

        #register on trading engine
        strategy.tradingEngine = self.__tradingEngine
        self.__tradingEngine.register(strategy)

    def execute(self):
        ''' run backtest '''
        #start trading engine
        thread = Thread(target = self.__tradingEngine.runListener, args = ())
        thread.start()

        #start tickFeeder
        self.__tickFeeder.execute()

    def printResult(self):
        ''' print result'''
        for accountId, metrix in self.__accountManager.getMetrix().items():
            account = self.__accountManager.getAccount(accountId)
            LOG.debug("account %s" % account)
            LOG.debug([str(order) for order in account.orderHistory])
            for metric in metrix:
                metric.printResult()

if __name__ == "__main__":
    backTester = BackTester()
    backTester.setup()
    backTester.execute()
    backTester.printResult()
