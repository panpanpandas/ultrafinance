'''
Created on Mar 20, 2011

@author: ppa
'''
from datetime import date
from xlwt import Workbook
import time

from lib.errors import ufException, Errors
from lib.yahooFinance import YahooFinance

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
        LOG.debug("buildExls %s, div %s" % (stocks, div))

        if div < 1:
            raise ufException(Errors.INDEX_RANGE_ERROR, "div need to be at least 1, %s are given" % div)

        for i in range(div):
            workbook = Workbook()
            for stock in stocks[i * len(stocks)/div: (i+1) * len(stocks)/div]:
                try:
                    self.__buildExl(stock, workbook)
                except:
                    LOG.debug("failed buildExl for stock %s" % stock)

                #sleep for 2 seconds, or Yahoo server will throw exception
                time.sleep(2)

            workbook.save(self.__outputPrefix + str(i) + '.xls')

    def buildExlsFromFile(self, fileName, div=1):
        ''' read a file with stock names, get data and store'''
        LOG.debug("buildExlsFromFile %s, div %s" % (fileName, div))

        f = open(fileName)
        lines = [line.rstrip() for line in f]
        self.buildExls(lines, div)

    def __buildExl(self, stock, workbook):
        ''' get one stock historical data and store it '''
        try:
            ws = workbook.add_sheet(stock)

            #get data
            yahooFinance = YahooFinance()
            allData = yahooFinance.get_historical_prices(stock, self.__startDate, self.__endDate)
            for col, field in enumerate(['date', 'open', 'high', 'low', 'close', 'volume', 'adjClose']):
                ws.write(0, col, field)

            for row, data in enumerate(allData):
                for col, field in enumerate(['date', 'open', 'high', 'low', 'close', 'volume', 'adjClose']):
                    ws.write(row+1, col, getattr(data, field) )

            LOG.debug(stock + 'saved')
        except ufException as excep:
            raise excep
        except BaseException as excep:
            raise ufException(Errors.UNKNOWN_ERROR, "historicalStorage.__buildExl got unknown error  %s" % excep)