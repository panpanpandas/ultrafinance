'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.backTest.constant import EVENT_TICK_UPDATE, EVENT_ORDER_EXECUTED
from ultrafinance.backTest.constant import STATE_SAVER_UPDATED_ORDERS, STATE_SAVER_PLACED_ORDERS

from threading import Thread
from time import sleep
import json

import logging
LOG = logging.getLogger()

class TradingEngine(object):
    ''' constructor
        no tick operation should take more that 0.5 second
        threadMaxFails indicates how many times thread for a subscriber can timeout,
        if it exceeds, them unregister that subscriber
    '''
    def __init__(self, threadTimeout = 2, threadMaxFail = 10):
        self.__subs = {} # {'event': {sub: {symbols: sub} }
        self.tickProxy = None
        self.orderProxy = None
        self.saver = None
        self.__threadTimeout = threadTimeout
        self.__threadMaxFail = threadMaxFail
        self.__curTime = ""
        self.__stop = False

    def stop(self):
        ''' set stop flag '''
        self.__stop = True

    def validateSub(self, sub):
        ''' validate subscriber '''
        symbols, rules = sub.subRules()

        '''
        if not symbols:
            raise UfException(Errors.SYMBOL_NOT_IN_SOURCE,
                               "can't find any symbol with re %s in source %s" % (symbolRe, self.__source.keys()))
        '''
        #TODO: validate rules
        return symbols, rules, sub

    def register(self, sub):
        ''' register a subscriber
            rule is not used for now
        '''
        symbols, events, sub = self.validateSub(sub)

        for event in events:
            if event not in self.__subs:
                self.__subs[event] = {}

            self.__subs[event][sub] = {'symbols': symbols, 'fail': 0}
            LOG.debug('register %s with id %s to event %s, symbols %s'
                      % (sub.name, sub.subId, event, symbols))

    def unregister(self, sub):
        ''' unregister'''
        for event, subDict in self.__subs.items():
            if sub in subDict.keys():
                del self.__subs[event][sub]

                # remove whole subs[event] if it's empty
                if not self.__subs[event]:
                    del self.__subs[event]

                LOG.debug('unregister %s with id %s' % (sub.name, sub.subId))


    #TODO: in real time trading, change this function
    def runListener(self):
        ''' execute func '''

        while True:
            if self.__stop:
                LOG.debug("Stopping trading engine...")
                self._complete()
                break

            else:
                timeTicksTuple = self.tickProxy.getUpdatedTick()

                if not timeTicksTuple:
                    sleep(0)
                    continue

                if timeTicksTuple:
                    self.__curTime = timeTicksTuple[0]
                    self._tickUpdate(timeTicksTuple)

                updatedOrderDict = self.orderProxy.getUpdatedOrder()
                placedOrderDict = self.orderProxy.getPlacedOrder()
                if updatedOrderDict:
                    self._orderUpdate(updatedOrderDict)

                #record order
                if self.saver:
                    self.saver.write(self.__curTime, STATE_SAVER_UPDATED_ORDERS, json.dumps([str(order) for order in updatedOrderDict.values()]))
                    self.saver.write(self.__curTime, STATE_SAVER_PLACED_ORDERS, json.dumps([str(order) for order in placedOrderDict.values()]))

                self.tickProxy.clearUpdateTick()

    def _complete(self):
        ''' call when complete feeding ticks '''
        for subDict in self.__subs.itervalues():
            for sub in subDict.iterkeys():
                sub.complete()

    def consumeTicks(self, ticks, sub, event):
        ''' publish ticks to sub '''
        thread = Thread(target = getattr(sub, event), args = (ticks,))
        thread.setDaemon(False)
        thread.start()
        return thread

    def consumeExecutedOrders(self, orderDict, sub, event):
        ''' publish ticks to sub '''
        thread = Thread(target = getattr(sub, event), args = (orderDict,))
        thread.setDaemon(False)
        thread.start()
        return thread


    def placeOrder(self, order):
        ''' called by each strategy to place order '''
        orderId = self.orderProxy.placeOrder(order)
        return orderId

    def cancelOrder(self, symbol, orderId):
        ''' cancel order '''
        self.orderProxy.cancelOrder(symbol, orderId)

    def _orderUpdate(self, orderDict):
        '''
        order status changes
        '''
        event = EVENT_ORDER_EXECUTED
        for sub, attrs in self.__subs[EVENT_ORDER_EXECUTED].items():
            thread = self.consumeExecutedOrders(orderDict, sub, event)
            thread.join(timeout = self.__threadTimeout * 1000)
            if thread.isAlive():
                LOG.error("Thread timeout for order update subId %s" % sub.subId)
                attrs['fail'] += 1

            if attrs['fail'] > self.__threadMaxFail:
                LOG.error("For order update, subId %s fails for too many times" % sub.subId)
                self.unregister(sub)

    def _tickUpdate(self, timeTicksTuple):
        ''' got tick update '''
        time, symbolTicksDict = timeTicksTuple
        #TODO: remove hard coded event
        #This should not happen
        event = EVENT_TICK_UPDATE
        if event not in self.__subs:
            LOG.warn("EVENT_TICK_UPDATE not in self.__subs %s" % self.__subs)
            return

        for sub, attrs in self.__subs[event].items():
            ticks = {}
            for symbol in attrs['symbols']:
                if symbol in symbolTicksDict:
                    ticks[symbol] = symbolTicksDict[symbol]

            thread = self.consumeTicks(ticks, sub, event)
            thread.join(timeout = self.__threadTimeout * 1000)
            if thread.isAlive():
                LOG.error("Thread timeout for tick update, subId %s at time %s" % (sub.subId, time))
                attrs['fail'] += 1

            if attrs['fail'] > self.__threadMaxFail:
                LOG.error("For tick update, subId %s fails for too many times" % sub.subId)
                self.unregister(sub)

        if self.saver and len(symbolTicksDict) < 10:
            for symbol in symbolTicksDict:
                self.saver.write(self.__curTime, symbol, str(symbolTicksDict[symbol]))
