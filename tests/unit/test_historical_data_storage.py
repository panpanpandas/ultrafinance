'''
Created on May 6, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.lib.historicalDataStorage import HistoricalDataStorage

import logging
LOG = logging.getLogger(__name__)

class testHistoricalDataStorage(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBuildExlsFromFile(self):
        stockListFile = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'stock.list' )
        outputPrefix = os.path.join( os.path.dirname( os.path.dirname(os.path.abspath(__file__)) ),
                                     'output', 'fromFile' )
        storage = HistoricalDataStorage(outputPrefix)
        storage.buildExlsFromFile(stockListFile, 2)

    def testBuildExls(self):
        outputPrefix = os.path.join( os.path.dirname( os.path.dirname(os.path.abspath(__file__)) ),
                                     'output', 'buildExl' )
        storage = HistoricalDataStorage(outputPrefix)
        storage.buildExls(['MMM', 'ACE', 'ABT', 'ANF', 'ADBE', 'AMD'], 2)
