'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import Errors, UfException
import abc
from ultrafinance.dam.hbaseLib import HBaseLib
from hbase.Hbase import Mutation, ColumnDescriptor

import logging
LOG = logging.getLogger()

class OutputSaver(object):
    ''' output saver '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        ''' constructor '''
        self.__tableName = None

    @abc.abstractmethod
    def read(self, row, col):
        ''' read value with row and col '''
        pass

    @abc.abstractmethod
    def write(self, row, col, value):
        ''' write value with row and col '''
        pass

    def writeComplete(self):
        ''' complete write operation '''
        pass

    def getTableName(self):
        ''' return table name '''
        return self.__tableName

    def setTableName(self, tableName):
        ''' set table name, table name can only be set once '''
        if self.__tableName:
            raise UfException(Errors.TABLENAME_ALREADY_SET,
                              "table name %s already set" % self.__tableName)

        self.__tableName = tableName

    tableName = property(getTableName, setTableName)

class HbaseSaver(OutputSaver):
    ''' hbase saver '''
    def __init__(self, ip = "localhost", port = 9090):
        ''' constructor '''
        super(HbaseSaver, self).__init__()
        self.__hbase = HBaseLib(ip, port)
        self.__writeCache = {}

    def resetCols(self, cols):
        ''' create cols '''
        if self.tableName in self.__hbase.getTableNames():
            self.__hbase.deleteTable(self.tableName)

        LOG.debug("create table %s with cols %s" % (self.tableName, cols))
        self.__hbase.createTable(self.tableName, [ColumnDescriptor(name = str(col), maxVersions = 5) for col in cols])

    def read(self, row, col):
        ''' read value with row and col '''
        oneRow = self.__hbase.getRow(self.tableName, row)
        keyValues = oneRow.columns
        key = "%s:" % col

        if key in keyValues:
            return keyValues[key].value
        else:
            return None

    def write(self, row, col, value):
        ''' write value with row and col '''
        self.__writeCache[(row, col)] = value

    def writeComplete(self):
        ''' complete write operation '''
        if not self.tableName:
            raise UfException(Errors.TABLENAME_NOT_SET,
                              "Table name not set")

        # reset table with all cols first
        cols = set()
        for (row, col) in self.__writeCache.iterkeys():
            cols.add(col)

        self.resetCols(cols)

        # write values
        for (row, col), value in self.__writeCache.iteritems():
            self.__hbase.updateRow(self.tableName,
                                   row,
                                   [Mutation(column = "%s:" % col, value = str(value))])

class OutputSaverFactory(object):
    ''' factory for output saver '''
    HBASE = 'hbase'
    def __init__(self):
        ''' constructor '''
        self.saverDict = {OutputSaverFactory.HBASE: HbaseSaver}

    def createOutputSaver(self, name):
        ''' create output saver '''
        if name not in self.saverDict:
            raise UfException(Errors.INVALID_SAVER_NAME,
                              "Saver name is invalid %s" % name)

        return self.saverDict[name]()

if __name__ == '__main__':
    saverFactory = OutputSaverFactory()
    h = saverFactory.createOutputSaver(OutputSaverFactory.HBASE)

    h.tableName = 'unittest_outputSaver'
    #h.resetCols(['accountValue', '1'])
    for i in range(5):
        h.write('time1', 'accountValue', 10000)
        h.writeComplete()
        accountValue = h.read('time1', 'accountValue')
        print accountValue
        assert str(10000) == accountValue
        assert None == h.read('time1', 'EDFASNONdafs')
