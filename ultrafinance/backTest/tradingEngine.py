'''
Created on Nov 6, 2011

@author: ppa
'''

from ultrafinance.lib.errors import UfException, Errors
from ultrafinance.backTest.appGlobal import appGlobal
from ultrafinance.backTest.constant import EVENT_TICK_UPDATE, STOP_FLAG

import json
from threading import Thread
from time import sleep

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
            if appGlobal[STOP_FLAG]:
                self.complete()
                break

            else:
                timeTicksTuple = self.tickProxy.getUpdatedTick()
                orderDict = self.orderProxy.getUpdatedOrder()

                if not timeTicksTuple and not orderDict:
                    sleep(0)
                    continue

                if timeTicksTuple:
                    self.__curTime = timeTicksTuple[0]
                    self._tickUpdate(timeTicksTuple)

                if orderDict:
                    self._orderUpdate(orderDict)

    def complete(self):
        ''' call when complete feeding ticks '''
        for event, subDict in self.__subs.items():
            for sub in subDict.iterkeys():
                sub.complete()

        #write to saver
        if self.saver:
            LOG.debug("Writing state to saver")
            self.saver.writeComplete()

    def consumeTicks(self, ticks, sub, event):
        ''' publish ticks to sub '''
        thread = Thread(target = getattr(sub, event), args = (ticks,))
        thread.start()
        return thread

    def placeOrder(self, order):
        ''' called by each strategy to place order '''
        self.orderProxy.placeOrder(order)

        # record order
        if self.saver:
            self.saver.write(self.__curTime, 'placedOrder', order)

    def _orderUpdate(self, orderDict):
        '''
        order status changes
        '''
        if self.saver:
            self.saver.write(self.__curTime, 'updatedOrder', [str(order) for order in orderDict.values()])

    def _tickUpdate(self, timeTicksTuple):
        ''' got tick update '''
        time, symbolTicksDict = timeTicksTuple
        #TODO: remove hard coded event
        event = EVENT_TICK_UPDATE
        for sub, attrs in self.__subs[EVENT_TICK_UPDATE].items():
            ticks = {}
            for symbol in attrs['symbols']:
                if symbol not in symbolTicksDict:
                    LOG.error("For %s with subId %s, symbol %s does't exist at time %s"\
                              % (sub.name, sub.subId, symbol, time))
                    attrs['fail'] += 1
                else:
                    ticks[symbol] = symbolTicksDict[symbol]

            thread = self.consumeTicks(ticks, sub, event)
            thread.join(timeout = self.__threadTimeout * 1000)
            if thread.isAlive():
                LOG.error("thread timeout for subId %s at time %s" % (sub.subId, time))
                attrs['fail'] += 1

            if attrs['fail'] > self.__threadMaxFail:
                LOG.error("subId %s fails for too many times" % sub.subId)
                self.unregister(sub)

        if self.saver:
            for symbol in symbolTicksDict:
                self.saver.write(self.__curTime, symbol, str(symbolTicksDict[symbol]))
