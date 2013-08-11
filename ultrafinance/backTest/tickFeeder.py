'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import UfException, Errors
from threading import Thread

from ultrafinance.backTest.appGlobal import appGlobal
from ultrafinance.backTest.constant import TRADE_TYPE, TICK, QUOTE
from ultrafinance.lib.util import split_dict_equally

import traceback
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
        self.timeTicksDict = {}
        self.indexTicksDict = {}

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

        dam.destruct()

        return ticks

    def __loadTicks(self):
        ''' generate timeTicksDict based on source DAM'''
        LOG.info('Start loading ticks, it may take a while......')

        threads = []
        for partSource in split_dict_equally(self.__source, 20):
            if partSource:
                thread = Thread(target = self.__loadPartTicks, args = (partSource,))
                thread.setDaemon(False)
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join(2 * len(self.__source)) # wait for enough time


    def __loadPartTicks(self, partSource):
        ''' publish ticks to sub '''
        for symbol, dam in partSource.items():
            LOG.info('Indexing ticks for %s' % symbol)
            try:
                ticks = self._getTicks(dam)

                for tick in ticks:
                    if tick.time not in self.timeTicksDict:
                        self.timeTicksDict[tick.time] = {}

                    self.timeTicksDict[tick.time][symbol] = tick
            except KeyboardInterrupt as ki:
                LOG.warn("Interrupted by user  when loading ticks for %s" % symbol)
                raise ki
            except BaseException as excp:
                LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (symbol, excp, traceback.format_exc(8)))


    def __loadIndex(self):
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
        self.__loadTicks()
        self.__loadIndex()

        for timeStamp in sorted(self.timeTicksDict.iterkeys()):
            while self.__updatedTick:
                time.sleep(0)

            # make sure trading center finish updating first
            self._freshTradingCenter(self.timeTicksDict[timeStamp])
            self._freshIndexHelper(self.indexTicksDict.get(timeStamp))

            self._freshUpdatedTick(timeStamp, self.timeTicksDict[timeStamp])
            self._updateHistory(timeStamp, self.timeTicksDict[timeStamp], self.indexTicksDict.get(timeStamp))

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
        thread.setDaemon(False)
        thread.start()
        return thread
