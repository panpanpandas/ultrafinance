'''
Created on Jan 3, 2011

@author: ppa
'''
from scipy import polyval, polyfit
from lib.YahooFinance import YahooFinance
from operator import itemgetter
import numpy

class StockMeasurement():
    ''' measurement of a single stock/index '''
    def __init__(self, dateValues):
        ''' constructor '''
        print dateValues
        self.__dates = [dateValue[0] for dateValue in dateValues]
        self.__values = [dateValue[1] for dateValue in dateValues]
        self.__benchmarkValues = None
        self.__alpha = None
        self.__beta = None
        
    def mean(self):
        ''' get average '''
        return numpy.mean([float(value[0]) for value in self.__values], axis=0)
        
    def std(self):
        ''' get standard deviation '''
        return numpy.std([float(value[0]) for value in self.__values], axis=0)
    
    def linearRegression(self, benchmark='SPY'):
        print "hello %s" %self.__dates[0]
        dateValues = YahooFinance().get_dates_values(benchmark, self.__dates[0], self.__dates[-1])
        if len(dateValues) == len(self.__dates):
            self.__benchmarkValues = [dateValue[1] for dateValue in dateValues]
            
            x = [float(self.__benchmarkValues[index + 1][1])/float(self.__benchmarkValues[index + 1][0]) for index in range(len(dateValues) - 1)]
            y = [float(self.__values[index + 1][1])/float(self.__values[index + 1][0]) for index in range(len(dateValues) - 1)]
            (self.__alpha, self.__beta) = polyfit(x, y, 1)
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