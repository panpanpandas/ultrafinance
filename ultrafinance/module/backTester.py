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

import json
import traceback
import logging.config
import logging
LOG = logging.getLogger()

class BackTester(object):
    ''' back testing '''
    def __init__(self, configFile, startTickDate = 0, startTradeDate = 0, endTradeDate = None, cash = 150000, symbolLists = None):
        LOG.debug("Loading config from %s" % configFile)
        self.__config = PyConfig()
        self.__config.setSource(configFile)

        self.__cash = cash
        self.__mCalculator = MetricCalculator()
        self.__symbolLists = symbolLists
        LOG.debug(self.__symbolLists)
        self.__accounts = []
        self.__startTickDate = startTickDate
        self.__startTradeDate = startTradeDate
        self.__endTradeDate = endTradeDate
        self.__firstSaver = None

    def setup(self):
        ''' setup '''
        appGlobal[TRADE_TYPE] = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_TRADE_TYPE)
        self.__config.override(CONF_ULTRAFINANCE_SECTION, CONF_INIT_CASH, self.__cash)
        self.__config.override(CONF_ULTRAFINANCE_SECTION, CONF_START_TRADE_DATE, self.__startTradeDate)
        self.__config.override(CONF_ULTRAFINANCE_SECTION, CONF_END_TRADE_DATE, self.__endTradeDate)
        self._setupLog()
        LOG.debug(self.__symbolLists)
        if not self.__symbolLists:
            self._loadSymbols()

    def __getFirstSaver(self):
        ''' get first saver, create it if not exist'''
        saverName = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_SAVER)
        outputDb = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_OUTPUT_DB)
        if saverName and len(self.__symbolLists) > 0:
            self.__firstSaver = StateSaverFactory.createStateSaver(saverName,
                                                                   {'db': outputDb},
                                                                   getBackTestTableName(self.__symbolLists[0],
                                                                                        self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_STRATEGY_NAME)))

        return self.__firstSaver


    def _setupLog(self):
        ''' setup logging '''
        if self.__config.getSection("loggers"):
            logging.config.fileConfig(self.__config.getFullPath())

    def _runOneTest(self, symbols):
        ''' run one test '''
        LOG.debug("Running backtest for %s" % symbols)
        runner = TestRunner(self.__config, self.__mCalculator, self.__accounts, symbols, self.__startTickDate, self.__endTradeDate, self.__cash)
        runner.runTest()

    def _loadSymbols(self):
        ''' find symbols'''
        symbolFile = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_SYMBOL_FILE)
        assert symbolFile is not None, "%s is required in config file" % CONF_SYMBOL_FILE

        LOG.info("loading symbols from %s" % os.path.join(self.__config.getDir(), symbolFile))
        if not self.__symbolLists:
            self.__symbolLists = []

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

    def getLatestStates(self):
        ''' get latest state'''
        return [json.loads(str(result)) for result in self.__getFirstSaver().getStates(0, None)]

    def getLatestPlacedOrders(self, num = 20):
        ''' get latest placed orders of first symbol list '''
        orders = []
        for account in self.__accounts:
            orders.extend(account.orderHistory[-num:])

        return orders

    def getHoldings(self):
        ''' get holdings '''
        holdings = []
        for account in self.__accounts:
            holdings.append(account.holdings)

        return holdings

    def getMetrics(self):
        ''' get all metrics '''
        return self.__mCalculator.getMetrics()


    def getOpenOrders(self):
        ''' get open orders '''
        return self.__

    def printMetrics(self):
        ''' print metrics '''
        LOG.info(self.getMetrics())

class TestRunner(object):
    ''' back testing '''
    def __init__(self, config, mCalculator, accounts, symbols, startTickDate, endTradeDate, cash):
        self.__accountManager = AccountManager()
        self.__accountId = None
        self.__tickFeeder = TickFeeder(start = startTickDate, end = endTradeDate)
        self.__tradingCenter = TradingCenter()
        self.__tradingEngine = TradingEngine()
        self.__indexHelper = IndexHelper()
        self.__accounts = accounts
        self.__history = History()
        self.__saver = None
        self.__symbols = symbols
        self.__config = config
        self.__mCalculator = mCalculator
        self.__cash = cash

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
        self.__tickFeeder.setSymbols(self.__symbols)
        self.__tickFeeder.setDam(self._createDam("")) # no need to set symbol because it's batch operation

        #set index dam
        #iSymbol = self.__config.getOption(CONF_APP_MAIN, CONF_INDEX)
        #iDam = self._createDam(iSymbol)
        #self.__tickFeeder.setIndexDam(iDam)

    def _createDam(self, symbol):
        ''' setup Dam'''
        damName = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_INPUT_DAM)
        inputDb = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_INPUT_DB)
        dam = DAMFactory.createDAM(damName, {'db': inputDb})
        dam.setSymbol(symbol)

        return dam

    def _setupSaver(self):
        ''' setup Saver '''
        saverName = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_SAVER)
        outputDb = self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_OUTPUT_DB)
        if saverName:
            self.__saver = StateSaverFactory.createStateSaver(saverName,
                                                              {'db': outputDb},
                                                              getBackTestTableName(self.__symbols, self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_STRATEGY_NAME)))

    def _setupStrategy(self):
        ''' setup tradingEngine'''
        strategy = StrategyFactory.createStrategy(self.__config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_STRATEGY_NAME),
                                                  self.__config.getSection(CONF_ULTRAFINANCE_SECTION))
        strategy.setSymbols(self.__symbols)
        strategy.indexHelper = self.__indexHelper
        strategy.history = self.__history

        #associate account
        self.__accountId = self.__accountManager.createAccount(self.__cash)
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


############Util function################################
def getBackTestTableName(symbols, strategyName):
    ''' get table name for back test result'''
    return "%s_%s" % (symbols if len(symbols) <= 1 else len(symbols), strategyName)


if __name__ == "__main__":
    backTester = BackTester("backtest_zscorePortfolio.ini", startTickDate = 20001010, startTradeDate = 20021010, endTradeDate = 20131010)
    backTester.setup()
    backTester.runTests()
    backTester.printMetrics()
    print backTester.getLatestStates()

