'''
Created on Aug 11, 2011

@author: ppa
'''
import os
import sys
from ultrafinance.lib.googleFinance import GoogleFinance

class StockPicker:
    ''' sort stocks '''
    def __init__(self):
        ''' constructor '''
        self.__workingDir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             'dataSource',
                             'SPY')
        self.__stockList = os.path.join(self.__workingDir, 'SPY500.list')
        self.__outputFile = os.path.join(self.__workingDir, 'SPY500.output')

    def getStockFinancials(self, fields, writeOutput=False):
        ''' get stock financials '''
        with open(self.__stockList) as inFile:
            stockFinancials = {}

            for stockName in inFile.readlines():
                try:
                    stockName = stockName.strip()
                    googleFinance = GoogleFinance()
                    financials = googleFinance.getFinancials(stockName, fields)
                    print "%s %s" % (stockName, financials)
                    stockFinancials[stockName] = financials
                except Exception as excp:
                    print '%s' % excp

            if writeOutput:
                with open(self.__outputFile, 'w') as outFile:
                    outFile.write(str(stockFinancials))

            return stockFinancials

        return {}

    def readStockFinancials(self):
        ''' read financials from file '''
        with open(self.__outputFile) as file:
            # dangerous to use eval
            return eval(file.read())

    def calDeceasingRate(self, value):
            try:
                firstIncRate = (float(value[0]) - float(value[1])) / float(value[1]) if float(value[1]) else 0
                secondIncRate = (float(value[1]) - float(value[2])) / float(value[2]) if float(value[2]) else 0
                thirdIncRate = (float(value[2]) - float(value[3])) / float(value[3]) if float(value[3]) else 0
                incRate = (firstIncRate + secondIncRate + thirdIncRate) / 3

                return incRate
            except:
                return 0 - sys.maxint

    def calAverage(self, value):
            try:
                return (float(value[0]) + float(value[1]) + float(value[2]) + float(value[3])) / 4
            except:
                return 0 - sys.maxint

    def sortStocks(self, stockFinancials, field, topNum=20):
        def sortByFieldDecreasing(stockFinancials):
            values = stockFinancials[1]
            value = values[field]
            if not value:
                return 0 - sys.maxint

#            return self.calDeceasingRate(value)
            return self.calAverage(value)

        ret = {}
        for name, values in sorted(stockFinancials.iteritems(), key=sortByFieldDecreasing, reverse=True)[0:topNum]:
            #ret[name] = (self.calDeceasingRate(values[field]), values[field])
            ret[name] = ('%.2f' % self.calAverage(values[field]), values[field])
            #ret[name] = '%.2f' % self.calAverage(values[field])

        return ret

if __name__ == '__main__':
    app = StockPicker()
    #app.getStockFinancials(['Total Revenue',
    #                        'Diluted Normalized EPS', 'Net Income', 'Gross Profit', 'Total Operating Expense', 'Income After Tax'],
    #                       True)
    stockFinancials = app.readStockFinancials()
    topNum = 20
    field1 = 'Total Revenue'
    field2 = 'Diluted Normalized EPS'
    print 'Top %d sorted by %s Increasing' % (topNum, field1)
    for key, value in app.sortStocks(stockFinancials, field1, topNum).items():
        print '||%s||%s||' % (key, value)
    print 'Top %d sorted by %s Increasing' % (topNum, field2)
    for key, value in app.sortStocks(stockFinancials, field2, topNum).items():
        print '||%s||%s||' % (key, value)