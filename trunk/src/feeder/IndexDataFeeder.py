'''
Created on Jan 30, 2010

@author: ppa
'''
from lib.ExcelLib import ExcelLib
from BaseModule import BaseModule
from lib.DataType import DateValueType

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
        with ExcelLib('../dataSource/longTerm_1871.xls', 0) as excel:
            year = excel.readCol(0, 8, 147)
            stock = excel.readCol(1, 8, 147)
            for i in range(len(year)):
                self.stockData.append(DateValueType(str(int(year[i])), stock[i]))

        ret = self.stockData
        print ret
        return ret

if __name__ == '__main__':
    feeder = IndexDataFeeder()
    feeder.execute("")
    print feeder.stockData