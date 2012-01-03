'''
Created on Dec 18, 2011

@author: ppa
'''
from ultrafinance.model import Side, Order
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.account import Account
from ultrafinance.backTest.tickSubscriber import TickSubsriber
from ultrafinance.backTest.metric.metricFactory import MetricFactory
import uuid
import re
import copy
import time

import logging
LOG = logging.getLogger()

class TradingCenter(TickSubsriber):
    '''
    trading center
    Note: set metricNames before adding accounts
    '''
    def __init__(self):
        ''' constructor '''
        super(TradingCenter, self).__init__("tradingCenter")
        self.__curTime = None
        self.__accounts = {}
        self.__metrix = {}
        self.__metricNames = []
        self.__openOrders = {}
        self.__closedOrders = {}
        self.__lastSymbolPrice = {}
        self.__metricFactory = MetricFactory()

    def placeOrder(self, order):
        ''' place an order '''
        if order.orderId is not None:
            raise UfException(Errors.ORDER_TYPE_ERROR, 'OrderId already set: %s' % self.orderId)

        if self.validateOrder(order):
            # generate a unique order id
            order.orderId = uuid.uuid4()

            # put order in list
            if order.symbol not in self.__openOrders:
                self.__openOrders[order.symbol] = []
            self.__openOrders[order.symbol].append(order)

            LOG.debug("Order placed %s" % order)
            return order.orderId

        else:
            return None

    def __generateId(self):
        ''' generate id '''
        return uuid.uuid4()

    def validateOrder(self, order):
        ''' validate an order '''
        account = self.__getAccount(order.accountId)
        if account and account.validate(order):
            return True

        return False

    def cancelOrder(self, orderId):
        ''' cancel an order '''
        for symbol, orders in self.__openOrders.items():
            for index, order in enumerate(orders):
                if orderId == order.orderId:
                    order.status = Order.CANCELED #change order state
                    self.__closedOrders[order.orderId] = order

                    del orders[index]
                    #if no open orders left for that symbol, remove it
                    if not len(orders):
                        del self.__openOrders[symbol]

    def cancelAllOpenOrders(self, orderId):
        ''' cancel all open order '''
        for symbol, orders in self.__openOrders.items():
            for index, order in enumerate(orders):
                order.status = Order.CANCELED #change order state
                self.__closedOrders[order.orderId] = order

                del orders[index]
                #if no open orders left for that symbol, remove it
                if not len(orders):
                    del self.__openOrders[symbol]

    def createAccountWithMetrix(self, cash, commission=0):
        ''' create account '''
        account = Account(cash, commission)
        self.__accounts[account.accountId] = account

        self.__metrix[account.accountId] = []
        for metricName in self.__metricNames:
            metric = self.__metricFactory.createMetric(metricName)
            metric.setAccount(account)
            self.__metrix[account.accountId].append(metric)

        return account.accountId

    def getCopyAccount(self, accountId):
        ''' get copy of account '''
        return copy.deepcopy(self.__getAccount(accountId) )

    def getCopyAccounts(self, expression):
        ''' get copy of accounts '''
        accounts = self.__getAccounts(expression)
        return copy.deepcopy(accounts)

    def __getAccount(self, accountId):
        ''' get account '''
        return self.__accounts.get(accountId)

    def __getAccounts(self, expression):
        ''' get accounts '''
        accounts = []
        pair = re.compile(expression)

        for accountId, account in self.__accounts.items():
            if pair.match(str(accountId) ):
                accounts.append(account)

        return accounts

    def getOpenOrdersBySymbol(self, symbol):
        ''' get open orders by symbol '''
        if symbol in self.__openOrders:
            return self.__openOrders.get(symbol)
        else:
            return []

    def getOpenOrdersByOrderId(self, expression):
        ''' get open order by orderId '''
        orders = []
        pair = re.compile(expression)

        for openOrders in self.__openOrders.values():
            for order in openOrders:
                if pair.match(order.orderId):
                    orders.append(order)

        return orders

    def getClosedOrder(self, orderId):
        ''' get closed orders'''
        return self.__closedOrders.get(orderId)

    def getClosedOrders(self, expression):
        ''' get closed orders '''
        orders = []
        pair = re.compile(expression)

        for orderId, order in self.__closedOrders:
            if pair.match(orderId):
                orders.append(order)

        return orders

    def subRules(self):
        ''' override function, will subscribe to all symbols '''
        return ('.*', None)

    def consume(self, tickDict):
        ''' consume tick '''
        if tickDict:
            self.__curTime = tickDict.values()[0].time

        for symbol, tick in tickDict.iteritems():
            LOG.debug("trading center get symbol %s with tick %s" % (symbol, tick.time) )
            self.__lastSymbolPrice[symbol] = tick.close
            if symbol in self.__openOrders:
                for index, order in enumerate(self.__openOrders[symbol]):
                    if self.isOrderMet(tick, order):
                        account = self.__getAccount(order.accountId)
                        if not account:
                            raise UfException(Errors.INVALID_ACCOUNT,
                                              ''' Account is invalid: accountId %s''' % order.accountId )
                        else:
                            LOG.debug("executing order %s" % order)
                            account.execute(order)
                            order.status = Order.FILLED
                            order.filledTime = time.time()

                            del self.__openOrders[symbol][index]
                            self.__closedOrders[order.orderId] = order

    def postConsume(self, tickDict):
        ''' calculate metrix for each account '''
        LOG.debug("postConsume in tradingCenter")
        for accountId, metrix in self.__metrix.items():
            account = self.__getAccount(accountId)
            account.setLastSymbolPrice(self.__lastSymbolPrice)

            for metric in metrix:
                metric.record(self.__curTime)

    def setMetricNames(self, metricNames):
        ''' set metricNames '''
        self.__metricNames = metricNames

    def getMetrix(self):
        ''' get metrix '''
        return self.__metrix

    def addMetrixToAccount(self, metrix, accountId):
        ''' add a list of metric to accountId '''
        account = self.__accounts.get(accountId)
        if account:
            account.metrix.extend(metrix)

    def isOrderMet(self, tick, order):
        ''' whether order can be execute or not '''
        if Side.BUY == order.side and float(tick.close) > float(order.price):
            return True
        elif Side.SELL == order.side and float(tick.price) < float(order.price):
            return True
        else:
            return False

    def getLastSymbolPrice(self):
        ''' return __lastSymbolPrice '''
        return self.__lastSymbolPrice

    lastSymbolPrice = property(getLastSymbolPrice)
