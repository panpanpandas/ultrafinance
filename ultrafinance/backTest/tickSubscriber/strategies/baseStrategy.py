'''
Created on Dec 25, 2011

@author: ppa
'''
import abc
from ultrafinance.backTest.tickSubscriber import TickSubsriber
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.constant import EVENT_TICK_UPDATE, EVENT_ORDER_EXECUTED

import logging
LOG = logging.getLogger()

class BaseStrategy(TickSubsriber):
    ''' trading center '''
    __meta__ = abc.ABCMeta

    def __init__(self, name):
        ''' constructor '''
        super(BaseStrategy, self).__init__(name)
        self.accountId = None
        self.tradingEngine = None
        self.configDict = {}
        self.symbols = []
        self.__curTime = ''
        self.indexHelper = None
        self.history = None
        self.accountManager = None


    def subRules(self):
        ''' override function '''
        return (self.symbols, [EVENT_TICK_UPDATE, EVENT_ORDER_EXECUTED])

    def checkReady(self):
        '''
        whether strategy has been set up and ready to run
        TODO: check trading engine
        '''
        if self.accountId is None:
            raise UfException(Errors.NONE_ACCOUNT_ID,
                              "Account id is none")

        return True

    def placeOrder(self, order):
        ''' place order and keep record'''
        orderId = self.tradingEngine.placeOrder(order)

        return orderId

    def complete(self):
        ''' complete operation '''
        pass

    def setSymbols(self, symbols):
        '''set symbols '''
        if list != type(symbols):
            raise UfException(Errors.INVALID_SYMBOLS,
                              "symbols %s is not a list" % symbols)

        self.symbols = symbols

    def getAccountCopy(self):
        ''' get copy of account info '''
        return self.accountManager.getAccountCopy(self.accountId)
