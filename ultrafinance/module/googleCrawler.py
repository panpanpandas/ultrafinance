'''
Created on Dec 4, 2011

@author: ppa
'''
from ultrafinance.dam.DAMFactory import DAMFactory

from os import path
import time

from threading import Thread
from threading import Lock

import logging
LOG = logging.getLogger()


THREAD_TIMEOUT = 5
MAX_TRY = 3

class GoogleCrawler(object):
    ''' collect quotes/ticks for a list of symbol '''
    def __init__(self, symbols, start, poolsize = 5):
        ''' constructor '''
        self.symbols = symbols
        self.sqlLocation = None
        self.outputDAM = DAMFactory.createDAM("sql", self.__getOutputDamSetting())
        self.googleDAM = DAMFactory.createDAM("google")
        self.start = start
        self.end = None
        self.poolsize = poolsize
        self.readLock = Lock()
        self.writeLock = Lock()
        self.failed = []
        self.succeeded = []

    def __getOutputDamSetting(self):
        self.sqlLocation = 'sqlite:///%s' % self.__getOutputSql()
        LOG.info("Sqlite location: %s" % self.sqlLocation)
        return {'db': self.sqlLocation}

    def __getOutputSql(self):
        return path.join("/"
                         "data",
                         "stock.sqlite")

    def __getSaveOneSymbol(self, symbol):
        ''' get and save data for one symbol '''
        try:
            lastExcp = None
            with self.readLock: #dam is not thread safe
                failCount = 0
                #try several times since it may fail
                while failCount < MAX_TRY:
                    try:
                        self.googleDAM.setSymbol(symbol)
                        quotes = self.googleDAM.readQuotes(self.start, self.end)

                    except BaseException as excp:
                        failCount += 1
                        lastExcp = excp
                    else:
                        break

                if failCount >= MAX_TRY:
                    raise BaseException("Can't retrieve historical data %s" % lastExcp)

            with self.writeLock: #dam is not thread safe
                self.outputDAM.setSymbol(symbol)
                self.outputDAM.writeQuotes(quotes)

        except BaseException as excp:
            LOG.info("Error while processing %s: %s" % (symbol, excp))
            self.failed.append(symbol)
        else:
            LOG.info("Processed %s" % symbol)
            self.succeeded.append(symbol)

    def getAndSaveSymbols(self):
        ''' get and save data '''
        counter = 0
        rounds = 0

        while counter < len(self.symbols):
            size = len(self.symbols) - counter
            if self.poolsize < size:
                size = self.poolsize
            symbols = self.symbols[counter: counter + size]

            threads = []
            for symbol in symbols:
                thread = Thread(name = symbol, target = self.__getSaveOneSymbol, args = [symbol])
                thread.daemon = True
                thread.start()

                threads.append(thread)

            for thread in threads:
                thread.join(THREAD_TIMEOUT) # no need to block, because thread should complete at last

            #can't start another thread to do commit because for sqlLite, only object for the same thread can be commited
            if 0 == rounds % 3:
                self.outputDAM.commit()

            counter += size
            rounds += 1

            # sleep for 3 second to avoid being blocked by google...
            time.sleep(5)

if __name__ == '__main__':
    crawler = GoogleCrawler(["AAPL", "EBAY", "GOOG"], "20131101")
    crawler.getAndSaveSymbols()
    print("Sqlite location: %s" % crawler.sqlLocation)
    print("Succeeded: %s" % crawler.succeeded)
    print("Failed: %s" % crawler.failed)

