'''
Created on May 6, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.dam.excelLib import ExcelLib

class testExcelLib(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadExcel(self):
        dataSourcePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dataSource')
        with ExcelLib( fileName = os.path.join(dataSourcePath, 'hoursing_interestRate.xls'),
                       mode = ExcelLib.READ_MODE ) as excel:
            print "sheet numbers: %s" % excel.getOperation().getTotalSheetNumber()
            print "sheetNames %s" % excel.getOperation().getSheetNames()
            excel.openSheet('Data')
            data = excel.readRow(0)
            print data
            assert len(data)

            data = excel.readCol(0, 7)
            print data
            assert len(data)

    def testWriteExcel(self):
        targetPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        targetFile = os.path.join(targetPath, "writeTest.xls")
        sheetName = "testSheet"

        if os.path.exists(targetFile):
            os.remove(targetFile)

        with ExcelLib(fileName = targetFile,
                      mode = ExcelLib.WRITE_MODE ) as excel:
            excel.openSheet(sheetName)
            excel.writeRow(0, [1, 2, 3, "4", "5"])

        if not os.path.exists(targetFile):
            assert 0
