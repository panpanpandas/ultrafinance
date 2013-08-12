'''
Created on Dec 3, 2011

@author: ppa
'''

from ultrafinance.backTest.tickSubscriber.strategies.strategyFactory import StrategyFactory
from ultrafinance.backTest.tradingCenter import TradingCenter
from ultrafinance.backTest.tickFeeder import TickFeeder
from ultrafinance.backTest.tradingEngine import TradingEngine
from ultrafinance.backTest.accountManager import AccountManager
from ultrafinance.ufConfig.pyConfig import PyConfig
from ultrafinance.dam.DAMFactory import DAMFactory
from ultrafinance.backTest.stateSaver.stateSaverFactory import StateSaverFactory
from ultrafinance.backTest.appGlobal import appGlobal
from ultrafinance.backTest.metric import MetricCalculator
from ultrafinance.backTest.indexHelper import IndexHelper
from ultrafinance.backTest.history import History
from ultrafinance.backTest.constant import *
import os
import sys

from threading import Thread

import traceback
import logging.config
import logging
LOG = logging.getLogger()

CONFIG_FILE = "backtest_smaPortfolio.ini"

class BackTester(object):
    ''' back testing '''
    CASH = 200000 #  1 million to start

    def __init__(self, startTickDate = 0, startTradeDate = 0):
        self.__config = PyConfig()
        self.__mCalculator = MetricCalculator()
        self.__symbolLists = []
        self.__accounts = []
        self.__startTickDate = startTickDate
        self.__startTradeDate = startTradeDate

    def setup(self):
        ''' setup '''
        LOG.debug("Loading config from %s" % CONFIG_FILE)
        self.__config.setSource(CONFIG_FILE)
        appGlobal[TRADE_TYPE] = self.__config.getOption(CONF_APP_MAIN, CONF_TRADE_TYPE)
        self.__config.override(CONF_STRATEGY, CONF_INIT_CASH, BackTester.CASH)
        self.__config.override(CONF_STRATEGY, CONF_START_TRADE_DATE, self.__startTradeDate)
        self._setupLog()
        self._loadSymbols()

    def _setupLog(self):
        ''' setup logging '''
        logging.config.fileConfig(self.__config.getFullPath())

    def _runOneTest(self, symbols):
        ''' run one test '''
        LOG.debug("Running backtest for %s" % symbols)
        runner = TestRunner(self.__config, self.__mCalculator, self.__accounts, symbols, self.__startTickDate)
        runner.runTest()

    def _loadSymbols(self):
        ''' find symbols'''
        symbolFile = self.__config.getOption(CONF_APP_MAIN, CONF_SYMBOL_FILE)
        assert symbolFile is not None, "%s is required in config file" % CONF_SYMBOL_FILE

        with open(os.path.join(self.__config.getDir(), symbolFile), "r") as f:
            for symbols in f:
                if symbols not in self.__symbolLists:
                    self.__symbolLists.append([symbol.strip() for symbol in symbols.split()])

        assert self.__symbolLists, "None symbol provided"

    def runTests(self):
        ''' run tests '''
        for symbols in self.__symbolLists:
            try:
                self._runOneTest(symbols)
            except KeyboardInterrupt:
                LOG.error("User Interrupted")
                sys.exit("User Interrupted")
            except BaseException as excp:
                LOG.error("Unexpected error when backtesting %s -- except %s, traceback %s" \
                          % (symbols, excp, traceback.format_exc(8)))

    def getLatestOrders(self, num = 10):
        ''' get latest orders'''
        orders = []
        for account in self.__accounts:
            orders.extend(account.orderHistory[-num:])

        return orders

    def getMetrics(self):
        ''' get alll metrics '''
        return self.__mCalculator.formatMetrics()

    def printMetrics(self):
        ''' print metrics '''
        LOG.info(self.getMetrics())

