'''
Created on Jan 30, 2011

@author: ppa
'''
from xlrd import open_workbook

from lib.errors import ufException, Errors
import logging
LOG = logging.getLogger(__name__)

class ExcelLib():
    ''' lib for aceesing excel '''
    def __init__(self, fileName=None, sheetNumber=0, sheetName=None):
        '''
        constructor

        '''
        self.book = None
        self.sheet = None
        if fileName is not None:
            self.book = open_workbook(fileName)
            self.sheet = self.book.sheet_by_name(sheetName) if sheetName \
                         else self.book.sheet_by_index(sheetNumber)

    def __enter__(self):
        '''
        do nothing because xlrd handle file close in Book constructor,
        which make reading multiple sheets slow
        '''
        return self

    def __exit__(self, type, value, traceback):
        ''' do nothing '''
        pass

    def openSheet(self, sheetNumber=0, sheetName=None):
        self.sheet = self.book.sheet_by_name(sheetName) if sheetName \
                     else self.book.sheet_by_index(sheetNumber)

    @staticmethod
    def getTotalSheetNumber(fileName):
        return open_workbook(fileName).nsheets

    @staticmethod
    def getSheetNames(fileName):
        return open_workbook(fileName).sheet_names()

    def setSheetNumber(self, sheetNumber):
        self.sheet = self.book.sheet_by_index(sheetNumber)

    def readRow(self, rowNumber, startCol=0, endCol=-1):
        if abs(rowNumber) >= self.sheet.nrows:
            raise ufException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readRow: row number too big: row %s, max %s" % (rowNumber, self.sheet.nrows) )
        if max(abs(startCol), abs(endCol)) > self.sheet.ncols:
            raise ufException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readRow: col number too big: col %s, max %s" % (max(abs(startCol), abs(endCol)), self.sheet.ncols) )
        if -1 == endCol:
            endCol = self.sheet.ncols

        return [self.readCell(rowNumber, i) for i in range(startCol, endCol)]

    def readCol(self, colNumber, startRow=0, endRow=-1):
        if abs(colNumber) > self.sheet.ncols:
            raise ufException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readCol: col number too big: col %s, max %s" % (colNumber, self.sheet.ncols) )
        if max(abs(startRow), abs(endRow)) > self.sheet.nrows:
            raise ufException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readCol: row number too big: row %s, max %s" % (max(abs(startRow), abs(endRow)), self.sheet.nrows) )
        if -1 == endRow:
            endRow = self.sheet.nrows

        return [self.readCell(i, colNumber) for i in range(startRow, endRow)]

    def readCell(self, rowNumber, colNumber):
        ''' read a cell'''
        try:
            return self.sheet.cell(rowNumber, colNumber).value
        except BaseException as excep:
            raise ufException(Errors.UNKNOWN_ERROR, "Unknown Error in Excellib.readCell %s" % excep)