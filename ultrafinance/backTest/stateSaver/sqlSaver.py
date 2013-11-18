'''
Created on Mar 1, 2011

@author: ppa
'''
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.stateSaver import StateSaver
from ultrafinance.model import Order

from sqlalchemy import Table, Column, Integer, String, create_engine, MetaData, and_, select
from sqlalchemy.ext.declarative import declarative_base

from ultrafinance.backTest.constant import STATE_SAVER_ACCOUNT, STATE_SAVER_UPDATED_ORDERS, STATE_SAVER_PLACED_ORDERS, STATE_SAVER_HOLDING_VALUE, STATE_SAVER_INDEX_PRICE

import sys
import json

import logging
LOG = logging.getLogger()

Base = declarative_base()

class BackTestResult(object):
    ''' back test result class '''
    def __init__(self, time, account, holdingValue, indexPrice, updateOrders, placedOrders):
        ''' constructor '''
        self.time = time
        self.account = account
        self.holdingValue = holdingValue
        self.indexPrice = indexPrice
        self.updateOrders = updateOrders
        self.placedOrders = placedOrders

    def __str__(self):
        ''' convert to string '''
        return json.dumps({"time": self.time,
                           STATE_SAVER_ACCOUNT: self.account,
                           STATE_SAVER_HOLDING_VALUE: self.holdingValue,
                           STATE_SAVER_INDEX_PRICE: self.indexPrice,
                           STATE_SAVER_UPDATED_ORDERS: [json.loads(str(order)) for order in self.updateOrders],
                           STATE_SAVER_PLACED_ORDERS: [json.loads(str(order)) for order in self.placedOrders]})

class SqlSaver(StateSaver):
    ''' sql saver '''
    COLUMNS = [Column('time', Integer, primary_key = True),
               Column(STATE_SAVER_ACCOUNT, String(40)),
               Column(STATE_SAVER_INDEX_PRICE, String(40)),
               Column(STATE_SAVER_UPDATED_ORDERS, String(200)),
               Column(STATE_SAVER_HOLDING_VALUE, String(40)),
               Column(STATE_SAVER_PLACED_ORDERS, String(200))]

    EXISTED_TABLE_DICT = {}

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

    def setup(self, setting, tableName):
        ''' setup '''
        if 'db' in setting:
            self.db = setting['db']
            self.engine = create_engine(setting['db'], echo = False)
            self.tableName = tableName
            self.__constructTable()
            self.table = SqlSaver.EXISTED_TABLE_DICT.get(tableName)

    def __constructTable(self):
        ''' construct table '''
        if not self.firstTime or self.table is not None or not self.tableName \
        or self.tableName in SqlSaver.EXISTED_TABLE_DICT:
            return

        SqlSaver.EXISTED_TABLE_DICT[self.tableName] = Table(self.tableName,
                                                            self.metadata,
                                                            *SqlSaver.COLUMNS)


    def resetTable(self):
        ''' create cols '''
        self.table.drop(self.engine, checkfirst = True)

        LOG.info("create db %s with table %s with cols %s" % (self.db, self.tableName, SqlSaver.COLUMNS))
        self.table.create(self.engine, checkfirst = True)

    def getStates(self, start, end):
        ''' read value for a col  '''
        if self.engine is None:
            return []

        if end is None:
            end = sys.maxint

        conn = self.engine.connect()
        rows = conn.execute(select([self.table]).where(and_(self.table.c.time >= int(start),
                                                            self.table.c.time < int(end))))

        return [self.__tupleToResult(row) for row in rows]

    def __tupleToResult(self, row):
        ''' convert tuple queried from sql to BackTestResult'''
        try:
            return BackTestResult(row['time'],
                                  row[STATE_SAVER_ACCOUNT],
                                  row[STATE_SAVER_HOLDING_VALUE],
                                  row[STATE_SAVER_INDEX_PRICE],
                                  [Order.fromStr(orderString) for orderString in json.loads(row[STATE_SAVER_UPDATED_ORDERS])],
                                  [Order.fromStr(orderString) for orderString in json.loads(row[STATE_SAVER_PLACED_ORDERS])])
        except Exception as ex:
            LOG.error("Unknown exception doing __tupleToResult in sqlSaver " + str(ex) + " --row-- " + str(row))
            return BackTestResult('-1', '-1', '[]', '[]')


    def __sqlToResult(self, row):
        ''' convert row result '''
        return (row.time, )


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

        self.resetTable()

        # write values
        updates = []
        for row, colValueDict in self.__writeCache.iteritems():
            update = {'time': row}
            update.update(colValueDict)
            # fill column that are empty
            if STATE_SAVER_ACCOUNT not in update:
                update[STATE_SAVER_ACCOUNT] = ""
            if STATE_SAVER_HOLDING_VALUE not in update:
                update[STATE_SAVER_HOLDING_VALUE] = ""
            if STATE_SAVER_INDEX_PRICE not in update:
                update[STATE_SAVER_INDEX_PRICE] = ""
            if STATE_SAVER_PLACED_ORDERS not in update:
                update[STATE_SAVER_PLACED_ORDERS] = "[]"
            if STATE_SAVER_UPDATED_ORDERS not in update:
                update[STATE_SAVER_UPDATED_ORDERS] = "[]"

            # convert everything to string
            for key in update.keys():
                update[key] = str(update[key])

            updates.append(update)

        conn = self.engine.connect()
        conn.execute(self.table.insert(), updates)
        LOG.info("committed table %s at %s" % (self.table, self.db))

def listTableNames(db):
    ''' list names of tables '''
    try:
        engine = create_engine(db, echo = False)
        metadata = MetaData()
        metadata.reflect(engine)
        return metadata.tables.keys()
    except Exception as ex:
        LOG.error("Unknown error " + str(ex))
        return []


if __name__ == '__main__':
    s = SqlSaver()
    s.setup({'db': 'sqlite:////data/test_output.sqlite'}, 'unittest_outputSaver')
    #h.resetCols(['accountValue', '1'])
    for i in range(5):
        s.write(123456, STATE_SAVER_HOLDING_VALUE, 10000)
        s.commit()

    print listTableNames("sqlite:////data/output.sqlite")
