'''
Created on Nov 09, 2013

This strategy use zscore to trade stocks

When to Buy/Short:
if zsocore is > 2.5

When to Sell/Buy to cover:
1 after 10 days
2 or stop order is met(5%)

@author: ppa
'''
from ultrafinance.model import Type, Action, Order
from ultrafinance.backTest.tickSubscriber.strategies.baseStrategy import BaseStrategy
from ultrafinance.pyTaLib.indicator import ZScoreForDollarVolume
from ultrafinance.backTest.constant import CONF_BUYING_RATIO
import math

import logging
LOG = logging.getLogger()

class ZscorePortfolioStrategy(BaseStrategy):
    ''' period strategy '''
    def __init__(self, configDict):
        ''' constructor '''
        super(ZscorePortfolioStrategy, self).__init__("zscorePortfolioStrategy")
        self.__trakers = {}
        self.buyingRatio = int(configDict.get(CONF_BUYING_RATIO) if CONF_BUYING_RATIO in configDict else 2)

    def __setUpTrakers(self):
        ''' set symbols '''
        for symbol in self.symbols:
            self.__trakers[symbol] = OneTraker(symbol, self, self.buyingRatio)

    def orderExecuted(self, orderDict):
        ''' call back for executed order '''
        for orderId, order in orderDict.items():
            if order.symbol in self.__trakers.keys():
                self.__trakers[order.symbol].orderExecuted(orderId)

    def tickUpdate(self, tickDict):
        ''' consume ticks '''
        if not self.__trakers:
            self.__setUpTrakers()

        for symbol, tick in tickDict.items():
            if symbol in self.__trakers:
                self.__trakers[symbol].tickUpdate(tick)

class OneTraker(object):
    ''' tracker for one stock '''
    def __init__(self, symbol, strategy, buyingRatio):
        ''' constructor '''
        self.__symbol = symbol
        self.__strategy = strategy
        self.__buyingRatio = buyingRatio
        self.__threshold = 2.5
        self.__holdDays = 15
        self.__dateCounter = 0
        self.__dollarVolume = ZScoreForDollarVolume(15)

        # order id
        self.__buyOrder = None


    def __getCashToBuyStock(self):
        ''' calculate the amount of money to buy stock '''
        account = self.__strategy.getAccountCopy()
        if (account.getCash() >= account.getTotalValue() / self.__buyingRatio):
            return account.getTotalValue() / self.__buyingRatio
        else:
            return 0

    def __placeBuyOrder(self, tick):
        ''' place buy order'''
        cash = self.__getCashToBuyStock()
        if cash == 0:
            return

        share = math.floor(cash / float(tick.close))
        buyOrder = Order(accountId = self.__strategy.accountId,
                         action = Action.BUY,
                         type = Type.MARKET,
                         symbol = self.__symbol,
                         share = share)
        if self.__strategy.placeOrder(buyOrder):
            self.__buyOrder = buyOrder

    def __placeSellOrder(self, tick):
        ''' place sell order '''
        if self.__buyOrder:
            sellOrder = Order(accountId = self.__strategy.accountId,
                             action = Action.BUY,
                             type = Type.MARKET,
                             symbol = self.__symbol,
                             share = self.__buyOrder.share)
            if self.__strategy.placeOrder(sellOrder):
                self.__buyOrder = None


    def orderExecuted(self, orderId):
        ''' call back for executed order '''
        return

    def tickUpdate(self, tick):
        ''' consume ticks '''
        LOG.debug("tickUpdate %s with tick %s, price %s" % (self.__symbol, tick.time, tick.close))
        self.__dollarVolume(tick.close, tick.volume)

        # if not enough data, skip to reduce risk
        if not self.__dollarVolume.getLastValue():
            return

        # get dollar volumes
        delta_z = self.__dollarVolume.getLastValue()
        if delta_z is None:
            return

        if delta_z < (-self.__threshold) and not self.__buyOrder:
            self.__dateCounter = 0
            self.__placeBuyOrder(tick)

        elif self.__buyOrder and (self.__dateCounter > self.__holdDays or tick.close < self.__buyOrder.price * 0.95):
            self.__placeSellOrder(tick)

        if self.__buyOrder:
            self.__dateCounter += 1

