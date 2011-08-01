'''
Created on July 30, 2011

@author: ppa
'''
import unittest
from ultrafinance.lib.googleFinance import GoogleFinance
from ultrafinance.lib.errors import ufException

import logging
LOG = logging.getLogger(__name__)

class testGoogleFinance(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetHistoricalPrices(self):
        googleFinance = GoogleFinance()
        data = googleFinance.getHistoricalPrices('NASDAQ:EBAY', '20110101', '20110110')
        assert len(data)

    def testGetAll(self):
        googleFinance = GoogleFinance()
        data = googleFinance.getAll('NASDAQ:EBAY')
        assert len(data)

    def testGetAll_badSymbol(self):
        googleFinance = GoogleFinance()
        self.assertRaises(ufException, googleFinance.getAll, 'fasfdsdfasf')

    def testGetHistoricalPrices_badSymbol(self):
        googleFinance = GoogleFinance()
        self.assertRaises(ufException, googleFinance.getHistoricalPrices, *['AFSDFASDFASDFS', '20110101', '20110110'])