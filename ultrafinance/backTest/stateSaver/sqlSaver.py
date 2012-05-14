'''
Created on Mar 1, 2011

@author: ppa
'''
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.stateSaver import StateSaver

from sqlalchemy import Table, Column, Integer, String, Float, Sequence, create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging
LOG = logging.getLogger()

Base = declarative_base()

class SqlSaver(StateSaver):
    ''' sql saver '''
    def __init__(self):
        ''' constructor '''
        #__writeCache:
        #{
        #"timestamp" : {"field1": 'value',
        #               "field1": 'value',
        #               "field1": 'value'}
        #}
        super(SqlSaver, self).__init__()
        self.__writeCache = {}
        self.table = None
        self.db = None
        self.metadata = MetaData()
        self.engine = None
        self.firstTime = True

    def setup(self, setting):
        ''' setup '''
        if 'db' in setting:
            self.db = setting['db']
            self.engine = create_engine(setting['db'], echo = False)

    def constructTable(self, cols):
        ''' construct table '''
        if not self.firstTime or self.table is not None or not self.tableName:
            return

        columns = [Column('time', Integer, primary_key = True)]
        for col in cols:
            columns.append(Column(col, String(200)))

        self.table = Table(self.tableName, self.metadata, *columns)

    def resetTable(self, cols):
        ''' create cols '''
        self.constructTable(cols)

        self.table.drop(self.engine, checkfirst = True)

        LOG.info("create db %s with table %s with cols %s" % (self.db, self.tableName, cols))
        self.table.create(self.engine, checkfirst = True)

    def read(self, row, col):
        ''' read value with row and col '''
        return None

    def write(self, timestamp, col, value):
        ''' write value with row and col '''
        if (int == int(timestamp)):
            LOG.error("timestamp %s is not integer" % timestamp)
            return

        if timestamp not in self.__writeCache:
            self.__writeCache[timestamp] = {}
        self.__writeCache[timestamp][col] = value

    def commit(self):
        ''' complete write operation '''
        if not self.tableName:
            raise UfException(Errors.TABLENAME_NOT_SET,
                              "Table name not set")

        # reset table with all cols first
        cols = set()
        for colValueDict in self.__writeCache.itervalues():
            cols.update(colValueDict.iterkeys())

        self.resetTable(cols)

        # write values
        updates = []
        for row, colValueDict in self.__writeCache.iteritems():
            update = {'time': row}
            update.update(colValueDict)
            # fill filed that are empty
            for col in cols:
                if col not in update:
                    update[col] = ""

            # convert everything to string
            for key in update.keys():
                update[key] = str(update[key])

            updates.append(update)

        conn = self.engine.connect()
        conn.execute(self.table.insert(), updates)
        LOG.info("committed table %s at %s" % (self.table, self.db))

if __name__ == '__main__':
    s = SqlSaver()
    s.tableName = 'unittest_outputSaver'
    s.setup({'db': 'sqlite:////tmp/test_output.sqlite'})
    #h.resetCols(['accountValue', '1'])
    for i in range(5):
        s.write(123456, 'accountValue', 10000)
        s.commit()

