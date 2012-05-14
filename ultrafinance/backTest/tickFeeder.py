'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import UfException, Errors
from threading import Thread

from ultrafinance.backTest.appGlobal import appGlobal
from ultrafinance.backTest.constant import TRADE_TYPE, TICK, QUOTE

import time
import logging
LOG = logging.getLogger()

class TickFeeder(object):
    ''' constructor
        no tick operation should take more that 2 second
        threadMaxFails indicates how many times thread for a subscriber can timeout,
        if it exceeds, them unregister that subscriber
    '''
    def __init__(self, intervalTimeout = 2):
        self.__subs = {} # securityIds: sub
        self.__source = {}
        self.__intervalTimeout = intervalTimeout
        self.start = 0
        self.end = None
        self.tradingCenter = None
        self.__updatedTick = None

    def getUpdatedTick(self):
        ''' return timeTickTuple with status changes '''
        timeTicksTuple = self.__updatedTick
        self.__updatedTick = None

        return timeTicksTuple

    def indexTicks(self):
        ''' generate timeTicksDict base on source DAM'''
        LOG.debug('Start indexing ticks, it may take a while......')
        timeTicksDict = {}
        for symbol, dam in self.__source.items():
            LOG.debug('Indexing ticks for %s' % symbol)
            ticks = []
            if TICK == appGlobal[TRADE_TYPE]:
                ticks = dam.readTicks(self.start, self.end)
            elif QUOTE == appGlobal[TRADE_TYPE]:
                ticks = dam.readQuotes(self.start, self.end)
            else:
                raise UfException(Errors.INVALID_TYPE,
                                  'Type %s is not accepted' % appGlobal[TRADE_TYPE])

            for tick in ticks:
                if tick.time not in timeTicksDict:
                    timeTicksDict[tick.time] = {}

                timeTicksDict[tick.time][symbol] = tick

        return timeTicksDict

    def execute(self):
        ''' execute func '''
        timeTicksDict = self.indexTicks()

        for timeStamp in sorted(timeTicksDict.iterkeys()):
            self._freshUpdatedTick(timeStamp, timeTicksDict[timeStamp])
            self._freshTradingCenter(timeTicksDict[timeStamp])

    def _freshUpdatedTick(self, timeStamp, symbolTicksDict):
        ''' update self.__updatedTick '''
        curTime = time.time()
        while (curTime + self.__intervalTimeout > time.time()):
            if not self.__updatedTick:
                self.__updatedTick = (timeStamp, symbolTicksDict)
                return
            else:
                # sleep for a small amount of time
                time.sleep(0)

        raise UfException(Errors.FEEDER_TIMEOUT,
                          "Can't do freshUpdateTick in %s seconds" % self.__intervalTimeout)

    def _freshTradingCenter(self, symbolTicksDict):
        ''' feed trading center ticks '''
        self.tradingCenter.consumeTicks(symbolTicksDict)

    def complete(self):
        ''' call when complete feeding ticks '''
        pass

    def addSource(self, dam):
        ''' add a source '''
        if dam.symbol in self.__source:
            raise UfException(Errors.SYMBOL_EXIST,
                              "Can't add dam with existing symbol: %s" % dam.symbol)

        else:
            self.__source[dam.symbol] = dam

    def pubTicks(self, ticks, sub):
        ''' publish ticks to sub '''
        thread = Thread(target = sub.doConsume, args = (ticks,))
        thread.start()
        return thread
