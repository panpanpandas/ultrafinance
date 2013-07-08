'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.model import Side
from ultrafinance.lib.errors import Errors, UfException
import uuid

import logging
LOG = logging.getLogger()

class Account(object):
    ''' account '''

    def __init__(self, cash, commision):
        ''' constructor '''
        self.__id = self.__generateId()
        self.__holdings = {}
        self.__cash = cash
        self.__commision = commision
        self.__orderHisotry = []
        self.__lastTickDict = None

    def __generateId(self):
        ''' generate id '''
        return uuid.uuid4()

    def __addHolding(self, symbol, share, price):
        ''' add holding '''
        if symbol not in self.__holdings:
            self.__holdings[symbol] = [share, price]

        else:
            preShare, prePrice = self.__holdings[symbol]
            preValue = preShare * prePrice
            curShare = share + preShare
            curPrice = (share * price + preValue) / curShare
            self.__holdings[symbol] = [curShare, curPrice]

    def __reduceHolding(self, symbol, share):
        ''' reduce holding '''
        preShare, prePrice = self.__holdings[symbol]
        curShare = preShare - share
        self.__holdings[symbol] = [curShare, prePrice]

    def execute(self, order):
        ''' execute order'''
        LOG.debug("account execute order: %s" % order)
        msg = self.validate(order)
        if msg != None:
            raise UfException(Errors.ORDER_INVALID_ERROR,
                              "Transition is invalid: symbol %s, share %s, price %s, details %s"\
                              % (order.symbol, order.share, order.price, msg))

        value = self.__getOrderValue(order)
        if Side.BUY == order.side:
            self.__cash = self.__cash - value - self.__commision
            self.__addHolding(order.symbol, order.share, order.price)
        elif Side.SELL == order.side:
            self.__cash = self.__cash + value - self.__commision
            self.__reduceHolding(order.symbol, order.share)
        else:
            self.__cash = self.__cash + value - self.__commision
            self.__reduceHolding(order.symbol, order.share)

        self.__orderHisotry.append(order)

    def validate(self, order):
        ''' validate order to check whether it's do-able or not '''
        value = self.__getOrderValue(order)
        cost = value + self.__commision
        msg = None

        if Side.BUY == order.side:
            if cost > self.__cash:
                msg = 'Transition fails validation: cash %.2f is smaller than cost %.2f' % (self.__cash, cost)
        elif Side.SELL == order.side:
            if order.symbol not in self.__holdings:
                msg = 'Transition fails validation: symbol %s not in holdings' % order.symbol
            elif order.share > self.__holdings[order.symbol][0]:
                msg = 'Transition fails validation: share %s is not enough as %s' % (order.share, self.__holdings[order.symbol])
            elif self.__commision > self.__cash:
                msg = 'Transition fails validation: cash %s is not enough for commission %s' % (self.__cash, self.__commision)
        #TODO validate stop order


        return msg

    def getCash(self):
        ''' get cash '''
        return self.__cash

    def getHoldingCost(self):
        ''' get cost of holdings '''
        value = 0.0
        for share, price in self.__holdings.values():
            value += share * price

        return value

    def getHoldingValue(self):
        ''' get value of holdings '''
        missingSymbols = set(self.__holdings.keys()) - set(self.__lastTickDict.keys())
        if missingSymbols:
            raise UfException(Errors.MISSING_SYMBOL,
                              "no all symbols in holdings have price: %s" % missingSymbols)

        value = 0.0
        for symbol, (share, price) in self.__holdings.items():
            price = self.__lastTickDict[symbol].close
            value += share * price

        return value

    def getTotalValue(self):
        ''' get total value '''
        return self.getCash() + self.getHoldingValue()

    def __getOrderValue(self, order):
        ''' get value of order '''
        return float(order.price) * float(order.share)

    def __getId(self):
        ''' get id '''
        return self.__id

    def __getHoldings(self):
        ''' get holding'''
        return self.__holdings

    def __getOrderHistory(self):
        ''' get order history '''
        return self.__orderHisotry

    def __getCommision(self):
        ''' get commission '''
        return self.__commision

    def setLastTickDict(self, tickDict):
        ''' set tickDict'''
        self.__lastTickDict = tickDict

    def getLastTickDict(self):
        ''' get time for last symbolPrice '''
        return self.__lastTickDict

    def __str__(self):
        ''' override string function '''
        totalValue = 0.0
        try:
            totalValue = self.getTotalValue()
        except:
            pass
        return str({'accountId': str(self.accountId), 'holdings': self.holdings, 'cash': "%.2f" % self.cash,
                    'totalValue': "%.2f" % totalValue, 'holdingCost': "%.2f" % self.getHoldingCost()})

    accountId = property(__getId)
    holdings = property(__getHoldings)
    cash = property(getCash)
    orderHistory = property(__getOrderHistory)
    commision = property(__getCommision)
