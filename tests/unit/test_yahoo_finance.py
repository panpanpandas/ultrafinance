'''
Created on May 6, 2011

@author: ppa
'''
import unittest
from ultrafinance.dam.yahooFinance import YahooFinance

class testYahooFinance(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetHistoricalPrices(self):
        yahooFinance = YahooFinance()
        data = yahooFinance.getQuotes('^STI', '20110101', '20110110')
        self.assertNotEqual(0, len(data))