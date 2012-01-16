'''
Created on Jan 18, 2011

@author: ppa
'''
import mox
import unittest
from ultrafinance.backTest.tickFeeder import TickFeeder
from ultrafinance.lib.errors import UfException

class testTickFeeder(unittest.TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        pass

    def testAddSource(self):
        dam = self.mock.CreateMockAnything('dam')
        dam.symbol = 's1'

        tf = TickFeeder()
        tf.addSource(dam)

        print tf._TickFeeder__source
        self.assertEquals({'s1': dam}, tf._TickFeeder__source)

    def testGetSymbolsByRe(self):
        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        symbols = tf.getSymbolsByRe('s3')
        print symbols
        self.assertEquals([], symbols)

        symbols = tf.getSymbolsByRe('s1')
        print symbols
        self.assertEquals(['s1'], symbols)

        symbols = tf.getSymbolsByRe('.*')
        print symbols
        self.assertEquals(set(symbols), set(['s1', 's11', 's2']))

    def testValidate_Normal(self):
        sub = self.mock.CreateMockAnything('sub')
        sub.subRules().AndReturn(['s1', 'mockRule'])

        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        self.mock.ReplayAll()
        symbols, sub = tf.validate(sub)
        print symbols
        self.mock.VerifyAll()

    def testValidate_Exception(self):
        sub = self.mock.CreateMockAnything('sub')
        sub.subRules().AndReturn(['s3', 'mockRule'])

        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        self.mock.ReplayAll()
        self.assertRaises(UfException, tf.validate, sub)
        self.mock.VerifyAll()