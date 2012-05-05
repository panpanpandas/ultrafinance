'''
Created on Dec 18, 2011

@author: ppa
'''
from ultrafinance.model import Side, Order
from ultrafinance.lib.errors import Errors, UfException
import uuid
import re
import time

import logging
LOG = logging.getLogger()

class TradingCenter(object):
    '''
    trading center
    Note: set metricNames before adding accounts
    '''
    def __init__(self):
        ''' constructor '''
        self.accountManager = None
        self.__openOrders = {}
        self.__closedOrders = {}
        self.__lastSymbolPrice = {}
        self.__updatedOrder = {}

    def getUpdatedOrder(self):
        ''' return orders with status changes '''
        updatedOrder = {}
        updatedOrder.update(self.__updatedOrder)
        self.__updatedOrder.clear()

        return updatedOrder

    def validateOrder(self, order):
        ''' validate an order '''
        account = self.accountManager.getAccount(order.accountId)
        if account and account.validate(order):
            return True

        return False

    def placeOrder(self, order):
        ''' place an order '''
        if order.orderId:
            raise UfException(Errors.ORDER_TYPE_ERROR, 'OrderId already set: %s' % order.orderId)

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

    def cancelAllOpenOrders(self):
        ''' cancel all open order '''
        for symbol, orders in self.__openOrders.items():
            for order in orders:
                order.status = Order.CANCELED #change order state
                self.__closedOrders[order.orderId] = order

            del self.__openOrders[symbol]

    def getOpenOrdersBySymbol(self, symbol):
        ''' get open orders by symbol '''
        if symbol in self.__openOrders:
            return self.__openOrders[symbol]
        else:
            return []

    def getOpenOrderByOrderId(self, orderId):
        ''' get open order by orderId '''
        for openOrders in self.__openOrders.values():
            for order in openOrders:
                if orderId == order.orderId:
                    return order

        return None

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

    def consumeTicks(self, tickDict):
        ''' consume ticks '''
        self._checkAndExecuteOpenOrder(tickDict)
        self.accountManager.updateAccountsPosition(tickDict)

    def _checkAndExecuteOpenOrder(self, tickDict):
        ''' check and execute open order '''
        for symbol, tick in tickDict.iteritems():
            LOG.debug("_executeOpenOrder symbol %s with tick %s" % (symbol, tick.time))
            if symbol in self.__openOrders:
                for index, order in enumerate(self.__openOrders[symbol]):
                    if self.isOrderMet(tick, order):
                        account = self.accountManager.getAccount(order.accountId)
                        if not account:
                            raise UfException(Errors.INVALID_ACCOUNT,
                                              ''' Account is invalid: accountId %s''' % order.accountId)
                        else:
                            LOG.debug("executing order %s" % order)
                            account.execute(order)
                            order.status = Order.FILLED
                            order.filledTime = time.time()

                            del self.__openOrders[symbol][index]
                            self.__closedOrders[order.orderId] = order
                            self.__updatedOrder[order.orderId] = order

    def isOrderMet(self, tick, order):
        ''' whether order can be execute or not '''
        if Side.BUY == order.side and float(tick.close) <= float(order.price):
            return True
        elif Side.SELL == order.side and float(tick.close) >= float(order.price):
            return True
        else:
            return False

