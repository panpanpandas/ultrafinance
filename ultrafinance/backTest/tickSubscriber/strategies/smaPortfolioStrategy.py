'''
Created on July 08, 2013

This strategy leverage 10/50/200 days Simple Moving Average(SMA) as short/mid/long term trend


When to Sell:
1 when stop order is hit
2 if the 10 < 50 or 10 < 200, place sell order

Stop order:
1 when buy order is placed, set stop order to be 5%
2 as time goes, increase stop price to be min(max(half of the profit, 85% of current price), 95% of current price)
3 never decrease limit price

When to Buy:
1 if 10 < 200 && 50 < 200, skip
2 if previous day price jump more than 10%, skip
3 if the previous day 10 < 200, and today 10 > 200, place buy order
4 if previous day 200 < 10 < 50, and today 200 < 50 < 10, place buy order
5 always place a stop order


@author: ppa
'''
from ultrafinance.model import Type, Action, Order
from ultrafinance.backTest.tickSubscriber.strategies.baseStrategy import BaseStrategy
from ultrafinance.pyTaLib.indicator import Sma, MovingLow
from ultrafinance.backTest.constant import CONF_START_TRADE_DATE, CONF_BUYING_RATIO
import math

import logging
LOG = logging.getLogger()

class SMAPortfolioStrategy(BaseStrategy):
    ''' period strategy '''
    def __init__(self, configDict):
        ''' constructor '''
        super(SMAPortfolioStrategy, self).__init__("smaPortfolioStrategy")
        self.__trakers = {}
        self.startDate = int(configDict.get(CONF_START_TRADE_DATE))
        self.buyingRatio = int(configDict.get(CONF_BUYING_RATIO) if CONF_BUYING_RATIO in configDict else 25)

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

        # order id
        self.__stopOrderId = None
        self.__stopOrder = None
        self.__buyOrder = None

        self.__smaShort = Sma(10)
        self.__smaMid = Sma(60)
        self.__smaLong = Sma(200)
        self.__smaVolumeShort = Sma(10)
        self.__smaVolumeMid = Sma(60)
        self.__movingLowShort = MovingLow(10)
        self.__movingLowWeek = MovingLow(3)

        #state of previous day
        self.__previousTick = None
        self.__previousSmaShort = None
        self.__previousMovingLowShort = None
        self.__previousMovingLowWeek = None
        self.__previousSmaMid = None
        self.__previousSmaLong = None
        self.__previousSmaVolumeShort = None
        self.__previousSmaVolumeMid = None


    def __buyIfMeet(self, tick):
        ''' place buy order if conditions meet '''
        # place short sell order
        '''
        if (self.__smaShort.getLastValue() < self.__smaLong.getLastValue() or self.__smaMid.getLastValue() < self.__smaLong.getLastValue()):
            if tick.close/self.__previousMovingLowWeek < 0.95:
                return

            if self.__previousSmaShort > self.__previousSmaLong and self.__smaShort.getLastValue() < self.__smaLong.getLastValue() and self.__previousSmaVolumeMid < (self.__previousSmaVolumeShort/1.1):
                # assume no commission fee for now
                self.__placeSellShortOrder(tick)

            elif self.__previousSmaLong > self.__previousSmaShort > self.__previousSmaMid and self.__smaLong.getLastValue() > self.__smaMid.getLastValue() > self.__smaShort.getLastValue():
                # assume no commission fee for now
                self.__placeSellShortOrder(tick)
        '''
        # place buy order
        if (self.__smaShort.getLastValue() > self.__smaLong.getLastValue() or self.__smaMid.getLastValue() > self.__smaLong.getLastValue()):
            if tick.close/self.__previousMovingLowWeek > 1.05:
                return

            if self.__previousSmaShort < self.__previousSmaLong and self.__smaShort.getLastValue() > self.__smaLong.getLastValue() and self.__previousSmaVolumeMid < (self.__previousSmaVolumeShort/1.1):
                # assume no commission fee for now
                self.__placeBuyOrder(tick)

            elif self.__previousSmaLong < self.__previousSmaShort < self.__previousSmaMid and self.__smaLong.getLastValue() < self.__smaMid.getLastValue() < self.__smaShort.getLastValue() and self.__previousSmaVolumeMid < (self.__previousSmaVolumeShort/1.1):
                # assume no commission fee for now
                self.__placeBuyOrder(tick)

    def __placeSellShortOrder(self, tick):
        ''' place short sell order'''
        share = math.floor(self.__strategy.getAccountCopy().getCash() / float(tick.close))
        sellShortOrder = Order(accountId = self.__strategy.accountId,
                                  action = Action.SELL_SHORT,
                                  type = Type.MARKET,
                                  symbol = self.__symbol,
                                  share = share)

        if self.__strategy.placeOrder(sellShortOrder):
            self.__buyOrder = sellShortOrder

            #place stop order
            stopOrder = Order(accountId = self.__strategy.accountId,
                          action = Action.BUY_TO_COVER,
                          type = Type.STOP,
                          symbol = self.__symbol,
                          price = tick.close * 1.05,
                          share = 0 - share)
            self.__placeStopOrder(stopOrder)


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

            #place stop order
            stopOrder = Order(accountId = self.__strategy.accountId,
                          action = Action.SELL,
                          type = Type.STOP,
                          symbol = self.__symbol,
                          price = tick.close * 0.95,
                          share = 0 - share)
            self.__placeStopOrder(stopOrder)

    def __placeStopOrder(self, order):
        ''' place stop order '''
        orderId = self.__strategy.placeOrder(order)
        if orderId:
            self.__stopOrderId = orderId
            self.__stopOrder = order
        else:
            LOG.error("Can't place stop order %s" % order)

    def __sellIfMeet(self, tick):
        ''' place sell order if conditions meet '''
        pass

    def orderExecuted(self, orderId):
        ''' call back for executed order '''
        if orderId == self.__stopOrderId:
            LOG.debug("smaStrategy stop order canceled %s" % orderId)
            # stop order executed
            self.__clearStopOrder()

    def __clearStopOrder(self):
        ''' clear stop order status '''
        self.__stopOrderId = None
        self.__stopOrder = None

    def __adjustStopOrder(self, tick):
        ''' update stop order if needed '''
        if not self.__stopOrderId:
            return

        if self.__stopOrder.action == Action.SELL:
            orgStopPrice = self.__buyOrder.price * 0.95
            newStopPrice = max(((tick.close + orgStopPrice) / 2), tick.close * 0.85)
            newStopPrice = min(newStopPrice, tick.close * 0.95)

            if newStopPrice > self.__stopOrder.price:
                self.__strategy.tradingEngine.cancelOrder(self.__symbol, self.__stopOrderId)
                stopOrder = Order(accountId = self.__strategy.accountId,
                                  action = Action.SELL,
                                  type = Type.STOP,
                                  symbol = self.__symbol,
                                  price = newStopPrice,
                                  share = self.__stopOrder.share)
                self.__placeStopOrder(stopOrder)
        '''
        elif self.__stopOrder.action == Action.BUY_TO_COVER:
            orgStopPrice = self.__buyOrder.price * 1.05
            newStopPrice = min(((orgStopPrice + tick.close) / 2), tick.close * 1.15)
            newStopPrice = max(newStopPrice, tick.close * 1.05)

            if newStopPrice < self.__stopOrder.price:
                self.__strategy.tradingEngine.cancelOrder(self.__symbol, self.__stopOrderId)
                stopOrder = Order(accountId = self.__strategy.accountId,
                                  action = Action.BUY_TO_COVER,
                                  type = Type.STOP,
                                  symbol = self.__symbol,
                                  price = newStopPrice,
                                  share = self.__stopOrder.share)
                self.__placeStopOrder(stopOrder)
        '''

    def __updatePreviousState(self, tick):
        ''' update previous state '''
        self.__previousTick = tick
        self.__previousSmaShort = self.__smaShort.getLastValue()
        self.__previousSmaMid = self.__smaMid.getLastValue()
        self.__previousSmaLong = self.__smaLong.getLastValue()
        self.__previousSmaVolumeShort = self.__smaVolumeShort.getLastValue()
        self.__previousSmaVolumeMid = self.__smaVolumeMid.getLastValue()
        self.__previousMovingLowShort = self.__movingLowShort.getLastValue()
        self.__previousMovingLowWeek = self.__movingLowWeek.getLastValue()

    def tickUpdate(self, tick):
        ''' consume ticks '''
        LOG.debug("tickUpdate %s with tick %s, price %s" % (self.__symbol, tick.time, tick.close))
        # update sma
        self.__smaShort(tick.close)
        self.__smaMid(tick.close)
        self.__smaLong(tick.close)
        self.__smaVolumeShort(tick.volume)
        self.__smaVolumeMid(tick.volume)
        self.__movingLowShort(tick.close)
        self.__movingLowWeek(tick.close)

        # if not enough data, skip to reduce risk -- SKIP NEWLY IPOs
        if not self.__smaLong.getLastValue() or not self.__smaMid.getLastValue() or not self.__smaShort.getLastValue():
            self.__updatePreviousState(tick)
            return

        #if haven't started, don't do any trading
        if tick.time <= self.__startDate:
            return

        # already have some holdings
        if self.__stopOrderId:
            self.__sellIfMeet(tick)
            self.__adjustStopOrder(tick)


        # don't have any holdings
        if not self.__stopOrderId and self.__getCashToBuyStock():
            self.__buyIfMeet(tick)

        self.__updatePreviousState(tick)

