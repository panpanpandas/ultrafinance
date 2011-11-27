'''
Created on Sep 27, 2011

@author: ppa
'''
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase import ttypes
from hbase.Hbase import Client, ColumnDescriptor, Mutation

from ultrafinance.lib.errors import UfException, Errors

import logging
LOG = logging.getLogger(__name__)

class HBaseClient:
    ''' Hbase client '''
    def __init__(self):
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        self.__client = Client(protocol)
        transport.open()

    def getTableNames(self):
        ''' get table names '''
        return self.__client.getTableNames()

    def deleteTable(self, tName):
        ''' delete table name '''
        if self.__client.isTableEnabled(tName):
            self.__client.disableTable(tName)

        self.__client.deleteTable(tName)

    def createTable(self, tName, ColumnDescriptors):
        try:
            self.__client.createTable(tName, ColumnDescriptors)
        except ttypes.AlreadyExists as excp:
            raise UfException(Errors.HBASE_CREATE_ERROR,
                              "AlreadyExists Error when creating table %s with cols: %s): %s" % \
                              (tName, [col.name for col in ColumnDescriptors], excp.message))

    def getColumnDescriptors(self, tName):
        try:
            return self.__client.getColumnDescriptors(tName)
        except:
            raise UfException(Errors.UNKNOWN_ERROR,
                              "Error when getting column descriptors table %s" % tName)

    def updateRow(self, tName, rowName, mutations, timestamp=None):
        ''' add row to table '''
        try:
            if timestamp is None:
                self.__client.mutateRow(tName, rowName, mutations)
            else:
                self.__client.mutateRowTs(tName, rowName, mutations, timestamp)
        except Exception as excp:
            raise UfException(Errors.HBASE_UPDATE_ERROR,
                              "Error when updating table %s - rowName %s - mutations %s: %s" % \
                              (tName, rowName, mutations, excp))

    def getRow(self, tName, rowName):
        ''' get row '''
        result = self.__client.getRow(tName, rowName)
        if not result:
            return result
        else:
            return result[0]

    def scanTable(self, tName, columns, startRow="", endRow=None):
        ''' scan a table '''
        if endRow is None:
            scanner = self.__client.scannerOpen(tName, startRow, columns)
        else:
            scanner = self.__client.scannerOpenWithStop(tName, startRow, endRow, columns)
        ret = []

        row = self.__client.scannerGet(scanner)
        while row:
            ret.append(row[0])
            row = self.__client.scannerGet(scanner)

        return ret

    def getClient(self):
        ''' return client, in case low level api is needed '''
        return self.__client

# testing
if __name__ == '__main__':
    h = HBaseClient()

    #delete all exiting tables
    for tName in h.getTableNames():
        print "deleting %s" % tName
        h.deleteTable(tName)

    assert not h.getTableNames()

    #create table
    tName = 'testTable'


    h.createTable(tName, [ColumnDescriptor(name='col1', maxVersions=5), ColumnDescriptor(name='col2', maxVersions=5)])
    print h.getTableNames()
    assert h.getTableNames()

    print "column families in %s" %(tName)
    print h.getColumnDescriptors(tName)

    #updateRow
    h.updateRows(tName, "bar", [Mutation(column="col1:bar", value='12345'), Mutation(column="col2:", value="67890")])
    h.updateRows(tName, "foo", [Mutation(column="col1:foo", value='12345')])
    print h.getRow(tName, 'bar')
    print h.getRow(tName, 'foo')

    #scan table
    rows = h.scanTable(tName, columns=["col1", "col2"])
    print rows
    assert 2 == len(rows)

    rows = h.scanTable(tName, columns=["col1", "col2"], startRow="foo")
    print rows
    assert 1 == len(rows)

    rows = h.scanTable(tName, columns=["col1", "col2"], endRow="foo")
    print rows
    assert 1 == len(rows)