'''
Created on July 30, 2011

@author: ppa
'''
import unittest
from ultrafinance.dam.googleFinance import GoogleFinance
from ultrafinance.lib.errors import UfException

import logging
LOG = logging.getLogger(__name__)

class testGoogleFinance(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetQuotes(self):
        googleFinance = GoogleFinance()
        data = googleFinance.getQuotes('NASDAQ:EBAY', '20131101', None)
        print [str(q) for q in data]
        assert len(data)

    def testGetAll(self):
        googleFinance = GoogleFinance()
        data = googleFinance.getAll('EBAY')
        print(data)
        self.assertNotEqual(0, len(data))

    def testGetAll_badSymbol(self):
        googleFinance = GoogleFinance()
        self.assertRaises(UfException, googleFinance.getAll, 'fasfdsdfasf')

    def testGetQuotes_badSymbol(self):
        googleFinance = GoogleFinance()
        self.assertRaises(UfException, googleFinance.getQuotes, *['AFSDFASDFASDFS', '20110101', '20110110'])

    def testGetFinancials(self):
        googleFinance = GoogleFinance()
        #ret = googleFinance.getFinancials('NASDAQ:EBAY', ['Net Income', 'Total Revenue', 'Diluted Normalized EPS', 'Total Common Shares Outstanding'], False)
        ret = googleFinance.getFinancials('NASDAQ:EBAY')
        print(ret)

    def testGetTicks(self):
        googleFinance = GoogleFinance()
        ret = googleFinance.getTicks('EBAY', start = '20110101', end = '20110110')
        print(ret)
