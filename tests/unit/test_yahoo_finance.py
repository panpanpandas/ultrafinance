'''
Created on May 6, 2011

@author: ppa
'''
import unittest
from ultrafinance.lib.yahooFinance import YahooFinance

import logging
LOG = logging.getLogger(__name__)

class testYahooFinance(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetHistoricalPrices(self):
        yahooFinance = YahooFinance()
        data = yahooFinance.getHistoricalPrices('^STI', '20110101', '20110110')
        assert len(data)