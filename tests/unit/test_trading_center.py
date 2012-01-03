'''
Created on Dec 18, 2011

@author: ppa
'''
import unittest
from ultrafinance.backTest.tradingCenter import TradingCenter

class testTradingCenter(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetAccounts(self):
        tradingCenter = TradingCenter()
        tradingCenter.createAccount(100000, 0)
        tradingCenter.createAccount(200000, 0)
        accounts = tradingCenter.getAccounts('.*')
        print accounts
        self.assertEquals(2, len(accounts))