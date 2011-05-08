'''
Created on May 6, 2011

@author: ppa
'''
import unittest

import os
from lib.stockMeasurement import StockMeasurement
from lib.dataType import StockDailyType

import logging
LOG = logging.getLogger(__name__)

class testStockMeasurement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMeasurement(self):
        dateValues = [StockDailyType('2011-01-03', '3190.04', '3239.03', '3190.04', '3235.77', '000', '3235.7'),
                      StockDailyType('2011-01-04', '3235.77', '3260.08', '3235.77', '3250.29', '000', '3250.2'),
                      StockDailyType('2011-01-05', '3250.29', '3263.05', '3242.98', '3254.25', '000', '3254.2'),
                      StockDailyType('2011-01-06', '3254.25', '3280.43', '3254.25', '3279.70', '000', '3279.7'),
                      StockDailyType('2011-01-07', '3279.70', '3280.77', '3253.14', '3261.35', '000', '3261.3'),
                      StockDailyType('2011-01-10', '3261.35', '3270.21', '3229.27', '3229.27', '000', '3229.2')]
        stockMeasurement = StockMeasurement(dateValues, '^GSPC')
        stockMeasurement.linearRegression()
        print stockMeasurement.alpha()
        assert stockMeasurement.alpha()
        assert stockMeasurement.beta()
        assert stockMeasurement.mean()
        assert stockMeasurement.std()
        assert stockMeasurement.relativeReturnRate()
        assert stockMeasurement.marketReturnRate()
        assert stockMeasurement.returnRate()