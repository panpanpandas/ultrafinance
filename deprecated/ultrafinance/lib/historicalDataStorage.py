'''
Created on Mar 20, 2011

@author: ppa
'''
from datetime import date
from xlwt import Workbook
import time
import traceback

from ultrafinance.lib.errors import UfException, Errors
from ultrafinance.lib.yahooFinance import YahooFinance

import logging
LOG = logging.getLogger(__name__)

class HistoricalDataStorage():
    ''' class that store historical data from Yahoo finance '''
    def __init__(self, outputPrefix, startDate = '1900-01-01', endDate = date.today()):
        ''' constructor '''
        self.__outputPrefix = outputPrefix
        self.__startDate = startDate
        self.__endDate = endDate

    def buildExls(self, stocks, div=1):
        ''' get a list of stock data and store '''
        print "BuildExls %s, div %s" % (stocks, div)

        if div < 1:
            raise UfException(Errors.INDEX_RANGE_ERROR, "div need to be at least 1, %s are given" % div)

        for i in range(div):
            workbook = Workbook()
            stocksToProcess = stocks[i * len(stocks)/div: (i+1) * len(stocks)/div]
            for stock in stocksToProcess:
                try:
                    self.__buildExl(stock, workbook)
                except Exception:
                    print "failed buildExl for stock %s: %s" % (stock, traceback.print_exc())

                #sleep for 2 seconds, or Yahoo server will throw exception
                time.sleep(2)

            fileName = '%s%d.xls' % (self.__outputPrefix, i)
            print "Saved %s to %s" % (stocksToProcess, fileName)
            workbook.save(fileName)

    def buildExlsFromFile(self, fileName, div=1):
        ''' read a file with stock names, get data and store'''
        print "buildExlsFromFile %s, div %s" % (fileName, div)

        f = open(fileName)
        lines = [line.rstrip() for line in f]
        self.buildExls(lines, div)

    def __buildExl(self, stock, workbook):
        ''' get one stock historical data and store it '''
        try:
            ws = workbook.add_sheet(stock)

            #get data
            yahooFinance = YahooFinance()
            allData = yahooFinance.getHistoricalPrices(stock, self.__startDate, self.__endDate)
            for col, field in enumerate(['date', 'open', 'high', 'low', 'close', 'volume', 'adjClose']):
                ws.write(0, col, field)

            for row, data in enumerate(allData):
                for col, field in enumerate(['date', 'open', 'high', 'low', 'close', 'volume', 'adjClose']):
                    ws.write(row+1, col, getattr(data, field) )

        except UfException as excp:
            raise excp
        except Exception:
            raise UfException(Errors.UNKNOWN_ERROR, "historicalStorage.__buildExl got unknown error  %s"
                              % traceback.print_exc())