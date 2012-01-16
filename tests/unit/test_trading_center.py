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

    def testGetCopyAccounts(self):
        tradingCenter = TradingCenter()
        tradingCenter.createAccountWithMetrix(100000, 0)
        tradingCenter.createAccountWithMetrix(200000, 0)

        accounts = tradingCenter.getCopyAccounts('.*')
        print [str(account) for account in accounts]
        self.assertEquals(2, len(accounts))


    def testGetCopyAccount(self):
        tradingCenter = TradingCenter()
        accountId1 = tradingCenter.createAccountWithMetrix(100000, 0)

        account = tradingCenter.getCopyAccount(accountId1)
        print account
        self.assertEquals(100000, account.cash)
