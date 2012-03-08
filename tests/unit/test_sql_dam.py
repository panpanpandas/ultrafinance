'''
Created on Nov 27, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.model import Tick, Quote
from ultrafinance.dam.sqlDAM import SqlDAM

class testSqlDAM(unittest.TestCase):

    def setUp(self):
        self.targetPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        self.symbol = 'ebay'

    def tearDown(self):
        pass

    def testSqlDam(self):
        dam = SqlDAM(echo = False)
        dam.setDb('sqlite:////tmp/sqldam.sqlite')
        dam.setSymbol("test")

        quotes = [Quote(*['1320676200', '32.59', '32.59', '32.58', '32.58', '65213', None]),
                  Quote(*['1320676201', '32.60', '32.60', '32.59', '32.59', '65214', None])]
        ticks = [Tick(*['1320676200', '32.59', '32.59', '32.58', '32.58', '65213']),
                 Tick(*['1320676201', '32.60', '32.60', '32.59', '32.59', '65214'])]

        dam.writeQuotes(quotes)
        dam.writeTicks(ticks)
        dam.commit()
        print [str(quote) for quote in dam.readQuotes(0, None) ]
        print [str(tick) for tick in dam.readTicks(0, "1320676201")]
        print [str(tick) for tick in dam.readTicks(0, "1320676202")]

