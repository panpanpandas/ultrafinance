'''
Created on Jan 18, 2011

@author: ppa
'''
import mox
import unittest
from ultrafinance.backTest.tickSubscriber import TickSubsriber
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.model import Tick

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

        print(tf._TickFeeder__source)
        self.assertEquals({'s1': dam}, tf._TickFeeder__source)

    def testGetSymbolsByRe(self):
        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        symbols = tf.getSymbolsByRe('s3')
        print(symbols)
        self.assertEquals([], symbols)

        symbols = tf.getSymbolsByRe('s1')
        print(symbols)
        self.assertEquals(['s1'], symbols)

        symbols = tf.getSymbolsByRe('.*')
        print(symbols)
        self.assertEquals(set(symbols), set(['s1', 's11', 's2']))

    def testValidate_Normal(self):
        sub = self.mock.CreateMock(TickSubsriber)
        sub.subRules().AndReturn(['s1', 'mockRule'])

        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        self.mock.ReplayAll()
        symbols, sub = tf.validate(sub)
        self.mock.VerifyAll()

        print(symbols)


    def testValidate_Exception(self):
        sub = self.mock.CreateMock(TickSubsriber)
        sub.subRules().AndReturn(['s3', 'mockRule'])

        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        self.mock.ReplayAll()
        self.assertRaises(UfException, tf.validate, sub)
        self.mock.VerifyAll()

    def testRegister_Normal(self):
        sub = self.mock.CreateMock(TickSubsriber)
        sub.subRules().AndReturn(['s1', 'mockRule'])

        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        self.mock.ReplayAll()
        tf.register(sub)
        self.mock.VerifyAll()

        subs = tf.getSubs()
        print(subs)
        self.assertEquals({sub: {'symbols': ['s1'], 'fail': 0} },
                          subs)

    def testRegister_Exception(self):
        sub = self.mock.CreateMock(TickSubsriber)
        sub.subRules().AndReturn(['s3', 'mockRule'])

        tf = TickFeeder()
        tf._TickFeeder__source = {'s1': 'dam1', 's11': 'dam2', 's2': 'dam3'}

        self.mock.ReplayAll()
        self.assertRaises(UfException, tf.register, sub)
        self.mock.VerifyAll()

    def testInputType(self):
        tf = TickFeeder()

        #invalid type - test assignment
        self.assertRaises(UfException, tf._TickFeeder__setInputType, 'adafsdf')

        #valid type - test assignment
        tf.inputType = TickFeeder.TICK_TYPE

        self.assertEquals(TickFeeder.TICK_TYPE, tf.inputType)

    def testIndexTicks_quote(self):
        tickTime1Dam1 = Tick('time1', 'open1', 'high1', 'low1', 'close1', 'volume1')
        tickTime2Dam1 = Tick('time2', 'open2', 'high2', 'low2', 'close2', 'volume2')
        tickTime1Dam2 = Tick('time1', 'open11', 'high11', 'low11', 'close11', 'volume11')
        tickTime2Dam2 = Tick('time2', 'open22', 'high22', 'low22', 'close22', 'volume22')

        dam1 = self.mock.CreateMock(BaseDAM)
        dam1.readQuotes(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([tickTime1Dam1, tickTime2Dam1])

        dam2 = self.mock.CreateMock(BaseDAM)
        dam2.readQuotes(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([tickTime1Dam2, tickTime2Dam2])

        tf = TickFeeder()
        tf.inputType = TickFeeder.QUOTE_TYPE
        tf._TickFeeder__source = {'s1': dam1, 's2': dam2}

        self.mock.ReplayAll()
        timeTicks = tf.indexTicks()
        self.mock.VerifyAll()

        print(timeTicks)
        self.assertEquals({'time1': {'s1': tickTime1Dam1, 's2': tickTime1Dam2},
                           'time2': {'s1': tickTime2Dam1, 's2': tickTime2Dam2}},
                           timeTicks)


    def testIndexTicks_tick(self):
        tickTime1Dam1 = Tick('time1', 'open1', 'high1', 'low1', 'close1', 'volume1')
        tickTime2Dam1 = Tick('time2', 'open2', 'high2', 'low2', 'close2', 'volume2')
        tickTime1Dam2 = Tick('time1', 'open11', 'high11', 'low11', 'close11', 'volume11')
        tickTime2Dam2 = Tick('time2', 'open22', 'high22', 'low22', 'close22', 'volume22')

        dam1 = self.mock.CreateMock(BaseDAM)
        dam1.readTicks(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([tickTime1Dam1, tickTime2Dam1])

        dam2 = self.mock.CreateMock(BaseDAM)
        dam2.readTicks(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([tickTime1Dam2, tickTime2Dam2])

        tf = TickFeeder()
        tf.inputType = TickFeeder.TICK_TYPE
        tf._TickFeeder__source = {'s1': dam1, 's2': dam2}

        self.mock.ReplayAll()
        timeTicks = tf.indexTicks()
        self.mock.VerifyAll()

        print(timeTicks)
        self.assertEquals({'time1': {'s1': tickTime1Dam1, 's2': tickTime1Dam2},
                           'time2': {'s1': tickTime2Dam1, 's2': tickTime2Dam2}},
                           timeTicks)

    def testPubTicks(self):
        sub = self.mock.CreateMock(TickSubsriber)
        sub.runConsume(['ticks'])

        tf = TickFeeder()
        self.mock.ReplayAll()
        thread = tf.pubTicks(['ticks'], sub)
        self.mock.VerifyAll()

        print (thread)

    #TODO, too lazy to write this one........
    def testExecute(self):
        pass