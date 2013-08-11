'''
Created on Dec 4, 2011

@author: ppa
'''
from ultrafinance.module.googleCrawler import GoogleCrawler

from os import path
import datetime
from dateutil.relativedelta import relativedelta
import optparse

BATCH_SIZE = 30
THREAD_TIMEOUT = 5
MAX_TRY = 3

class StockCrawler(object):
    ''' collect quotes/ticks for a list of symbol '''
    def __init__(self):
        ''' constructor '''
        self.symbols = []
        self.start = None

    def getOptions(self):
        ''' crawling data and save to hbase '''
        parser = optparse.OptionParser("Usage: %prog [options]")
        parser.add_option("-f", "--symbolFile", dest = "symbolFile", type = "string",
                          help = "file that contains symbols for each line")
        parser.add_option("-s", "--start", dest = "start",
                          default = 'month', type = "string",
                          help = "start date, all|month")

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

        if options.start not in ['all', 'month']:
            print("Please provide valid start option(all|month): %s" % options.outputDAM)
            exit(4)

        # set start date and end date
        if 'all' == options.start:
            self.start = '19800101'
        else:
            self.start = (datetime.datetime.now() + relativedelta(months = -1)).strftime("%Y%m%d")
        self.end = datetime.datetime.now().strftime("%Y%m%d")
        print("Retrieving quotes start from %s" % self.start)

    def retrieveQuotes(self):
        ''' retrieve quotes '''
        googleCrawler = GoogleCrawler(self.symbols, self.start)
        googleCrawler.getAndSaveSymbols()
        print("Sqlite location: %s" % googleCrawler.sqlLocation)
        print("Succeeded: %s" % googleCrawler.succeeded)
        print("Failed: %s" % googleCrawler.failed)

if __name__ == '__main__':
    crawler = StockCrawler()
    crawler.getOptions()
    crawler.retrieveQuotes()
