'''
Created on Dec 18, 2011

@author: ppa
'''
from ultrafinance.model import Side, Order
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.tradingCenter.account import Account
import uuid
import re
import copy
import time

import logging
LOG = logging.getLogger(__name__)

class TradingCenter(object):
    ''' trading center '''
    def __init__(self):
        ''' constructor '''
        self.__accounts = {}
        self.__openOrders = {}
        self.__closedOrders = {}

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

            return order.orderId

        else:
            return None

    def __generateId(self):
        ''' generate id '''
        return uuid.uuid4()

    def validateOrder(self, order):
        ''' validate an order '''
        account = self.getAccount(order.accountId)
        if account and account.validate(order):
            return True

        return False

    def cancelOrder(self, orderId):
        ''' cancel an order '''
        for symbol, orders in self.__openOrders.items():
            for index, order in enumerate(orders):
                if orderId == order.orderId:
                    order.status = Order.CANCELED #change order state
                    self.__deadOrders[order.orderId] = order

                    del orders[index]
                    #if no open orders left for that symbol, remove it
                    if not len(orders):
                        del self.__openOrders[symbol]

    def createAccount(self, cash, commission=0):
        ''' create account '''
        account = Account(cash, commission)
        self.__accounts[account.accountId] = account
        return account.accountId

    def getAccount(self, accountId):
        ''' get account '''
        return copy(self.__accounts.get(accountId) )

    def getAccounts(self, expression):
        ''' get account '''
        accounts = []
        pair = re.compile(expression)

        for accountId, account in self.__accounts.items():
            if pair.match(accountId):
                accounts.append[copy(account)]

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
        return ('*', None)

    def consume(self, tickDict):
        ''' consume tick '''
        for symbol, tick in tickDict.iteritems():
            if symbol in self.__openOrders:
                for index, order in enumerate(self.__openOrders[symbol]):
                    if self.isOrderMet(tick, order):
                        account = self.getAccount(order.accountId)
                        if not account:
                            raise UfException(Errors.INVALID_ACCOUNT,
                                              ''' Account is invalid: accountId %s''' % order.accountId )
                        else:
                            account.execute(order)
                            order.status = Order.FILLED
                            order.filledTime = time.time()

                            del self.__openOrders[symbol][index]
                            self.__closedOrders.append(order)


    def isOrderMet(self, tick, order):
        ''' whether order can be execute or not '''
        if Side.BUY == order.side and float(tick.price) > order.price:
            return True
        elif Side.SELL == order.side and float(tick.price) < order.price:
            return True
        else:
            return False



