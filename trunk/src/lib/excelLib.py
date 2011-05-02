'''
Created on Jan 30, 2011

@author: ppa
'''
from xlrd import open_workbook

class ExcelLib():
    ''' lib for aceesing excel '''
    def __init__(self, fileName=None, sheetNumber=0, sheetName=None):
        ''' constructor '''
        self.book = None
        self.sheet = None
        if fileName is not None:
            self.book = open_workbook(fileName)
            self.sheet = self.book.sheet_by_name(sheetName) if sheetName \
                         else self.book.sheet_by_index(sheetNumber)

    def __enter__(self):
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
            print "row number too big"
            return None
        if abs(startCol) >= self.sheet.ncols:
            print "start col too big"
            return None
        if abs(endCol) >= self.sheet.ncols:
            print "end col too big, max is %s" %str(self.sheet.ncols)
            return None
        if -1 == endCol:
            endCol = self.sheet.ncols

        return [self.sheet.cell(rowNumber, i).value for i in range(startCol, endCol)]

    def readCol(self, colNumber, startRow=0, endRow=-1):
        if abs(colNumber) > self.sheet.ncols:
            print "col number too big"
            return None
        if abs(startRow) > self.sheet.nrows:
            print "start row too big, max is %s" %str(self.sheet.nrows)
            return None
        if abs(endRow) > self.sheet.nrows:
            print "end row too big, max is %s" %str(self.sheet.nrows)
            return None
        if -1 == endRow:
            endRow = self.sheet.nrows

        return [self.sheet.cell(i, colNumber).value for i in range(startRow, endRow)]


    def readCell(self, rowNumber, colNumber):
        ''' read a cell'''
        return self.sheet(rowNumber, colNumber)

if __name__ == '__main__':
    with ExcelLib('../../dataSource/hoursing_interestRate.xls') as excel:
        excel.setSheetNumber(0)
        print excel.readRow(0)
        print excel.readCol(0, 7)