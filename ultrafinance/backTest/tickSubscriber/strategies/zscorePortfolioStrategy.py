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
from ultrafinance.pyTaLib.indicator import ZScore
from ultrafinance.backTest.constant import CONF_START_TRADE_DATE, CONF_BUYING_RATIO
import math

import logging
LOG = logging.getLogger()

class ZscorePortfolioStrategy(BaseStrategy):
    ''' period strategy '''
    def __init__(self, configDict):
        ''' constructor '''
        super(ZscorePortfolioStrategy, self).__init__("zscorePortfolioStrategy")
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
        self.__threshold = 2.5
        self.__priceZscore = ZScore(120)
        self.__volumeZscore = ZScore(120)
        self.__toSell = False
        self.__toBuy = False

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
                             action = Action.SELL,
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
        self.__priceZscore(tick.close)
        self.__volumeZscore(tick.volume)

        #if haven't started, don't do any trading
        if tick.time <= self.__startDate:
            return

        # if not enough data, skip to reduce risk
        if not self.__priceZscore.getLastValue() or not self.__volumeZscore.getLastValue():
            return

        # get zscore
        priceZscore = self.__priceZscore.getLastValue()
        volumeZscore = self.__volumeZscore.getLastValue()
        if priceZscore is None or volumeZscore is None:
            return

        if self.__toBuy:
            self.__placeBuyOrder(tick)
            self.__toBuy = False
            return

        if self.__toSell:
            self.__placeSellOrder(tick)
            self.__toSell = False
            return

        if priceZscore < (-self.__threshold) and not self.__buyOrder and abs(volumeZscore) > 1.5:
            self.__toBuy = True

        elif self.__buyOrder and priceZscore > 0.5:
            self.__toSell = True