class TestRunner(object):
    ''' back testing '''
    def __init__(self, config, mCalculator, accounts, symbols, startTickDate):
        self.__accountManager = AccountManager()
        self.__accountId = None
        self.__tickFeeder = TickFeeder(start = startTickDate)
        self.__tradingCenter = TradingCenter()
        self.__tradingEngine = TradingEngine()
        self.__indexHelper = IndexHelper()
        self.__accounts = accounts
        self.__history = History()
        self.__saver = None
        self.__symbols = symbols
        self.__config = config
        self.__mCalculator = mCalculator

    def _setup(self):
        ''' setup '''
        self._setupTradingCenter()
        self._setupTickFeeder()
        self._setupSaver()

        #wire things together
        self._setupStrategy()
        self.__tickFeeder.tradingCenter = self.__tradingCenter
        self.__tradingEngine.tickProxy = self.__tickFeeder
        self.__tradingEngine.orderProxy = self.__tradingCenter
        self.__tradingCenter.accountManager = self.__accountManager
        self.__tradingEngine.saver = self.__saver
        self.__accountManager.saver = self.__saver

    def _setupTradingCenter(self):
        self.__tradingCenter.start = 0
        self.__tradingCenter.end = None

    def _setupTickFeeder(self):
        ''' setup tickFeeder'''
        self.__tickFeeder.indexHelper = self.__indexHelper
        self.__tickFeeder.hisotry = self.__history
        #set source dam
        for symbol in self.__symbols:
            sDam = self._createDam(symbol)
            self.__tickFeeder.addSource(sDam)

        #set index dam
        iSymbol = self.__config.getOption(CONF_APP_MAIN, CONF_INDEX)
        iDam = self._createDam(iSymbol)
        self.__tickFeeder.setIndexDam(iDam)

    def _createDam(self, symbol):
        ''' setup Dam'''
        damName = self.__config.getOption(CONF_INPUT_SECTION, CONF_DAM)
        setting = self.__config.getSection(CONF_INPUT_SECTION)
        dam = DAMFactory.createDAM(damName, setting)
        dam.setSymbol(symbol)

        return dam

    def _setupSaver(self):
        ''' setup Saver '''
        saverName = self.__config.getOption(CONF_OUTPUT_SECTION, CONF_SAVER)
        setting = self.__config.getSection(CONF_OUTPUT_SECTION)
        if saverName:
            self.__saver = StateSaverFactory.createStateSaver(saverName,
                                                              setting,
                                                              "%s_%s" % (self.__symbols,
                                                                         self.__config.getOption(CONF_STRATEGY, CONF_STRATEGY_NAME)))

    def _setupStrategy(self):
        ''' setup tradingEngine'''
        strategy = StrategyFactory.createStrategy(self.__config.getOption(CONF_STRATEGY, CONF_STRATEGY_NAME),
                                                  self.__config.getSection(CONF_STRATEGY))
        strategy.setSymbols(self.__symbols)
        strategy.indexHelper = self.__indexHelper
        strategy.history = self.__history

        #associate account
        self.__accountId = self.__accountManager.createAccount(BackTester.CASH)
        strategy.accountId = self.__accountId
        strategy.accountManager = self.__accountManager

        #register on trading engine
        strategy.tradingEngine = self.__tradingEngine
        self.__tradingEngine.register(strategy)

    def _execute(self):
        ''' run backtest '''
        LOG.info("Running backtest for %s" % self.__symbols)
        #start trading engine
        thread = Thread(target = self.__tradingEngine.runListener, args = ())
        thread.setDaemon(False)
        thread.start()

        #start tickFeeder
        self.__tickFeeder.execute()
        self.__tradingEngine.stop()
        thread.join(timeout = 60)

        self.__mCalculator.calculate(self.__symbols, self.__accountManager.getAccountPostions(self.__accountId))

    def _printResult(self):
        ''' print result'''
        account = self.__accountManager.getAccount(self.__accountId)
        self.__accounts.append(account)
        LOG.info("account %s" % account)
        LOG.debug([str(order) for order in account.orderHistory])
        LOG.debug("account position %s" % self.__accountManager.getAccountPostions(self.__accountId))


    def runTest(self):
        ''' run one test '''
        self._setup()
        self._execute()
        self._printResult()

if __name__ == "__main__":
    backTester = BackTester(startTickDate = 20101010, startTradeDate = 20131010)
    backTester.setup()
    backTester.runTests()
    backTester.printMetrics()

