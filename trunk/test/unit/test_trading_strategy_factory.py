'''
Created on May 6, 2011

@author: ppa
'''
import unittest
from lib.tradingStrategyFactory import *

from lib.dataType import DateValueType
import logging
LOG = logging.getLogger(__name__)

class testTradingStrategyFatory(unittest.TestCase):

    def setUp(self):
        self.data = [DateValueType(1, 10.0), DateValueType(2, 20.0), DateValueType(3, 25.0), DateValueType(4, 50.0)]

    def tearDown(self):
        pass

    def testFixAmountPerPeriod(self):
        tradingStrategyFactory = TradingStrategyFactory(fixAmountPerPeriod)
        assert tradingStrategyFactory.calculateReturn(self.data, 1)

    def testFixAmountPerPeriodWithAddtionWhenDrop(self):
        data = [DateValueType(1, 10.0), DateValueType(2, 20.0), DateValueType(3, 25.0), DateValueType(4, 50.0)]
        tradingStrategyFactory = TradingStrategyFactory(fixAmountPerPeriodWithAddtionWhenDrop)
        assert tradingStrategyFactory.calculateReturn(data, 1, 2)

    def testAdjustFixAmountPerPeriod(self):
        tradingStrategyFactory = TradingStrategyFactory(adjustFixAmountPerPeriod)
        assert tradingStrategyFactory.calculateReturn(self.data, 1, 2)