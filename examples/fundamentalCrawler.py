'''
Created on Dec 4, 2011

@author: ppa
'''
from ultrafinance.dam.DAMFactory import DAMFactory
from os import path
import optparse

from threading import Thread
from threading import Lock

BATCH_SIZE = 30
THREAD_TIMEOUT = 5
MAX_TRY = 3

class FundamentalCrawler(object):
    ''' collect fundamental for a list of symbol '''
    def __init__(self):
        ''' constructor '''
        self.symbols = []
        self.outputDAM = None
        self.googleDAM = None
        self.readLock = Lock()
        self.writeLock = Lock()
        self.failed = []
        self.succeeded = []

    def getOutputSql(self):
        ''' output path for sql database'''
        return path.join(path.dirname(path.dirname(path.realpath(__file__))),
                 "data",
                 "fundamental.sqlite")

    def getOptions(self):
        ''' crawling data and save to hbase '''
        parser = optparse.OptionParser("Usage: %prog [options]")
        parser.add_option("-f", "--symbolFile", dest = "symbolFile", type = "string",
                          help = "file that contains symbols for each line")
        parser.add_option("-o", "--outputDAM", dest = "outputDAM",
                          default = 'sql', type = "string",
                          help = "output dam, e.g. sql|hbase")

        (options, _) = parser.parse_args()

        # get symbols
        if options.symbolFile is None or not path.exists(options.symbolFile):
            print("Please provide valid file: %s" % options.symbolFile)
            exit(4)

        # get all symbols
        with open(options.symbolFile, 'r') as f:
            for line in f.readlines():
                self.symbols.append(line.strip())

        if not self.symbols:
            print("No symbols provided in file %s" % options.symbolFile)
            exit(4)

        # set output dam
        if options.outputDAM not in ["hbase", "sql"]:
            print("Please provide valid outputDAM %s" % options.outputDAM)
            exit(4)

        if 'sql' == options.outputDAM:
            sqlLocation = 'sqlite:///%s' % self.getOutputSql()
            print("Sqlite location: %s" % sqlLocation)
            setting = {'db': sqlLocation}


        # set google and output dam
        self.googleDAM = DAMFactory.createDAM("google")
        self.outputDAM = DAMFactory.createDAM(options.outputDAM, setting)

    def __getSaveOneSymbol(self, symbol):
        ''' get and save data for one symbol '''
        try:
            with self.readLock: #dam is not thread safe
                failCount = 0
                #try several times since it may fail
                while failCount < MAX_TRY:
                    try:
                        self.googleDAM.setSymbol(symbol)
                        keyTimeValueDict = self.googleDAM.readFundamental()

                    except BaseException as excp:
                        failCount += 1
                    else:
                        break

                if failCount >= MAX_TRY:
                    raise BaseException("Can't retrive historical data")

            with self.writeLock: #dam is not thread safe
                self.outputDAM.setSymbol(symbol)
                self.outputDAM.writeFundamental(keyTimeValueDict)

        except BaseException as excp:
            print("Error while processing %s: %s" % (symbol, excp))
            self.failed.append(symbol)
        else:
            print("Processed %s" % symbol)
            self.succeeded.append(symbol)

    def getSaveSymbols(self):
        ''' get and save data '''
        counter = 0
        rounds = 0

        while counter < len(self.symbols):
            size = len(self.symbols) - counter
            if BATCH_SIZE < size:
                size = BATCH_SIZE
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

    def printFailedSucceeded(self):
        ''' print out which ones fails'''
        print("Succeeded: %s" % self.succeeded)
        print("Failed: %s" % self.failed)

if __name__ == '__main__':
    crawler = FundamentalCrawler()
    crawler.getOptions()
    crawler.getSaveSymbols()
    crawler.printFailedSucceeded()

