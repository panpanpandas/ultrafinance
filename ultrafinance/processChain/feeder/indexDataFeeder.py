'''
Created on Jan 30, 2011

@author: ppa
'''
from ultrafinance.lib.excelLib import ExcelLib
from ultrafinance.processChain.baseModule import BaseModule
from ultrafinance.lib.dataType import DateValueType
from os.path import join

import logging
LOG = logging.getLogger(__name__)

class IndexDataFeeder(BaseModule):
    '''
    feeder that get stock, hoursing and interest rate from excel
    '''
    def __init__(self):
        ''' Constructor '''
        super(IndexDataFeeder, self).__init__()
        self.stockData = []

    def execute(self, input):
        ''' preparing data'''
        with ExcelLib(join('dataSource', 'longTerm_1871.xls'), 0) as excel:
            year = excel.readCol(0, 8, 147)
            stock = excel.readCol(1, 8, 147)
            for i in range(len(year)):
                self.stockData.append(DateValueType(str(int(year[i])), stock[i]))

        ret = self.stockData
        return ret

if __name__ == '__main__':
    feeder = IndexDataFeeder()
    feeder.execute("")
    print feeder.stockData