'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import UfException, Errors
from threading import Thread

from ultrafinance.backTest.appGlobal import appGlobal
from ultrafinance.backTest.constant import TRADE_TYPE, TICK, QUOTE
from ultrafinance.backTest.constant import STATE_SAVER_INDEX_PRICE

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
    def __init__(self, intervalTimeout = 2, start = 0, end = None):
        self.__subs = {} # securityIds: sub
        self.__symbols = []
        self.__indexSymbol = None
        self.__dam = None
        self.__intervalTimeout = intervalTimeout
        self.start = start
        self.end = end
        self.tradingCenter = None
        self.saver = None
        self.__updatedTick = None
        self.timeTicksDict = {}
        self.iTimePositionDict = {}

    def getUpdatedTick(self):
        ''' return timeTickTuple with status changes '''
        timeTicksTuple = self.__updatedTick

        return timeTicksTuple

    def clearUpdateTick(self):
        ''' clear current ticks '''
        self.__updatedTick = None


    def _getSymbolTicksDict(self, symbols):
        ''' get ticks from one dam'''
        ticks = []
        if TICK == appGlobal[TRADE_TYPE]:
            ticks = self.__dam.readBatchTupleTicks(symbols, self.start, self.end)
        elif QUOTE == appGlobal[TRADE_TYPE]:
            ticks = self.__dam.readBatchTupleQuotes(symbols, self.start, self.end)
        else:
            raise UfException(Errors.INVALID_TYPE,
                              'Type %s is not accepted' % appGlobal[TRADE_TYPE])

        return ticks

    def __loadTicks(self):
        ''' generate timeTicksDict based on source DAM'''
        LOG.info('Start loading ticks, it may take a while......')

        LOG.info('Indexing ticks for %s' % self.__symbols)
        try:
            self.timeTicksDict = self._getSymbolTicksDict(self.__symbols)

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for %s" % self.__symbols)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.__symbols, excp, traceback.format_exc(8)))


    def __loadIndex(self):
        ''' generate timeTicksDict based on source DAM'''
        LOG.debug('Start loading index ticks, it may take a while......')
        try:
            return self._getSymbolTicksDict([self.__indexSymbol])

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for %s" % self.__indexSymbol)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.__indexSymbol, excp, traceback.format_exc(8)))

        return {}

    def execute(self):
        ''' execute func '''
        self.__loadTicks()

        for timeStamp in sorted(self.timeTicksDict.iterkeys()):
            # make sure trading center finish updating first
            self._freshTradingCenter(self.timeTicksDict[timeStamp])

            self._freshUpdatedTick(timeStamp, self.timeTicksDict[timeStamp])
            #self._updateHistory(timeStamp, self.timeTicksDict[timeStamp], self.indexTicksDict.get(timeStamp))

            while self.__updatedTick:
                time.sleep(0)

    def _freshUpdatedTick(self, timeStamp, symbolTicksDict):
        ''' update self.__updatedTick '''
        self.__updatedTick = (timeStamp, symbolTicksDict)

    def _freshTradingCenter(self, symbolTicksDict):
        ''' feed trading center ticks '''
        self.tradingCenter.consumeTicks(symbolTicksDict)

    def complete(self):
        '''
        call when complete feeding ticks
        write history to saver
        '''
        try:
            if not self.saver:
                return

            timeITicksDict = self.__loadIndex()
            if timeITicksDict:
                for time, symbolDict in timeITicksDict.iteritems():
                    for symbol in symbolDict.keys():
                        self.saver.write(time, STATE_SAVER_INDEX_PRICE, symbolDict[symbol].close)
                        self.iTimePositionDict[time] = symbolDict[symbol].close
                        break # should only have one benchmark


        except Exception as ex:
            LOG.warn("Unknown error when recording index info:" + str(ex))

    def setSymbols(self, symbols):
        ''' set symbols '''
        self.__symbols = symbols

    def setIndexSymbol(self, indexSymbol):
        ''' set symbols '''
        self.__indexSymbol = indexSymbol


    def setDam(self, dam):
        ''' set source dam '''
        self.__dam = dam

    def pubTicks(self, ticks, sub):
        ''' publish ticks to sub '''
        thread = Thread(target = sub.doConsume, args = (ticks,))
        thread.setDaemon(False)
        thread.start()
        return thread
