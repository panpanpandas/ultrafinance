'''
Created on May 6, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.lib.plotDateValueDict import PlotDateValueDict
from ultrafinance.lib.dataType import DateValueType

class testPlotDateValueDict(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPlotOneDateValue(self):
        stock1 = [DateValueType('2010-11-01', 1), DateValueType('2010-11-02', 2), DateValueType('2010-11-03', 3)]
        stock2 = [DateValueType('2010-11-01', 3), DateValueType('2010-11-02', 2), DateValueType('2010-11-03', 1)]
        stock3 = [DateValueType('2010-11-01', 1), DateValueType('2010-11-02', 2), DateValueType('2010-11-03', 3)]
        stock4 = [DateValueType('2010-11-01', 3), DateValueType('2010-11-02', 2), DateValueType('2010-11-03', 1)]
        dateValues = {'testStock1': stock1, 'testStock2': stock2, 'testStock3': stock3, 'testStock4': stock4}
        p = PlotDateValueDict(dateValues, '%Y-%m-%d')
        p.plot()