'''
Created on July 08, 2013

This strategy leverage 10/50/200 days Simple Moving Average(SMA) as short/mid/long term trend


When to Sell:
1 when stop order is hit
2 if the 10 < 50 or 10 < 200, place sell order

Stop order:
1 when buy order is placed, set limit order to be 5%
2 as time goes, increase limit price to be half of the profit
3 never decrease limit price

When to Buy:
1 if 10 < 200 && 50 < 200, skip
2 if previous day price jump more than 10%, skip
3 if the previous day 10 < 200, and today 10 > 200, place buy order
4 if previous day 200 < 10 < 50, and today 200 < 50 < 10, place buy order
5 always place a stop order


@author: ppa
'''
from ultrafinance.model import Side, Order
from ultrafinance.backTest.tickSubscriber.strategies.baseStrategy import BaseStrategy
from ultrafinance.pyTaLib.indicator import Sma
import math

import logging
LOG = logging.getLogger()

class SMAStrategy(BaseStrategy):
    ''' period strategy '''
    def __init__(self, configDict):
        ''' constructor '''
        super(SMAStrategy, self).__init__("smaStrategy")
        self.configDict = configDict

        self.symbols = None

        # order id
        self.__stopOrderId = None
        self.__stopOrder = None
        self.__buyOrder = None

        self.__smaShort = Sma(10)
        self.__smaMid = Sma(50)
        self.__smaLong = Sma(200)

        #state of privious day
        self.__previousTick = None
        self.__previousSmaShort = None
        self.__previousSmaMid = None
        self.__previousSmaLong = None


    def __buyIfMeet(self, tick, symbol):
        ''' place buy order if conditions meet '''
        if self.__smaShort.getLastValue() < self.__smaLong.getLastValue() and self.__smaMid.getLastValue() < self.__smaLong.getLastValue():
            return

        if tick.close/self.__previousTick.close > 1.1:
            return

        if self.__previousSmaShort < self.__previousSmaLong and self.__smaShort.getLastValue() > self.__smaLong.getLastValue():
            # assume no commission fee for now
            self.__placeBuyOrder(tick, symbol)

        elif self.__previousSmaLong < self.__previousSmaShort < self.__previousSmaMid and self.__smaLong.getLastValue() < self.__smaMid.getLastValue() < self.__smaShort.getLastValue():
            # assume no commission fee for now
            self.__placeBuyOrder(tick, symbol)


    def __placeBuyOrder(self, tick, symbol):
        ''' place buy order'''
        share = math.floor(self.getAccountCopy().getCash() / float(tick.close))
        buyOrder = Order(accountId = self.accountId,
                                  side = Side.BUY,
                                  symbol = symbol,
                                  price = tick.close,
                                  share = share)
        if self.placeOrder(buyOrder):
            self.__buyOrder = buyOrder

            #place stop order
            stopOrder = Order(accountId = self.accountId,
                          side = Side.STOP,
                          symbol = symbol,
                          price = tick.close * 0.95,
                          share = share)
            self.__placeStopOrder(stopOrder)

    def __placeStopOrder(self, order):
        ''' place stop order '''
        orderId = self.placeOrder(order)
        if orderId:
            self.__stopOrderId = orderId
            self.__stopOrder = order
        else:
            LOG.error("Can't place stop order %s" % order)

    def __sellIfMeet(self, tick, symbol):
        ''' place sell order if conditions meet '''
        if self.__smaShort.getLastValue() < self.__smaLong.getLastValue() or self.__smaShort.getLastValue() < self.__smaMid.getLastValue():
            self.placeOrder(Order(accountId = self.accountId,
                                  side = Side.SELL,
                                  symbol = symbol,
                                  price = tick.close,
                                  share = self.__stopOrder.share) )
            self.tradingEngine.cancelOrder(self.__stopOrderId)
            self.__clearStopOrder()

    def orderExecuted(self, orderId):
        ''' call back for executed order '''
        if orderId == self.__stopOrderId:
            # stop order executed
            self.__clearStopOrder()

    def __clearStopOrder(self):
        ''' clear stop order status '''
        self.__stopOrderId = None
        self.__stopOrder = None

    def __adjustStopOrder(self, tick, symbol):
        ''' update stop order if needed '''
        newStopPrice = + self.__buyOrder.price + ((tick.close - self.__buyOrder.price) / 2)
        if self.__stopOrderId and newStopPrice > self.__stopOrder.price:
            self.tradingEngine.cancelOrder(self.__stopOrderId)
            stopOrder = Order(accountId = self.accountId,
                              side = Side.STOP,
                              symbol = symbol,
                              price = newStopPrice,
                              share = self.__stopOrder.share)
            self.__placeStopOrder(stopOrder)

    def updatePreviousState(self, tick):
        ''' update privous state '''
        self.__previousTick = tick
        self.__previousSmaShort = self.__smaShort.getLastValue()
        self.__previousSmaMid = self.__smaMid.getLastValue()
        self.__previousSmaLong = self.__smaLong.getLastValue()


    def tickUpdate(self, tickDict):
        ''' consume ticks '''
        assert self.symbols
        assert self.symbols[0] in tickDict.keys()
        symbol = self.symbols[0]
        tick = tickDict[symbol]

        # update sma
        self.__smaShort(tick.close)
        self.__smaMid(tick.close)
        self.__smaLong(tick.close)

        # if not enough data, skip to reduce risk -- SKIP NEWLY IPOs
        if not self.__smaLong.getLastValue() or not self.__smaMid.getLastValue() or not self.__smaShort.getLastValue():
            self.updatePreviousState(tick)
            return

        # don't have any holdings
        if not self.__stopOrderId:
            self.__buyIfMeet(tick, symbol)

        # already have some holdings
        else:
            self.__sellIfMeet(tick, symbol)
            self.__adjustStopOrder(tick, symbol)


        self.updatePreviousState(tick)

