'''
Created on Nov 09, 2013

This strategy use zscore to trade stocks

When to Buy/Short:
if zsocore is > 2

When to Sell/Buy to cover:
1 after 10 days
2 or stop order is met(5%)

@author: ppa
'''
from ultrafinance.model import Type, Action, Order
from ultrafinance.backTest.tickSubscriber.strategies.baseStrategy import BaseStrategy
from ultrafinance.pyTaLib.indicator import ZScore, Momentum
from ultrafinance.backTest.constant import CONF_START_TRADE_DATE, CONF_BUYING_RATIO
import math

import logging
LOG = logging.getLogger()

class ZscoreMomentumPortfolioStrategy(BaseStrategy):
    ''' period strategy '''
    def __init__(self, configDict):
        ''' constructor '''
        super(ZscoreMomentumPortfolioStrategy, self).__init__("zscoreMomentumPortfolioStrategy")
        self.__trakers = {}
        self.startDate = int(configDict.get(CONF_START_TRADE_DATE))
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
        self.__startDate = strategy.startDate
        self.__buyingRatio = buyingRatio
        self.__buyThreshold = 1.5
        self.__sellThreshold = 0.5
        self.__preZscore = None
        self.__priceZscore = ZScore(150)
        self.__volumeZscore = ZScore(150)
        self.__dayCounter = 0
        self.__dayCounterThreshold = 5

        # order id
        self.__position = 0
        self.__buyPrice = 0


    def __getCashToBuyStock(self):
        ''' calculate the amount of money to buy stock '''
        account = self.__strategy.getAccountCopy()

        if (account.buyingPower >= account.getTotalValue() / self.__buyingRatio):
            return account.getTotalValue() / self.__buyingRatio
        else:
            return 0

    def __placeBuyOrder(self, tick):
        ''' place buy order'''
        cash = self.__getCashToBuyStock()
        if cash == 0:
            return

        share = math.floor(cash / float(tick.close))
        order = Order(accountId = self.__strategy.accountId,
                         action = Action.BUY,
                         type = Type.MARKET,
                         symbol = self.__symbol,
                         share = share)
        if self.__strategy.placeOrder(order):
            self.__position = share
            self.__buyPrice = tick.close

    def __placeSellOrder(self, tick):
        ''' place sell order '''
        if self.__position < 0:
            return

        share = self.__position
        order = Order(accountId = self.__strategy.accountId,
                         action = Action.SELL,
                         type = Type.MARKET,
                         symbol = self.__symbol,
                         share = -share)
        if self.__strategy.placeOrder(order):
            self.__position = 0
            self.__buyPrice = 0


    def orderExecuted(self, orderId):
        ''' call back for executed order '''
        return

    def tickUpdate(self, tick):
        ''' consume ticks '''
        LOG.debug("tickUpdate %s with tick %s, price %s" % (self.__symbol, tick.time, tick.close))
        self.__priceZscore(tick.close)
        self.__volumeZscore(tick.volume)

        # get zscore
        priceZscore = self.__priceZscore.getLastValue()
        volumeZscore = self.__volumeZscore.getLastValue()

        #if haven't started, don't do any trading
        if tick.time <= self.__startDate:
            return

        # if not enough data, skip to reduce risk
        if priceZscore is None or volumeZscore is None:
            return

        if self.__position > 0:
            self.__dayCounter += 1

        if priceZscore > self.__buyThreshold and self.__preZscore and self.__preZscore < self.__buyThreshold and self.__position <= 0 and abs(volumeZscore) > 1:
            self.__placeBuyOrder(tick)
        elif self.__position > 0:
            if (self.__dayCounter > self.__dayCounterThreshold and priceZscore < self.__sellThreshold)\
            or priceZscore < 0 or self.__buyPrice * 0.9 > tick.close:
                self.__placeSellOrder(tick)
                self.__dayCounter = 0

        self.__preZscore = priceZscore
