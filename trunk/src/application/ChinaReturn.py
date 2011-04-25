'''
Created on Apr 24, 2011

@author: ppa
'''
from lib.StockMeasurement import StockMeasurement
from lib.DataType import StockDailyType
from lib.excelLib import ExcelLib
from operator import itemgetter
import time
import os

benchmarks = {'DEFAULT': '^GSPC',
              'L': '^STI',
              'HK': '^HSI',
              'SI': '^FTSE'}

class ChinaReturn():
    def __init__(self):
        self.excelPath = '../../dataSource/CHINA'

    def run(self):
        returnRate = [0, 0, 0, 0, 0, 0, 0]
        count = 0

        for fileName in filter( lambda f: f.endswith('.xls'), os.listdir(self.excelPath) ):
            excelFile = os.path.join(self.excelPath, fileName)
            sheetNames = ExcelLib.getSheetNames( excelFile )
            print sheetNames

            for sheetName in sheetNames:
                print 'processing %s' % sheetName
                with ExcelLib(excelFile, sheetName=sheetName) as excel:
                    contry = sheetName.split('.')[-1] if len( sheetName.split('.') ) != 1 else 'DEFAULT'
                    benchmark = benchmarks[contry]

                    for index, duration in enumerate([1, 3, 30, 90, 250, 500, 750]):
                        data = []
                        for i in range(0 - duration, 0):
                            values = excel.readRow(i)
                            if values:
                                for j in range( len(values) ):
                                    values[j] = float(values[j]) if j != 0 else values[j]

                                data.append( StockDailyType( *values ) )
                            else:
                                print 'break at %d' % i
                                break
                        if data:
                            dateValues = sorted(data, key=itemgetter(0))

                            stockMeasurement = StockMeasurement(dateValues, benchmark)
                            returnRate[index] += stockMeasurement.returnRate()

                    count += 1
                    time.sleep(1)

        print "result: %s" % returnRate

if __name__ == '__main__':
    app = ChinaReturn()
    app.run()