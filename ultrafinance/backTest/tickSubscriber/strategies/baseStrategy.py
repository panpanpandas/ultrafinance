'''
Created on Dec 25, 2011

@author: ppa
'''
from ultrafinance.backTest.tickSubscriber import TickSubsriber
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.outputSaver import OutputSaverFactory
from ultrafinance.backTest.btUtil import OUTPUT_PREFIX, OUTPUT_FIELDS
from ultrafinance.backTest.constant import CONF_SYMBOLRE, CONF_SAVER

import logging
LOG = logging.getLogger()

class BaseStrategy(TickSubsriber):
    ''' trading center '''
    def __init__(self, name):
        ''' constructor '''
        super(BaseStrategy, self).__init__(name)
        self.accountId = None
        self.tradingCenter = None
        self.configDict = {}
        self.__saver = None
        self.__firstTime = True
        self.__curTime = ''

    def subRules(self):
        ''' override function '''
        return (self.configDict[CONF_SYMBOLRE], None)

    def preConsume(self, tickDict):
        ''' override function '''
        if self.accountId is None:
            raise UfException(Errors.NONE_ACCOUNT_ID,
                              "Account id is none")
        if self.tradingCenter is None:
            raise UfException(Errors.NONE_TRADING_CENTER,
                              "trading center is not set")

        self.__saveOutput(tickDict)

    def __setupSaver(self, saverName, symbols):
        ''' setup Saver '''
        self.__saver = OutputSaverFactory().createOutputSaver(saverName)
        self.__saver.tableName = "%s_%s_%s" % (OUTPUT_PREFIX,
                                               self.__class__.__name__,
                                               '.'.join(symbols))

    def __saveOutput(self, tickDict):
        #save ticks info
        # for the first time, clear output table
        if self.__firstTime:
            saverName = self.configDict.get(CONF_SAVER)
            if saverName:
                self.__setupSaver(saverName, tickDict.keys())
                self.__firstTime = False

        self.__curTime = tickDict.values()[0].time

        for symbol, tick in tickDict.iteritems():
            if self.__saver:
                self.__saver.write(tick.time, symbol, str(tick))


    def placeOrder(self, order):
        ''' place order and keep record'''
        orderId = self.tradingCenter.placeOrder(order)

        if self.__saver:
            self.__saver.write(self.__curTime, 'placedOrder', str(order))

        return orderId


    def complete(self):
        ''' complete operation '''
        if self.__saver:
            self.__saver.writeComplete()