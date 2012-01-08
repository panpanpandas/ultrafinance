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
        self.tableName =  None

    @abc.abstractmethod
    def read(self, row, col):
        ''' read value with row and col '''
        pass

    @abc.abstractmethod
    def write(self, row, col, value):
        ''' write value with row and col '''
        pass

class HbaseSaver(OutputSaver):
    ''' hbase saver '''
    def __init__(self, ip="localhost", port=9090):
        ''' constructor '''
        super(HbaseSaver, self).__init__()
        self.__hbase = HBaseLib(ip, port)
        self.__tableNameCache = []

    def getTableNames(self):
        ''' make a cache for table name '''
        if not self.__tableNameCache:
            self.__tableNameCache = self.__hbase.getTableNames()

        return self.__tableNameCache

    def resetCols(self, cols):
        ''' create cols '''
        if self.tableName in self.__hbase.getTableNames():
            self.__hbase.deleteTable(self.tableName)

        LOG.debug("create table %s with cols %s" % (self.tableName, cols))
        self.__hbase.createTable(self.tableName, [ColumnDescriptor(name=str(col), maxVersions=5) for col in cols])

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
        if not self.tableName:
            raise UfException(Errors.TABLENAME_NOT_SET,
                              "Table name not set")

        if self.tableName not in self.__hbase.getTableNames():
            self.__hbase.createTable(self.tableName, [ColumnDescriptor(name=col, maxVersions=5)])

        self.__hbase.updateRow(self.tableName,
                               row,
                               [Mutation(column = "%s:" % col, value = str(value))])

if __name__ == '__main__':
    h = HbaseSaver()
    h.tableName = 'unittest_outputSaver'
    h.resetCols(['accountValue', '1'])
    for i in range(10):
        h.write('time1', 'accountValue', 10000)
        accountValue = h.read('time1', 'accountValue')
        print accountValue
        assert str(10000) == accountValue
        assert None == h.read('time1', 'EDFASNONdafs')