'''
Created on Jan 30, 2011

@author: ppa
'''
from xlrd import open_workbook
from xlwt import Workbook
from ultrafinance.lib.errors import UfException, Errors

from os import path

import logging
LOG = logging.getLogger()

class ExcelLib(object):
    ''' lib for accessing excel '''
    READ_MODE = 'r'
    WRITE_MODE = 'w'

    def __init__(self, fileName = None, mode = READ_MODE):
        ''' constructor '''
        if ExcelLib.READ_MODE == mode:
            self.__operation = ExcelRead(fileName)
        elif ExcelLib.WRITE_MODE == mode:
            self.__operation = ExcelWrite(fileName)
        else:
            raise UfException(Errors.INVALID_EXCEL_MODE,
                              "Invalid operation mode, only %s and %s are accepted"\
                              % (ExcelLib.READ_MODE, ExcelLib.WRITE_MODE))

    def __enter__(self):
        ''' call enter of operation '''
        self.__operation.pre()
        return self

    def __exit__(self, type, value, traceback):
        ''' call exit of operation '''
        self.__operation.post()
        return

    def openSheet(self, name):
        ''' open a sheet by name '''
        self.__operation.openSheet(name)

    def readRow(self, row, startCol=0, endCol=-1):
        ''' read row '''
        return self.__operation.readRow(row, startCol, endCol)

    def readCol(self, col, startRow=0, endRow=-1):
        ''' read col '''
        return self.__operation.readCol(col, startRow, endRow)

    def readCell(self, row, col):
        ''' read cell'''
        return self.__operation.readCell(row, col)

    def writeRow(self, row, values):
        ''' write row '''
        self.__operation.writeRow(row, values)

    def writeCell(self, row, col, value):
        ''' write cell'''
        self.__operation.writeCell(row, col, value)

    def getOperation(self):
        ''' get operation'''
        return self.__operation

class ExcelOpertion(object):
    ''' excel operation '''
    DEFAULT_SHEET = "sheet0"

    def openSheet(self, name):
        ''' open sheet '''
        raise UfException(Errors.UNDEFINED_METHOD, "openSheet function is not defined")

    def readRow(self, row, startCol=0, endCol=-1):
        ''' read row '''
        raise UfException(Errors.UNDEFINED_METHOD, "readRow function is not defined")

    def readCol(self, col, startRow=0, endRow=-1):
        ''' read col '''
        raise UfException(Errors.UNDEFINED_METHOD, "readCol function is not defined")

    def readCell(self, row, col):
        ''' read cell'''
        raise UfException(Errors.UNDEFINED_METHOD, "readCell function is not defined")

    def writeRow(self, sheetName, row, values):
        ''' write row '''
        raise UfException(Errors.UNDEFINED_METHOD, "writeRow function is not defined")

    def writeCell(self, sheetName, row, col, value):
        ''' write cell'''
        raise UfException(Errors.UNDEFINED_METHOD, "readCell function is not defined")

    def post(self):
        ''' post action as exit'''
        return

    def pre(self):
        ''' pre action as pre '''
        return

class ExcelWrite(ExcelOpertion):
    ''' class to write excel '''
    def __init__(self, fileName):
        if path.exists(fileName):
            raise UfException(Errors.FILE_EXIST, "File already exist: %s" % fileName)

        self.__fileName = fileName
        self.__workbook = Workbook()
        self.__sheetNameDict ={}
        self.__sheet = None

    def openSheet(self, name):
        ''' set a sheet to write '''
        if name not in self.__sheetNameDict:
            sheet = self.__workbook.add_sheet(name)
            self.__sheetNameDict[name] = sheet

        self.__sheet = self.__sheetNameDict[name]

    def __getSheet(self, name):
        ''' get a sheet by name '''
        if not self.sheetExsit(name):
            raise UfException(Errors.SHEET_NAME_INVALID, "Can't find a sheet named %s" % name)

        return self.__sheetNameDict[name]

    def sheetExsit(self, name):
        ''' whether a sheet name exist or not '''
        return name in self.__sheetNameDict

    def writeCell(self, row, col, value):
        ''' write a cell '''
        if self.__sheet is None:
            self.openSheet(super(ExcelWrite, self).DEFAULT_SHEET)

        self.__sheet.write(row, col, value)

    def writeRow(self, row, values):
        '''
        write a row
        Not sure whether xlwt support write the same cell multiple times
        '''
        if self.__sheet is None:
            self.openSheet(super(ExcelWrite, self).DEFAULT_SHEET)

        for index, value in enumerate(values):
            self.__sheet.write(row, index, value)

    def post(self):
        ''' save workbook to excel file '''
        self.__workbook.save(self.__fileName)


class ExcelRead(ExcelOpertion):
    ''' class to read excel '''
    def __init__(self, fileName):
        ''' constructor '''
        if not path.exists(fileName):
            raise UfException(Errors.FILE_NOT_EXIST, "File doesn't exist: %s" % fileName)

        self.__book = open_workbook(fileName)
        self.__sheet = None

    def openSheet(self, name):
        self.__sheet = self.__book.sheet_by_name(name)

    def getTotalSheetNumber(self):
        return self.__book.nsheets

    def getSheetNames(self):
        return self.__book.sheet_names()

    def readRow(self, row, startCol=0, endCol=-1):
        if self.__sheet is None:
            self.openSheet(super(ExcelRead, self).DEFAULT_SHEET)

        if abs(row) >= self.__sheet.nrows:
            raise UfException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readRow: row number too big: row %s, max %s" % (row, self.__sheet.nrows) )
        if max(abs(startCol), abs(endCol)) > self.__sheet.ncols:
            raise UfException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readRow: col number too big: col %s, max %s" % (max(abs(startCol), abs(endCol)), self.sheet.ncols) )
        if -1 == endCol:
            endCol = self.__sheet.ncols

        return [self.readCell(row, i) for i in range(startCol, endCol)]

    def readCol(self, col, startRow=0, endRow=-1):
        if self.__sheet is None:
            self.openSheet(super(ExcelRead, self).DEFAULT_SHEET)

        if abs(col) > self.__sheet.ncols:
            raise UfException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readCol: col number too big: col %s, max %s" % (col, self.sheet.ncols) )
        if max(abs(startRow), abs(endRow)) > self.__sheet.nrows:
            raise UfException(Errors.INDEX_RANGE_ERROR,
                              "Excellib.readCol: row number too big: row %s, max %s" % (max(abs(startRow), abs(endRow)), self.sheet.nrows) )
        if -1 == endRow:
            endRow = self.__sheet.nrows

        return [self.readCell(i, col) for i in range(startRow, endRow)]

    def readCell(self, row, col):
        ''' read a cell'''
        try:
            if self.__sheet is None:
                self.openSheet(super(ExcelRead, self).DEFAULT_SHEET)

            return self.__sheet.cell(row, col).value
        except BaseException as excp:
            raise UfException(Errors.UNKNOWN_ERROR, "Unknown Error in Excellib.readCell %s" % excp)
