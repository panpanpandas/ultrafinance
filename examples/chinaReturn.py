'''
Created on Apr 24, 2011

@author: ppa
'''
from operator import itemgetter
import time
import os

from ultrafinance.lib.stockMeasurement import StockMeasurement
from ultrafinance.lib.historicalDataStorage import HistoricalDataStorage
from ultrafinance.lib.yahooFinance import YahooFinance
from ultrafinance.lib.dataType import StockDailyType
from ultrafinance.lib.excelLib import ExcelLib

import logging
LOG = logging.getLogger(__name__)

benchmarks = {'DEFAULT': '^GSPC',
              'L': '^STI',
              'HK': '^HSI',
              'SI': '^FTSE'}
benchmarkValues = {}

def buildBenchmarkValues():
    print "Building BenchmarkValues"
    for key in benchmarks.values():
        benchmarkValues[key] = YahooFinance().getHistoricalPrices(key, '19010101', '20130101')
        time.sleep(1)

    print "BenchmarkValues %s built" % benchmarkValues.keys()

class ChinaReturn():
    def __init__(self, fullTest=False):
        ''' constructor '''
        #folder path ../dataSource/CHINA'
        self.__workingDir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     'dataSource',
                                     'CHINA')
        self.dayIntervals = [1, 3, 30, 90, 250, 500, 750]
        if fullTest:
            self.__stocklistFile = os.path.join(self.__workingDir, 'china544.list')
        else:
            self.__stocklistFile = os.path.join(self.__workingDir, 'china10.list')

    def saveHistroyDataIntoExcel(self):
        ''' read stock list, get historical data, and save to excel '''
        print 'Save HistroyData Into Excel'
        storage = HistoricalDataStorage(os.path.join(self.__workingDir, 'china') )
        storage.buildExlsFromFile(fileName=self.__stocklistFile, div=5)

    def analyze(self):
        ''' analyze '''
        print 'Start analyzing'
        buildBenchmarkValues()

        returnRates = [[], [], [], [], [], [], []]
        alphas = [[], [], [], [], [], [], []]
        relativeReturnRates = [[], [], [], [], [], [], []]

        for fileName in filter( lambda f: f.endswith('.xls'), os.listdir(self.__workingDir) ):
            excelFile = os.path.join(self.__workingDir, fileName)
            sheetNames = ExcelLib.getSheetNames(excelFile)

            for sheetName in sheetNames:
                with ExcelLib(excelFile) as excel:
                    excel.openSheet(sheetName=sheetName)

                    contry = sheetName.split('.')[-1] if len( sheetName.split('.') ) != 1 else 'DEFAULT'
                    benchmark = benchmarks[contry]
                    print 'Processing %s with benchmark %s' % (sheetName, benchmark)

                    for index, duration in enumerate(self.dayIntervals):
                        data = []
                        broke = False
                        for i in range(1, duration + 1):
                            #print "row %d, duration %d" % (i, duration)
                            if broke:
                                break

                            try:
                                values = excel.readRow(i)
                                for j in range( len(values) ):
                                    values[j] = float(values[j]) if j != 0 else values[j]

                                data.append( StockDailyType( *values ) )
                            except Exception:
                                print 'Analyzing %s break at %d' % (sheetName, i)
                                broke = True
                                break
                        if data:
                            dateValues = sorted(data, key=itemgetter(0))

                            #print benchmarkValues[benchmark]
                            stockMeasurement = StockMeasurement(dateValues, benchmark, benchmarkValues[benchmark])
                            stockMeasurement.linearRegression()
                            returnRates[index].append( stockMeasurement.returnRate() )
                            alphas[index].append( stockMeasurement.alpha() )
                            relativeReturnRates[index].append( stockMeasurement.relativeReturnRate() )

        with open(os.path.join(self.__workingDir, 'output.txt'), 'w') as outputFile:
            outputReturnRates = map(lambda x: sum(x)/len(x), returnRates)
            outputAlphas = map(lambda x: sum(x)/len(x), alphas)
            outputRelativeReturnRates = map(lambda x: sum(x)/len(x), relativeReturnRates)
            print "Days since going public %s" % self.dayIntervals
            print "returnRates: %s" % outputReturnRates
            print "alphas: %s" % outputAlphas
            print "relativeReturnRates: %s" % outputRelativeReturnRates
            outputFile.write("outputReturnRates %s\n" % outputReturnRates)
            outputFile.write("outputAlphas %s\n" % outputAlphas)
            outputFile.write("outputRelativeReturnRates %s\n" % outputRelativeReturnRates)
            outputFile.write("returnRates %s\n" % returnRates)
            outputFile.write("alphas %s\n" % alphas)
            outputFile.write("relativeReturnRates %s\n" % relativeReturnRates)

if __name__ == '__main__':
    app = ChinaReturn()
    app.saveHistroyDataIntoExcel()
    app.analyze()