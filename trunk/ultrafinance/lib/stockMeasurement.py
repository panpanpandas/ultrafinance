'''
Created on Jan 3, 2011

@author: ppa
'''
from scipy import polyfit
import copy
import numpy

from lib.yahooFinance import YahooFinance
from lib.errors import ufException, Errors

import logging
LOG = logging.getLogger(__name__)

class StockMeasurement():
    ''' measurement of a single stock/index '''
    def __init__(self, dateValues, benchmark='^GSPC', benchmarkValues=None):
        ''' constructor '''
        self.__dateValues = dateValues
        self.__benchmark = benchmark
        self.__benchmarkValues = copy.deepcopy(benchmarkValues)
        self.__alpha = None
        self.__beta = None
        self.__regressioned = False

    def mean(self):
        ''' get average '''
        return numpy.mean([float(dateValues.close) for dateValues in self.__dateValues], axis=0)

    def std(self):
        ''' get standard deviation '''
        return numpy.std([float(dateValues.close) for dateValues in self.__dateValues], axis=0)

    def linearRegression(self):
        if self.__regressioned:
            return

        if not self.__benchmarkValues:
            self.__benchmarkValues = YahooFinance().get_historical_prices(self.__benchmark, self.__dateValues[0].date, self.__dateValues[-1].date)

        tradeSuspended = False
        if 0 in map(lambda x: float(x.adjClose), self.__dateValues):
            tradeSuspended = True

        #filter out date tha't not in both stock and benchmark
        dateSet = set([dateValue.date for dateValue in self.__dateValues]) & set([dateValue.date for dateValue in self.__benchmarkValues])
        self.__dateValues = filter(lambda dateValue: dateValue.date in dateSet, self.__dateValues)
        self.__benchmarkValues = filter(lambda dateValue: dateValue.date in dateSet, self.__benchmarkValues)

        if len(self.__dateValues) <= 1 or tradeSuspended:
            msg = "Not enought dateValues" if len(self.__dateValues) <= 1 else "trade suspended"
            LOG.debug(msg)

            self.__beta = 0
            self.__alpha = 0
            self.__regressioned = True
            return

        try:
            x = [float(self.__benchmarkValues[index + 1].adjClose)/float(self.__benchmarkValues[index].adjClose) for index in range(len(self.__benchmarkValues) - 1)]
            y = [float(self.__dateValues[index + 1].adjClose)/float(self.__dateValues[index].adjClose) for index in range(len(self.__dateValues) - 1)]
            (self.__beta, self.__alpha) = polyfit(x, y, 1)
            self.__regressioned = True
        except BaseException as excep:
            raise ufException(Errors.UNKNOWN_ERROR, "stockMeasurement.linearRegression got unknown error %s" % excep)

    def marketReturnRate(self):
        if not self.__regressioned:
            self.linearRegression()
        return (float(self.__benchmarkValues[-1].adjClose) - float(self.__benchmarkValues[0].adjClose)) / float(self.__benchmarkValues[0].adjClose) \
                if self.__benchmarkValues and float(self.__benchmarkValues[0].adjClose) \
                else 0

    def returnRate(self):
        return (float(self.__dateValues[-1].adjClose) - float(self.__dateValues[0].adjClose)) / float(self.__dateValues[0].adjClose) \
                if self.__dateValues and float(self.__dateValues[0].adjClose) \
                else 0

    def relativeReturnRate(self):
        return self.returnRate() - self.marketReturnRate()

    def alpha(self):
        if not self.__regressioned:
            self.linearRegression()
        return self.__alpha

    def beta(self):
        if not self.__regressioned:
            self.linearRegression()
        return self.__beta