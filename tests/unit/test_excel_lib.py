'''
Created on May 6, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.lib.excelLib import ExcelLib

class testExcelLib(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadExcel(self):
        dataSourcePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dataSource')
        with ExcelLib( os.path.join(dataSourcePath, 'hoursing_interestRate.xls') ) as excel:
            excel.setSheetNumber(0)
            data = excel.readRow(0)
            assert len(data)
            data = excel.readCol(0, 7)
            assert len(data)