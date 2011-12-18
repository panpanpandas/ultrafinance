'''
Created on Dec 18, 2011

@author: ppa
'''
import unittest
from ultrafinance.pyTaLib import *

class testPyTaLib(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSma(self):
        sma = Sma(period = 3)
        expectedAvgs = [1, 1.5, 2, 3, 4]
        for index, number in enumerate(range(1, 6) ):
            self.assertEquals(expectedAvgs[index], sma(number))
