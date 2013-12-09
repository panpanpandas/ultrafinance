'''
Created on Mar 1, 2011

@author: ppa
'''
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.stateSaver import StateSaver
from ultrafinance.model import Order

from sqlalchemy import Table, Column, Integer, String, create_engine, MetaData, and_, select
from sqlalchemy.ext.declarative import declarative_base

from ultrafinance.backTest.constant import *

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
    RESULT_COLUMNS = [Column('time', Integer, primary_key = True),
                      Column(STATE_SAVER_ACCOUNT, String(40)),
                      Column(STATE_SAVER_INDEX_PRICE, String(40)),
                      Column(STATE_SAVER_UPDATED_ORDERS, String(200)),
                      Column(STATE_SAVER_HOLDING_VALUE, String(40)),
                      Column(STATE_SAVER_PLACED_ORDERS, String(200))]

    METRICS_COLUMNS = [Column('metric', String(40), primary_key = True),
                       Column('value', String(40))]

    RESULT_TABLE = None
    METRICS_TABLE = None

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
        self.__metrics = []
        self.db = None
        self.metadata = None
        self.engine = None

    def setup(self, setting):
        ''' setup '''
        if 'db' in setting:
            self.db = setting['db']
            self.engine = create_engine(setting['db'], echo = False)
            self.metadata = MetaData(self.engine)
            self.__constructTableIfNotExist()

    def __constructTableIfNotExist(self):
        ''' construct table '''
        if SqlSaver.RESULT_TABLE is None:
            SqlSaver.RESULT_TABLE = Table("result",
                                          self.metadata,
                                          *SqlSaver.RESULT_COLUMNS)

        if SqlSaver.METRICS_TABLE is None:
            SqlSaver.METRICS_TABLE = Table("metrics",
                                           self.metadata,
                                           *SqlSaver.METRICS_COLUMNS)

    def __resetResultTable(self):
        ''' reset result table '''
        SqlSaver.RESULT_TABLE.drop(self.engine, checkfirst = True)

        LOG.info("create db %s with cols %s" % (self.db, SqlSaver.RESULT_COLUMNS))
        SqlSaver.RESULT_TABLE.create(self.engine, checkfirst = True)

    def __resetMetricsTable(self):
        ''' reset result table '''
        SqlSaver.METRICS_TABLE.drop(self.engine, checkfirst = True)

        LOG.info("create db %s with cols %s" % (self.db, SqlSaver.METRICS_COLUMNS))
        SqlSaver.METRICS_TABLE.create(self.engine, checkfirst = True)

    def getStates(self, start, end):
        ''' read value for a col  '''
        if self.engine is None:
            return []

        if end is None:
            end = sys.maxint

        conn = self.engine.connect()
        rows = conn.execute(select([SqlSaver.RESULT_TABLE]).where(and_(SqlSaver.RESULT_TABLE.c.time >= int(start),
                                                                  SqlSaver.RESULT_TABLE.c.time < int(end))))

        #return [self.__tupleToResult(row) for row in rows]
        ret = []
        for row in rows:
            ret.append({"time": row['time'],
                        STATE_SAVER_ACCOUNT: row[STATE_SAVER_ACCOUNT],
                        STATE_SAVER_HOLDING_VALUE: row[STATE_SAVER_HOLDING_VALUE],
                        STATE_SAVER_INDEX_PRICE: row[STATE_SAVER_INDEX_PRICE],
                        STATE_SAVER_UPDATED_ORDERS: row[STATE_SAVER_UPDATED_ORDERS],
                        STATE_SAVER_PLACED_ORDERS: row[STATE_SAVER_UPDATED_ORDERS]})

        return ret

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
            return BackTestResult('-1', '-1', '-1', '-1', '[]', '[]')

    def getMetrics(self):
        ''' read value for a col  '''
        d = {}
        if self.engine is None:
            return d

        conn = self.engine.connect()
        rows = conn.execute(select([SqlSaver.METRICS_TABLE]))

        for row in rows:
            d[row['metric']] = row['value']

        return d

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

    def writeMetrics(self, startDate, endDate, lowestValue, highestValue, sharpeRatio, maxDrawDown, rSquared, endValue, endHoldings):
        ''' write metrics '''
        self.__metrics.append({'metric': STATE_SAVER_METRICS_START_DATE, 'value': str(startDate)})
        self.__metrics.append({'metric': STATE_SAVER_METRICS_END_DATE, 'value': str(endDate)})
        self.__metrics.append({'metric': STATE_SAVER_METRICS_LOWEST_VALUE, 'value': str(lowestValue)})
        self.__metrics.append({'metric': STATE_SAVER_METRICS_HIGHEST_VALUE, 'value': str(highestValue)})
        self.__metrics.append({'metric': STATE_SAVER_METRICS_SHARPE_RATIO, 'value': str(sharpeRatio)})
        self.__metrics.append({'metric': STATE_SAVER_METRICS_MAX_DRAW_DOWN, 'value': str(maxDrawDown)})
        self.__metrics.append({'metric': STATE_SAVER_METRICS_R_SQUARED, 'value': str(rSquared)})
        self.__metrics.append({'metric': "endValue", 'value': str(endValue)})
        self.__metrics.append({'metric': "endHoldings", 'value': json.dumps(self.__convertHoldingsToList(endHoldings))})


    def __convertHoldingsToList(self, holding):
        ''' convert holding to dict'''
        ret = []
        for symbol, (share, price) in holding.items():
            if share <= 0:
                continue

            ret.append({"symbol": symbol,
                        "share": int(share),
                        "price": "%.2f" % price})

        return ret

    def commit(self):
        ''' complete write operation '''
        self.__resetResultTable()

        # write values
        updates = []
        for row, colValueDict in self.__writeCache.iteritems():
            if STATE_SAVER_ACCOUNT not in colValueDict or STATE_SAVER_INDEX_PRICE not in colValueDict:
                continue

            update = {'time': row}
            update.update(colValueDict)
            # fill column that are empty
            if STATE_SAVER_HOLDING_VALUE not in update:
                update[STATE_SAVER_HOLDING_VALUE] = ""
            if STATE_SAVER_PLACED_ORDERS not in update:
                update[STATE_SAVER_PLACED_ORDERS] = "[]"
            if STATE_SAVER_UPDATED_ORDERS not in update:
                update[STATE_SAVER_UPDATED_ORDERS] = "[]"

            # convert everything to string
            for key in update.keys():
                update[key] = str(update[key])

            updates.append(update)

        conn = self.engine.connect()
        conn.execute(SqlSaver.RESULT_TABLE.insert(), updates)

        if self.__metrics:
            self.__resetMetricsTable()
            conn.execute(SqlSaver.METRICS_TABLE.insert(), self.__metrics)
            self.__metrics = []
        LOG.info("committed table result at %s" % self.db)

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
    for i in range(2):
        s = SqlSaver()
        s.setup({'db': 'sqlite:////data/test_output' + str(i) + '.sqlite'})
        #h.resetCols(['accountValue', '1'])
        for i in range(5):
            s.write(123456, STATE_SAVER_HOLDING_VALUE, 10000)
            s.write(123456, STATE_SAVER_ACCOUNT, 12312312)
            s.write(123456, STATE_SAVER_INDEX_PRICE, 123123)

            s.writeMetrics(2010, 2013, 1, 100, 10, 0.1, 0.1, 123123, {})
            s.commit()

        print listTableNames("sqlite:////data/test_output" + str(i) + ".sqlite")
