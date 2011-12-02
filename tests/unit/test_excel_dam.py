'''
Created on Nov 27, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.model import Tick, Quote
from ultrafinance.dam.excelDAM import ExcelDAM

class testExcelDAM(unittest.TestCase):

    def setUp(self):
        self.targetPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        self.symbol = 'ebay'

    def tearDown(self):
        pass

    def testWriteExcel(self):
        writeDam = ExcelDAM()
        writeDam.setDir(self.targetPath)
        writeDam.setSymbol(self.symbol)

        for file in [writeDam.targetPath(ExcelDAM.QUOTE), writeDam.targetPath(ExcelDAM.TICK)]:
            if os.path.exists(file):
                os.remove(file)

        quote1 = Quote('1320676200', '32.58', '32.58', '32.57', '32.57', '65212', None)
        quote2 = Quote('1320676201', '32.59', '32.59', '32.58', '32.58', '65213', None)
        tick1 = Tick('1320676200', '32.58', '32.58', '32.57', '32.57', '65212')
        tick2 = Tick('1320676201', '32.59', '32.59', '32.58', '32.58', '65213')
        writeDam.writeQuotes([quote1, quote2])
        writeDam.writeTicks([tick1, tick2])

    def testReadExcel(self):
        self.testWriteExcel()
        readDam = ExcelDAM()
        readDam.setDir(self.targetPath)
        readDam.setSymbol(self.symbol)

        print readDam.readQuotes(0, 10000000000)
        print readDam.readTicks(1320676201, 1320676201)
