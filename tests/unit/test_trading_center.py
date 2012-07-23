'''
Created on Dec 18, 2011

@author: ppa
'''
import unittest
from ultrafinance.backTest.tradingCenter import TradingCenter
from ultrafinance.model import Tick, Order, Side
from ultrafinance.backTest.account import Account
from ultrafinance.lib.errors import UfException
import mox

class testTradingCenter(unittest.TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        pass

    def testGetCopyAccounts(self):
        tc = TradingCenter()
        tc.createAccountWithMetrix(100000, 0)
        tc.createAccountWithMetrix(200000, 0)

        accounts = tc.getCopyAccounts('.*')
        print([str(account) for account in accounts])
        self.assertEquals(2, len(accounts))


    def testGetCopyAccount(self):
        tc = TradingCenter()
        accountId1 = tc.createAccountWithMetrix(100000, 0)

        account = tc.getCopyAccount(accountId1)
        print(account)
        self.assertEquals(100000, account.cash)

    def testIsOrderMet(self):
        tc = TradingCenter()
        tick1 = Tick('time', 'open', 'high', 'low', 13.20, 'volume')
        order1 = Order(accountId = None, side = Side.BUY, symbol = 'symbol', price = 13.25, share = 10)
        order2 = Order(accountId = None, side = Side.BUY, symbol = 'symbol', price = 13.15, share = 10)
        order3 = Order(accountId = None, side = Side.SELL, symbol = 'symbol', price = 13.25, share = 10)
        order4 = Order(accountId = None, side = Side.SELL, symbol = 'symbol', price = 13.15, share = 10)

        self.assertEquals(True, tc.isOrderMet(tick1, order1))
        self.assertEquals(False, tc.isOrderMet(tick1, order2))
        self.assertEquals(False, tc.isOrderMet(tick1, order3))
        self.assertEquals(True, tc.isOrderMet(tick1, order4))

    def testValidOrder(self):
        tc = TradingCenter()

        accountId = 'accountId'
        order1 = Order(accountId = accountId, side = Side.BUY, symbol = 'symbol', price = 13.25, share = 10)
        order2 = Order(accountId = 'unknowAccount', side = Side.BUY, symbol = 'symbol', price = 13.25, share = 10)
        account = self.mock.CreateMock(Account)
        account.validate(order1).AndReturn(True)
        account.validate(order1).AndReturn(False)
        tc._TradingCenter__accounts = {accountId: account}

        self.mock.ReplayAll()
        self.assertEquals(False, tc.validateOrder(order2) ) # invalid account id
        self.assertEquals(True, tc.validateOrder(order1) ) # True
        self.assertEquals(False, tc.validateOrder(order1) ) # False
        self.mock.VerifyAll()

    def testPlaceOrder_existedOrder(self):
        tc = TradingCenter()

        accountId = 'accountId'
        order1 = Order(accountId = accountId, side = Side.BUY, symbol = 'symbol', price = 13.25, share = 10, orderId = 'orderId1')
        self.assertRaises(UfException, tc.placeOrder, order1)

    def testPlaceOrder_invalidAccountId(self):
        tc = TradingCenter()

        order2 = Order(accountId = 'unknowAccount', side = Side.BUY, symbol = 'symbol', price = 13.25, share = 10)

        self.mock.ReplayAll()
        self.assertEquals(None, tc.placeOrder(order2) ) # invalid account id
        self.mock.VerifyAll()

    def testPlaceOrder_OK(self):
        tc = TradingCenter()

        accountId = 'accountId'
        order1 = Order(accountId = accountId, side = Side.BUY, symbol = 'symbol', price = 13.25, share = 10)
        account = self.mock.CreateMock(Account)
        account.validate(order1).AndReturn(True)
        tc._TradingCenter__accounts = {accountId: account}

        self.mock.ReplayAll()
        self.assertNotEquals(None, tc.placeOrder(order1) ) # True
        self.mock.VerifyAll()

    def testPlaceOrder_failed(self):
        tc = TradingCenter()

        accountId = 'accountId'
        order1 = Order(accountId = accountId, side = Side.BUY, symbol = 'symbol', price = 13.25, share = 10)
        account = self.mock.CreateMock(Account)
        account.validate(order1).AndReturn(False)
        tc._TradingCenter__accounts = {accountId: account}

        self.mock.ReplayAll()
        self.assertEquals(None, tc.placeOrder(order1) ) # True
        self.mock.VerifyAll()

    def testGetOpenOrdersByOrderId(self):
        order1 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.2, share = 10, orderId = 'id1')
        order2 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.25, share = 10, orderId = 'id2')

        tc = TradingCenter()
        tc._TradingCenter__openOrders = {'symbol1': [order1, order2]}
        order = tc.getOpenOrderByOrderId('id1')
        self.assertEquals(order1, order)

        order = tc.getOpenOrderByOrderId('id1sdfasdf')
        self.assertEquals(None, order)

    def testGetOpenOrdersBySymbol(self):
        order1 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.2, share = 10, orderId = 'id1')
        order2 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.25, share = 10, orderId = 'id2')

        tc = TradingCenter()
        tc._TradingCenter__openOrders = {'symbol1': [order1, order2]}
        orders = tc.getOpenOrdersBySymbol('symbol1')
        self.assertEquals([order1, order2], orders)

    def testCancelOrder(self):
        order1 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.2, share = 10, orderId = 'id1')
        order2 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.25, share = 10, orderId = 'id2')

        tc = TradingCenter()
        tc._TradingCenter__openOrders = {'symbol1': [order1, order2]}

        tc.cancelOrder('id1')
        print(tc._TradingCenter__openOrders)
        print(tc._TradingCenter__closedOrders)
        self.assertEquals({'symbol1': [order2]}, tc._TradingCenter__openOrders)
        self.assertEquals({'id1': order1}, tc._TradingCenter__closedOrders)
        self.assertEquals(Order.CANCELED, order1.status)

        tc.cancelOrder('id2')
        print(tc._TradingCenter__openOrders)
        print(tc._TradingCenter__closedOrders)
        self.assertEquals({}, tc._TradingCenter__openOrders)
        self.assertEquals({'id1': order1, 'id2': order2}, tc._TradingCenter__closedOrders)

    def testCancelAllOpenOrders(self):
        order1 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.2, share = 10, orderId = 'id1')
        order2 = Order(accountId = 'accountId', side = Side.BUY, symbol = 'symbol1', price = 13.25, share = 10, orderId = 'id2')

        tc = TradingCenter()
        tc._TradingCenter__openOrders = {'symbol1': [order1, order2]}

        tc.cancelAllOpenOrders()
        print(tc._TradingCenter__openOrders)
        print(tc._TradingCenter__closedOrders)
        self.assertEquals({}, tc._TradingCenter__openOrders)
        self.assertEquals({'id1': order1, 'id2': order2}, tc._TradingCenter__closedOrders)

    def testConsume(self):
        pass

    def testPostConsume(self):
        pass

    def testCreateAccountWithMetrix(self):
        pass
