'''
Created on Dec 4, 2011

@author: ppa
'''

from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.dam.DAMFactory import DAMFactory

from os import path
import datetime
import optparse

class SymbolCrawler(object):
    ''' collect quotes/ticks for a list of symbol '''
    def __init__(self):
        ''' constructor '''
        self.symbols = []
        self.hbaseDAM = None
        self.googleDAM = None
        self.isQuote = False
        self.isTick = False
        self.start = None
        self.end = None
        self.failed = []
        self.succeeded = []

    def getOptions(self):
        ''' crawling data and save to hbase '''
        parser = optparse.OptionParser("Usage: %prog [options]")
        parser.add_option("-f", "--symbolFile", dest = "symbolFile", type = "string",
                          help = "file that contains symbols for each line")
        parser.add_option("-t", "--dataType", dest = "dataType",
                          default = 'tick', type = "string",
                          help = "data type that will be stored, e.g. quote|tick|all")
        parser.add_option("-s", "--start", dest = "start",
                          default = '19800101', type = "string",
                          help = "start date")
        parser.add_option("-e", "--end", dest = "end",
                          default = datetime.datetime.now().strftime("%Y%m%d"), type = "string",
                          help = "end date")


        (options, args) = parser.parse_args()

        # get symbols
        if options.symbolFile is None or not path.exists(options.symbolFile):
            print "Please provide valid file: %s" % options.symbolFile
            exit(4)

        # get all symbols
        with open(options.symbolFile, 'r') as f:
            for line in f.readlines():
                self.symbols.append(line.strip())

        if not self.symbols:
            print "No symbols provided in file %s" % options.symbolFile
            exit(4)

        # set dataType
        if options.dataType not in ["quote", "tick", "all"]:
            print "Please provide valide dataType %s" % options.dataType
            exit(4)

        if "quote" == options.dataType:
            self.isQuote = True
        elif "tick" == options.dataType:
            self.isTick = True
        else:
            self.isQuote = self.isTick = True

        # set google and hbase dam
        self.googleDAM = DAMFactory.createDAM("google")
        self.hbaseDAM = DAMFactory.createDAM("hbase")

        # set start date and end date
        self.start = options.start
        self.end = options.end

    def __getSaveOneSymbol(self, symbol):
        ''' get and save data for one symbol '''
        try:
            self.googleDAM.setSymbol(symbol)
            self.hbaseDAM.setSymbol(symbol)

            if self.isQuote:
                quotes = self.googleDAM.readQuotes(self.start, self.end)
                self.hbaseDAM.writeQuotes(quotes)

            if self.isTick:
                ticks = self.googleDAM.readTicks(self.start, self.end)
                self.hbaseDAM.writeTicks(ticks)
        except BaseException as excp:
            print "Error while processing %s: %s" % (symbol, excp)
            self.failed.append(symbol)
        else:
            print "Processed %s" % symbol
            self.succeeded.append(symbol)

    def getSaveSymbols(self):
        ''' get and save data '''
        for symbol in self.symbols:
            self.__getSaveOneSymbol(symbol)

    def printFailedSucceeded(self):
        ''' print out which ones fails'''
        print "Succeeded: %s" % self.succeeded
        print "Failed: %s" % self.failed

if __name__ == '__main__':
    crawler = SymbolCrawler()
    crawler.getOptions()
    crawler.getSaveSymbols()
    crawler.printFailedSucceeded()

