'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import UfException, Errors
from threading import Thread
from time import sleep

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
        self.__indexDam = None
        self.tradingCenter = None
        self.indexHelper = None
        self.hisotry = None
        self.__updatedTick = None

    def getUpdatedTick(self):
        ''' return timeTickTuple with status changes '''
        timeTicksTuple = self.__updatedTick

        return timeTicksTuple

    def clearUpdateTick(self):
        ''' clear current ticks '''
        self.__updatedTick = None


    def _getTicks(self, dam):
        ''' get ticks from one dam'''
        ticks = []
        if TICK == appGlobal[TRADE_TYPE]:
            ticks = dam.readTicks(self.start, self.end)
        elif QUOTE == appGlobal[TRADE_TYPE]:
            ticks = dam.readQuotes(self.start, self.end)
        else:
            raise UfException(Errors.INVALID_TYPE,
                              'Type %s is not accepted' % appGlobal[TRADE_TYPE])

        return ticks

    def loadTicks(self):
        ''' generate timeTicksDict based on source DAM'''
        LOG.debug('Start loading ticks, it may take a while......')
        timeTicksDict = {}
        for symbol, dam in self.__source.items():
            LOG.debug('Indexing ticks for %s' % symbol)
            ticks = self._getTicks(dam)

            for tick in ticks:
                if tick.time not in timeTicksDict:
                    timeTicksDict[tick.time] = {}

                timeTicksDict[tick.time][symbol] = tick

        return timeTicksDict

    def loadIndex(self):
        ''' generate timeTicksDict based on source DAM'''
        LOG.debug('Start loading ticks, it may take a while......')
        indexTicksDict = {}

        LOG.debug('loading index...')
        ticks = self._getTicks(self.__indexDam)

        for tick in ticks:
            indexTicksDict[tick.time] = tick

        return indexTicksDict

    def execute(self):
        ''' execute func '''
        timeTicksDict = self.loadTicks()
        indexTicksDict = self.loadIndex()

        for timeStamp in sorted(timeTicksDict.iterkeys()):
            while self.__updatedTick:
                time.sleep(0)

            # make sure trading center finish updating first
            self._freshTradingCenter(timeTicksDict[timeStamp])
            self._freshIndexHelper(indexTicksDict.get(timeStamp))

            self._freshUpdatedTick(timeStamp, timeTicksDict[timeStamp])
            self._updateHistory(timeStamp, timeTicksDict[timeStamp], indexTicksDict.get(timeStamp))

    def _updateHistory(self, timeStamp, symbolTicksDict, indexTick):
        ''' update history '''
        self.hisotry.update(timeStamp, symbolTicksDict, indexTick)

    def _freshUpdatedTick(self, timeStamp, symbolTicksDict):
        ''' update self.__updatedTick '''
        self.__updatedTick = (timeStamp, symbolTicksDict)

    def _freshTradingCenter(self, symbolTicksDict):
        ''' feed trading center ticks '''
        self.tradingCenter.consumeTicks(symbolTicksDict)

    def _freshIndexHelper(self, tick):
        ''' update self.__updatedTick '''
        self.indexHelper.appendTick(tick)

    def complete(self):
        ''' call when complete feeding ticks '''
        pass

    def setIndexDam(self, dam):
        ''' set index dam '''
        self.__indexDam = dam

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
