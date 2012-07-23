'''
Created on Jan 08, 2012

@author: ppa
'''
import unittest
from ultrafinance.backTest.account import Account
from ultrafinance.model import Order, Side, Quote

class testAccount(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetCash(self):
        account = Account(1000, 1)
        self.assertEquals(1000, account.cash)

    def testGetHoldingCost(self):
        share = 10
        price = 9.1
        account = Account(1000, 1)
        account._Account__holdings = {'stock1': (share, price)}
        print(account.holdings)

        holdingCost = account.getHoldingCost()
        print(holdingCost)

        self.assertAlmostEquals(share * price, holdingCost)

    def testGetHoldingValue(self):
        share = 10
        price = 9.1
        curPrice = 10.1
        account = Account(1000, 1)
        account._Account__holdings = {'stock1': (share, price)}
        account.setLastTickDict({'stock1': Quote(0, 0, 0, 0, curPrice, 0, 0)})

        holdingValue = account.getHoldingValue()
        print(holdingValue)
        self.assertAlmostEqual(share * curPrice, holdingValue)

    def testTotalValue(self):
        share = 10
        price = 9.1
        curPrice = 10.1
        account = Account(1000, 1)
        account._Account__holdings = {'stock1': (share, price)}
        account.setLastTickDict({'stock1': Quote(0, 0, 0, 0, curPrice, 0, 0)})

        totalValue = account.getTotalValue()
        print(totalValue)
        self.assertAlmostEquals(1000 + share * curPrice, totalValue)

    def testValidate(self):
        share = 10
        price = 9.1
        symbol = 'stock1'
        account = Account(1000, 1)
        account._Account__holdings = {symbol: (share, price)}

        # can't buy because price too high
        order1 = Order(accountId = 'id1', side = Side.BUY, symbol = symbol, price = 10000, share = 100000)
        self.assertEquals(False, account.validate(order1) )

        # can't buy because of commission fee
        order1 = Order(accountId = 'id1', side = Side.BUY, symbol = symbol, price = 100, share = 10)
        self.assertEquals(False, account.validate(order1) )

        # buy it
        order1 = Order(accountId = 'id1', side = Side.BUY, symbol = symbol, price = 100, share = 9)
        self.assertEquals(True, account.validate(order1) )

        # can't sell because don't have the stock
        order1 = Order(accountId = 'id1', side = Side.SELL, symbol = 'fas89ph2', price = 100, share = 9)
        self.assertEquals(False, account.validate(order1) )

        # can't sell because don't have the enough share
        order1 = Order(accountId = 'id1', side = Side.SELL, symbol = symbol, price = 100, share = 9000)
        self.assertEquals(False, account.validate(order1) )

        # sell it
        order1 = Order(accountId = 'id1', side = Side.SELL, symbol = symbol, price = 100, share = 9)
        self.assertEquals(True, account.validate(order1) )

