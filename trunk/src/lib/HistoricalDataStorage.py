'''
Created on Mar 20, 2011

@author: ppa
'''
from datetime import date
from xlwt import Workbook
from lib.YahooFinance import YahooFinance
import time

class HistoricalDataStorage():
    ''' class that store historical data from Yahoo finance '''
    def __init__(self, outputPrefix, startDate = '1900-01-01', endDate = date.today()):
        ''' constructor '''
        self.__outputPrefix = outputPrefix
        self.__startDate = startDate
        self.__endDate = endDate

    def buildExls(self, stocks, div=1):
        ''' get a list of stock data and store '''
        if div < 1:
            raise Exception("div need to be at least 1")

        for i in range(div):
            workbook = Workbook()
            for stock in stocks[i * len(stocks)/div: (i+1) * len(stocks)/div]:
                try:
                    self.__buildExl(stock, workbook)
                except:
                    pass
                time.sleep(2)

            workbook.save(self.__outputPrefix + str(i) + '.xls')

    def buildExlsFromFile(self, fileName, div=1):
        ''' read a file with stock names, get data and store'''
        f = open(fileName)
        lines = [line.rstrip() for line in f]
        print lines
        self.buildExls(lines, div)

    def __buildExl(self, stock, workbook):
        ''' get one stock historical data and store it '''
        ws = workbook.add_sheet(stock)

        #get data
        yahooFinance = YahooFinance()
        allData = yahooFinance.get_historical_prices(stock, self.__startDate, self.__endDate)
        for col, field in enumerate(['date', 'open', 'high', 'low', 'close', 'volume', 'adjClose']):
            ws.write(0, col, field)

        for row, data in enumerate(allData):
            for col, field in enumerate(['date', 'open', 'high', 'low', 'close', 'volume', 'adjClose']):
                ws.write(row+1, col, getattr(data, field) )

        print stock + 'saved'

if __name__ == "__main__":
    '''
    storage = HistoricalDataStorage('../../dataSource/SPY/SPY')
    storage.buildExlsFromFile('../../dataSource/SPY/SPY500.list', 5)
    '''
    storage = HistoricalDataStorage('../../dataSource/SPY/SPYINDEX')
    storage.buildExls(['SPY'], 1)