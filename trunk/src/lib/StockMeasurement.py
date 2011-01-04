'''
Created on Jan 3, 2011

@author: ppa
'''
from scipy import stats
import numpy

class StockMeasurement():
    ''' measurement of a single stock/index '''
    def __init__(self, dateValues):
        ''' constructor '''
        self.dates = [dateValue[0] for dateValue in dateValues]
        self.values = [float(dateValue[1]) for dateValue in dateValues]
    
    def mean(self):
        ''' get average '''
        return numpy.mean(self.values, axis=0)
        
    def std(self):
        ''' get standard deviation '''
        return numpy.std(self.values, axis=0)