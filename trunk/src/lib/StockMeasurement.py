'''
Created on Jan 3, 2011

@author: ppa
'''
from scipy import polyfit
from lib.YahooFinance import YahooFinance
import numpy

class StockMeasurement():
    ''' measurement of a single stock/index '''
    def __init__(self, dateValues):
        ''' constructor '''
        self.__dateValues = dateValues
        self.__benchmarkValues = None
        self.__alpha = None
        self.__beta = None
        
    def mean(self):
        ''' get average '''
        return numpy.mean([float(dateValues.close) for dateValues in self.__dateValues], axis=0)
        
    def std(self):
        ''' get standard deviation '''
        return numpy.std([float(dateValues.close) for dateValues in self.__dateValues], axis=0)
    
    def linearRegression(self, benchmark='^GSPC'):
        self.__benchmarkValues = YahooFinance().get_historical_prices(benchmark, self.__dateValues[0].date, self.__dateValues[-1].date)
        if len(self.__benchmarkValues) == len(self.__dateValues):
            x = [float(self.__benchmarkValues[index + 1].adjClose)/float(self.__benchmarkValues[index].adjClose) for index in range(len(self.__benchmarkValues) - 1)]
            y = [float(self.__dateValues[index + 1].adjClose)/float(self.__dateValues[index].adjClose) for index in range(len(self.__benchmarkValues) - 1)]
            (self.__beta, self.__alpha) = polyfit(x, y, 1)
        else:
            print 'benchmark %s don\'t have enough data' % benchmark
 
    def alpha(self):
        if not self.__benchmarkValues:
            self.linearRegression()
        return self.__alpha

    def beta(self):
        if not self.__benchmarkValues:
            self.linearRegression()
        return self.__beta