'''
Created on Nov 28, 2011

@author: ppa
'''
import unittest
from ultrafinance.dam.yahooDAM import YahooDAM

class testYahooDAM(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadQuotes(self):
        dam = YahooDAM()
        dam.setSymbol('^STI')
        data = dam.readQuotes('20110101', '20110110')
        print data
        self.assertNotEquals(len(data), 0)
