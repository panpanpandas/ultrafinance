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
        print([str(quote) for quote in dam.readQuotes(0, None) ])
        print([str(tick) for tick in dam.readTicks(0, "1320676201")])
        print([str(tick) for tick in dam.readTicks(0, "1320676202")])


    def testFundamental(self):
        dam = SqlDAM(echo = False)
        dam.setDb('sqlite:////tmp/sqldam.sqlite')
        dam.setSymbol("test")

        keyTimeValueDict = {'Total Debt': {'As of 2011-12-31': 2089.6500000000001, 'As of 2012-03-31': 2085.0, 'As of 2010-12-31': 1794.23, 'As of 2009-12-31': 0.0, 'As of 2008-12-31': 1000.0, 'As of 2011-09-30': 2543.9899999999998, 'As of 2011-06-30': 2545.6999999999998, 'As of 2011-03-31': 1794.48}, 'Effect of Special Items on Income Taxes': {'12 months ending 2010-12-31': None, '3 months ending 2011-09-30': None, '12 months ending 2008-12-31': None, '3 months ending 2012-03-31': None, '3 months ending 2011-12-31': None, '12 months ending 2011-12-31': None, '12 months ending 2009-12-31': None, '3 months ending 2011-03-31': None, '3 months ending 2011-06-30': None}}
        dam.writeFundamental(keyTimeValueDict)
        dam.commit()

        ret = dam.readFundamental()
        print(ret)
        self.assertEqual(keyTimeValueDict, ret)
