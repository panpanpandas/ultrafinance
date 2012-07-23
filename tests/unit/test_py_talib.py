'''
Created on Dec 18, 2011

@author: ppa
'''
import unittest
from ultrafinance.pyTaLib.indicator import Sma

class testPyTaLib(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSma(self):
        sma = Sma(period = 3)
        expectedAvgs = [1, 1.5, 2, 3, 4]
        for index, number in enumerate(range(1, 6) ):
            self.assertEqual(expectedAvgs[index], sma(number))
