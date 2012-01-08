'''
Created on Dec 25, 2011

@author: ppa
'''
from ultrafinance.backTest.tickSubscriber import TickSubsriber
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.outputSaver import HbaseSaver
from ultrafinance.backTest.btUtil import OUTPUT_PREFIX, OUTPUT_FIELDS

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
        self.__hbaseSaver = HbaseSaver()
        self.__firstTime = True
        self.__curTime = ''

    def subRules(self):
        ''' override function '''
        return (self.configDict['symbolre'], None)

    def preConsume(self, tickDict):
        ''' override function '''
        if self.accountId is None:
            raise UfException(Errors.NONE_ACCOUNT_ID,
                              "Account id is none")
        if self.tradingCenter is None:
            raise UfException(Errors.NONE_TRADING_CENTER,
                              "trading center is not set")

        self.__saveOutput(tickDict)

    def __setupHSaver(self, symbols):
        ''' setup HbaseSaver '''
        self.__hbaseSaver.tableName = "%s_%s_%s" % (OUTPUT_PREFIX,
                                                    self.__class__.__name__,
                                                    '.'.join(symbols))
        cols = symbols
        cols.extend(OUTPUT_FIELDS)
        LOG.debug(cols)
        self.__hbaseSaver.resetCols(cols)

    def __saveOutput(self, tickDict):
        #save ticks info
        # for the first time, clear output table
        if self.__firstTime:
            if self.configDict.get('outputsaver'):
                self.__setupHSaver(tickDict.keys())
                self.__firstTime = False

        self.__curTime = tickDict.values()[0].time

        for symbol, tick in tickDict.iteritems():
            if self.configDict.get('outputsaver'):
                self.__hbaseSaver.write(tick.time, symbol, tick.close)

    def placeOrder(self, order):
        ''' place order and keep record'''
        orderId = self.tradingCenter.placeOrder(order)

        if self.configDict.get('outputsaver'):
            self.__hbaseSaver.write(self.__curTime, 'placedOrder', str(order))

        return orderId