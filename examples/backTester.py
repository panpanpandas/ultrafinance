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

from threading import Thread

import traceback
import logging.config
import logging
LOG = logging.getLogger()

CONFIG_FILE = "backtest_period.ini"

class BackTester(object):
    ''' back testing '''
    CASH = 1000000 #  0.1 million to start

    def __init__(self):
        self.__config = PyConfig()
        self.__mCalculator = MetricCalculator()
        self.__symbols = []

    def setup(self):
        ''' setup '''
        LOG.debug("Loading config from %s" % CONFIG_FILE)
        self.__config.setSource(CONFIG_FILE)
        appGlobal[TRADE_TYPE] = self.__config.getOption(CONF_APP_MAIN, CONF_TRADE_TYPE)
        self.__config.override(CONF_STRATEGY, CONF_INIT_CASH, BackTester.CASH)
        self._setupLog()
        self._loadSymbols()

    def _setupLog(self):
        ''' setup logging '''
        logging.config.fileConfig(self.__config.getFullPath())

    def _runOneTest(self, symbol):
        ''' run one test '''
        LOG.debug("Running backtest for %s" % symbol)
        runner = TestRunner(self.__config, self.__mCalculator, symbol)
        runner.runTest()

    def _loadSymbols(self):
        ''' find symbols'''
        symbolFile = self.__config.getOption(CONF_APP_MAIN, CONF_SYMBOL_FILE)
        assert symbolFile is not None, "%s is required in config file" % CONF_SYMBOL_FILE

        with open(os.path.join(self.__config.getDir(), symbolFile), "r") as f:
            for symbol in f:
                if symbol not in self.__symbols:
                    self.__symbols.append(symbol.strip())

        assert self.__symbols, "None symbol provided"

    def runTests(self):
        ''' run tests '''
        for symbol in self.__symbols:
            try:
                self._runOneTest(symbol)
            except BaseException as excp:
                LOG.error("Unexpected error when backtesting %s -- except %s, traceback %s" \
                          % (symbol, excp, traceback.format_exc(8)))


class TestRunner(object):
    ''' back testing '''
    CASH = 100000 #  0.1 million to start

    def __init__(self, config, mCalculator, symbol):
        self.__accountManager = AccountManager()
        self.__tickFeeder = TickFeeder()
        self.__tradingCenter = TradingCenter()
        self.__tradingEngine = TradingEngine()
        self.__indexHelper = IndexHelper()
        self.__history = History()
        self.__saver = None
        self.__symbol = symbol
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
        sDam = self._createDam(self.__symbol)
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
                                                              "%s_%s" % (self.__symbol,
                                                                         self.__config.getOption(CONF_STRATEGY, CONF_STRATEGY_NAME)))

    def _setupStrategy(self):
        ''' setup tradingEngine'''
        strategy = StrategyFactory.createStrategy(self.__config.getOption(CONF_STRATEGY, CONF_STRATEGY_NAME),
                                                  self.__config.getSection(CONF_STRATEGY))
        strategy.setSymbols([self.__symbol])
        strategy.indexHelper = self.__indexHelper
        strategy.history = self.__history

        #associate account
        accountId = self.__accountManager.createAccount(BackTester.CASH)
        strategy.accountId = accountId

        #register on trading engine
        strategy.tradingEngine = self.__tradingEngine
        self.__tradingEngine.register(strategy)

    def _execute(self):
        ''' run backtest '''
        LOG.info("Running backtest for %s" % self.__symbol)
        #start trading engine
        thread = Thread(target = self.__tradingEngine.runListener, args = ())
        thread.setDaemon(True)
        thread.start()

        #start tickFeeder
        self.__tickFeeder.execute()
        self.__tradingEngine.stop()
        thread.join(timeout = 60)

    def _printResult(self):
        ''' print result'''
        for account in self.__accountManager.getAccounts():
            accountId = account.accountId
            LOG.info("account %s" % account)
            LOG.debug([str(order) for order in account.orderHistory])
            LOG.debug("account position %s" % self.__accountManager.getAccountPostions(accountId))
            LOG.info(self.__mCalculator.formatMetrics(self.__accountManager.getAccountPostions(accountId)))

    def runTest(self):
        ''' run one test '''
        self._setup()
        self._execute()
        self._printResult()

if __name__ == "__main__":
    backTester = BackTester()
    backTester.setup()
    backTester.runTests()
