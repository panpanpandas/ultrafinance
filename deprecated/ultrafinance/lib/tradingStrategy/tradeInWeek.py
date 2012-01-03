'''
Created on Mar 27, 2011

@author: ppa
'''
from datetime import date
from operator import itemgetter
from ultrafinance.lib.excelLib import ExcelLib

import logging
LOG = logging.getLogger(__name__)

class TradeInWeek():
    '''
    trade in one week. Which day to buy and sell is best
    '''
    WEEKDAY = ['SUN.', 'MON.', 'TUE.', 'WED.', 'THU.', 'FRI.']
    def __init__(self, fileName, sheetNumber = 0):
        ''' Constructor '''
        self.returnRate = {}
        self.fileName = fileName
        self.sheetNumber = sheetNumber

    def tryAllStrategy(self):
        ''' preparing data'''
        for buyWeekDate in range(1, 6):
            for sellWeekDate in range(1, 6):
                self.returnRate[(TradeInWeek.WEEKDAY[buyWeekDate], TradeInWeek.WEEKDAY[sellWeekDate])] = \
                    '%.2f' % self.oneStrategy(buyWeekDate, sellWeekDate)

        return sorted(self.returnRate.items(), key=itemgetter(1))

    def oneStrategy(self, buyWeekDate, sellWeekDate):
        totalReturn = 0
        with ExcelLib(self.fileName, self.sheetNumber) as excel:
            stockDates = excel.readCol(0, 1, -1)
            open = excel.readCol(1, 1, -1)
            close = excel.readCol(4, 1, -1)

            for i, stockDate in enumerate([date(int(stockDate.split('-')[0]), int(stockDate.split('-')[1]), int(stockDate.split('-')[2]))
                                           for stockDate in stockDates]):
                if buyWeekDate == stockDate.isoweekday():
                    for holdDay in range(1, 5):
                        if i + holdDay < len(stockDates):
                            stockDate = stockDates[i + holdDay]
                            if sellWeekDate == date(int(stockDate.split('-')[0]), int(stockDate.split('-')[1]), int(stockDate.split('-')[2])).isoweekday():
                                #print float(close[i + holdDay]) -
                                totalReturn += float(close[i + holdDay])
                                totalReturn -= float(open[i])

            return totalReturn

if __name__ == '__main__':
    tradeInWeek = TradeInWeek('../../dataSource/SPY/SPYINDEX0.xls', 0)
    tradeInWeek.tryAllStrategy()
    print tradeInWeek.returnRate