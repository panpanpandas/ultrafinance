'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.dam.excelLib import ExcelLib
from ultrafinance.model import TICK_FIELDS, QUOTE_FIELDS
from ultrafinance.lib.errors import UfException, Errors

from os import path

import logging
LOG = logging.getLogger(__name__)

class ExcelDAM(BaseDAM):
    ''' Excel DAO '''
    QUOTE = 'quote'
    TICK = 'tick'

    def __init__(self):
        ''' constructor '''
        super(ExcelDAM, self).__init__()
        self.__dir = None

    def targetPath(self, kind):
        return path.join(self.__dir, "%s-%s.xls" % (self.symbol, kind) )

    def __findRange(self, excelLib, start, end):
        ''' return low and high as excel range '''
        inc = 1
        low = 0
        high = 0
        dates = excelLib.readCol(0, 1)

        for index, date in enumerate(dates):
            if int(start) <= int(date):
                low = index + inc
                break

        if low:
            for index, date in reversed(list(enumerate(dates))):
                if int(date) <= int(end):
                    high = index + inc
                    break

        return low, high

    def __readData(self, targetPath, start, end):
        ''' read data '''
        ret = []
        if not path.exists(targetPath):
            LOG.error("Target file doesn't exist: %s" % path.abspath(targetPath) )
            return ret

        with ExcelLib(fileName = targetPath, mode = ExcelLib.READ_MODE) as excel:
            low, high = self.__findRange(excel, start, end)

            for index in range(low, high + 1):
                ret.append(excel.readRow(index))

        return ret

    def __writeData(self, targetPath, fields, values):
        ''' write data '''
        if path.exists(targetPath):
            LOG.error("Target file exists: %s" % path.abspath(targetPath) )
            raise UfException(Errors.FILE_EXIST, "can't write to a existing file") #because xlwt doesn't support it

        with ExcelLib(fileName = targetPath, mode = ExcelLib.WRITE_MODE) as excel:
            excel.writeRow(0, fields)
            for index, value in enumerate(values):
                excel.writeRow(index+1, value)

    def readQuotes(self, start, end):
        ''' read quotes '''
        return self.__readData(self.targetPath(ExcelDAM.QUOTE), start, end)

    def writeQuotes(self, quotes):
        ''' write quotes '''
        self.__writeData(self.targetPath(ExcelDAM.QUOTE), QUOTE_FIELDS, quotes)

    def readTicks(self, start, end):
        ''' read ticks '''
        return self.__readData(self.targetPath(ExcelDAM.TICK), start, end)

    def writeTicks(self, ticks):
        ''' read quotes '''
        self.__writeData(self.targetPath(ExcelDAM.TICK), TICK_FIELDS, ticks)

    def setDir(self, path):
        ''' set dir '''
        self.__dir = path