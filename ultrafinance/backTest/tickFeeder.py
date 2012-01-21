'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import UfException, Errors
from ultrafinance.backTest.btUtil import findInListbyRe
from threading import Thread

import logging
LOG = logging.getLogger()

class TickFeeder(object):
    ''' constructor
        no tick operation should take more that 0.5 second
        threadMaxFails indicates how many times thread for a subscriber can timeout,
        if it exceeds, them unregister that subscriber
        TODO: read from config
    '''
    QUOTE_TYPE = 'quote'
    TICK_TYPE = 'tick'
    TYPES = [QUOTE_TYPE, TICK_TYPE]

    def __init__(self, threadTimeout = 2, threadMaxFail = 10):
        self.__subs = {} # securityIds: sub
        self.__source = {}
        self.__inputType = TickFeeder.QUOTE_TYPE
        self.__threadTimeout = threadTimeout
        self.__threadMaxFail = threadMaxFail
        self.start = 0
        self.end = None

    def validate(self, sub):
        ''' validate subscriber '''
        symbolRe, rules = sub.subRules()

        symbols = self.getSymbolsByRe(symbolRe)
        if not symbols:
            raise UfException(Errors.SYMBOL_NOT_IN_SOURCE,
                              "can't find any symbol with re %s in source %s" % (symbolRe, self.__source.keys()))

        return symbols, sub

    def getSymbolsByRe(self, symbolRe):
        ''' get symbols by regular expression'''
        symbols = findInListbyRe(self.__source.keys(), symbolRe)
        return symbols

    def addSource(self, dam):
        ''' add a source '''
        if dam.symbol in self.__source:
            raise UfException(Errors.SYMBOL_EXIST,
                              "Can't add dam with existing symbol: %s" % dam.symbol)

        self.__source[dam.symbol] = dam

    def register(self, sub):
        ''' register a subscriber
            rule is not used for now
        '''
        symbols, sub= self.validate(sub)
        self.__subs[sub] = {'symbols': symbols,
                            'fail': 0}

    def unregister(self, subId):
        ''' unregister'''
        if subId in self.__subs:
            del self.__subs[subId]

    def indexTicks(self):
        ''' generate timeTicksDict base on source DAM'''
        self.validateType(self.__inputType)

        timeTicksDict = {}
        for symbol, dam in self.__source.items():
            LOG.debug('Indexing ticks for %s' % symbol)
            ticks = []
            if TickFeeder.TICK_TYPE == self.__inputType:
                ticks = dam.readTicks(self.start, self.end)
            else:
                ticks = dam.readQuotes(self.start, self.end)

            for tick in ticks:
                if tick.time not in timeTicksDict:
                    timeTicksDict[tick.time] = {}

                timeTicksDict[tick.time][symbol] = tick

        return timeTicksDict

    def execute(self):
        ''' execute func '''
        timeTicksDict = self.indexTicks()
        for time in sorted(timeTicksDict.iterkeys()):
            for sub, attrs in self.__subs.items():
                ticks = {}
                for symbol in attrs['symbols']:
                    if symbol not in timeTicksDict[time]:
                        LOG.error("For subId %s, symbol %s does't exist at time %s"\
                                  % (sub.subId, symbol, time))
                        attrs['fail'] += 1
                    else:
                        ticks[symbol] = timeTicksDict[time][symbol]

                thread = self.pubTicks(ticks, sub)
                thread.join(timeout = self.__threadTimeout * 1000)
                if thread.isAlive():
                    LOG.error("thread timeout for subId %s at time %s" % (sub.subId, time))
                    attrs['fail'] += 1

                if attrs['fail'] > self.__threadMaxFail:
                    LOG.error("subId %s fails for too many times" % sub.subId)
                    self.unregister(sub)


    def complete(self):
        ''' call when complete feeding ticks '''
        for sub in self.__subs.iterkeys():
            sub.complete()

    def pubTicks(self, ticks, sub):
        ''' publish ticks to sub '''
        thread = Thread(target = sub.doConsume, args=(ticks, ))
        thread.start()
        return thread

    def getSubs(self):
        ''' get all subs, should not be used to change any sub '''
        return self.__subs

    def __getInputType(self):
        ''' get type '''
        return self.__inputType

    def __setInputType(self, inputType):
        ''' set type '''
        self.validateType(inputType)
        self.__inputType = inputType

    def validateType(self, inputType):
        if inputType not in TickFeeder.TYPES:
            raise UfException(Errors.INVALID_TYPE,
                              'Type %s is not accepted, allow types: %s' % (inputType, TickFeeder.TYPES) )

    inputType = property(__getInputType, __setInputType)
