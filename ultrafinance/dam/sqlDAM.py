'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.model import Quote, Tick, TupleQuote
from ultrafinance.lib.util import splitListEqually
import sys

from sqlalchemy import Column, Integer, String, Float, Sequence, create_engine, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import time

Base = declarative_base()

import logging
LOG = logging.getLogger()

class FmSql(Base):
    __tablename__ = 'fundamental'

    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    symbol = Column(String(12))
    field = Column(String(50))
    timeStamp = Column(String(50))
    value = Column(Float)

    def __init__(self, symbol, field, timeStamp, value):
        ''' constructor '''
        self.symbol = symbol
        self.field = field
        self.timeStamp = timeStamp
        self.value = value

    def __repr__(self):
        return "<Fundamentals('%s', '%s', '%s', '%s')>" \
           % (self.symbol, self.field, self.timeStamp, self.value)

class QuoteSql(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    symbol = Column(String(12))
    time = Column(Integer)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    adjClose = Column(Float)

    def __init__(self, symbol, time, open, high, low, close, volume, adjClose):
        ''' constructor '''
        self.symbol = symbol
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adjClose = adjClose

    def __repr__(self):
        return "<Quote('%s', '%s','%s', '%s', '%s','%s', '%s', '%s')>" \
           % (self.symbol, self.time, self.open, self.high, self.low, self.close, self.volume, self.adjClose)

class TickSql(Base):
    __tablename__ = 'ticks'

    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    symbol = Column(String(12))
    time = Column(Integer)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

    def __init__(self, symbol, time, open, high, low, close, volume):
        ''' constructor '''
        self.symbol = symbol
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __repr__(self):
        return "<Tick('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
           % (self.symbol, self.time, self.open, self.high, self.low, self.close, self.volume)

class SqlDAM(BaseDAM):
    '''
    SQL DAM
    '''
    def __init__(self, echo = False):
        ''' constructor '''
        super(SqlDAM, self).__init__()
        self.echo = echo
        self.first = True
        self.engine = None
        self.ReadSession = None
        self.WriteSession = None
        self.writeSession = None


    def setup(self, setting):
        ''' set up '''
        if 'db' not in setting:
            raise Exception("db not specified in setting")

        self.engine = create_engine(setting['db'], echo = self.echo)

    def getReadSession(self):
        ''' return scopted session '''
        if self.ReadSession is None:
            self.ReadSession = scoped_session(sessionmaker(bind = self.engine))

        return self.ReadSession

    def getWriteSession(self):
        ''' return unscope session, TODO, make it clear '''
        if self.WriteSession is None:
            self.WriteSession = sessionmaker(bind = self.engine)
            self.writeSession = self.WriteSession()

        return self.writeSession

    def __sqlToQuote(self, row):
        ''' convert row result to Quote '''
        return Quote(row.time, row.open, row.high, row.low, row.close, row.volume, row.adjClose)

    def __sqlToTupleQuote(self, row):
        ''' convert row result to tuple Quote '''
        #return TupleQuote(row.time, row.open, row.high, row.low, row.close, row.volume, row.adjClose)
        #TODO -- remove type conversion, crawler should get the right type
        return TupleQuote(row.time, row.close, int(row.volume), row.low, row.high)

    def __sqlToTick(self, row):
        ''' convert row result to Tick '''
        return Tick(row.time, row.open, row.high, row.low, row.close, row.volume)

    def __sqlToTupleTick(self, row):
        ''' convert row result to tuple Tick '''
        return Tick(row.time, row.open, row.high, row.low, row.close, row.volume)

    def __tickToSql(self, tick):
        ''' convert tick to TickSql '''
        return TickSql(self.symbol, tick.time, tick.open, tick.high, tick.low, tick.close, tick.volume)

    def __quoteToSql(self, quote):
        ''' convert tick to QuoteSql '''
        return QuoteSql(self.symbol, quote.time, quote.open, quote.high, quote.low, quote.close, quote.volume, quote.adjClose)

    def readQuotes(self, start, end):
        ''' read quotes '''
        if end is None:
            end = sys.maxint

        session = self.getReadSession()()
        try:
            rows = session.query(QuoteSql).filter(and_(QuoteSql.symbol == self.symbol,
                                                            QuoteSql.time >= int(start),
                                                            QuoteSql.time < int(end)))
        finally:
            self.getReadSession.remove()

        return [self.__sqlToQuote(row) for row in rows]

    def readTupleQuotes(self, start, end):
        ''' read quotes as tuple '''
        if end is None:
            end = sys.maxint

        session = self.getReadSession()()
        try:
            rows = session.query(QuoteSql).filter(and_(QuoteSql.symbol == self.symbol,
                                                       QuoteSql.time >= int(start),
                                                       QuoteSql.time < int(end)))
        finally:
            self.getReadSession().remove()

        return [self.__sqlToTupleQuote(row) for row in rows]

    def readBatchTupleQuotes(self, symbols, start, end):
        '''
        read batch quotes as tuple to save memory
        '''
        if end is None:
            end = sys.maxint

        ret = {}
        session = self.getReadSession()()
        try:
            symbolChunks = splitListEqually(symbols, 100)
            for chunk in symbolChunks:
                rows = session.query(QuoteSql.symbol, QuoteSql.time, QuoteSql.close, QuoteSql.volume,
                                     QuoteSql.low, QuoteSql.high).filter(and_(QuoteSql.symbol.in_(chunk),
                                                                              QuoteSql.time >= int(start),
                                                                              QuoteSql.time < int(end)))

                for row in rows:
                    if row.time not in ret:
                        ret[row.time] = {}

                    ret[row.time][row.symbol] = self.__sqlToTupleQuote(row)
        finally:
            self.getReadSession().remove()

        return ret


    def readTupleTicks(self, start, end):
        ''' read ticks as tuple '''
        if end is None:
            end = sys.maxint

        session = self.getReadSession()()
        try:
            rows = session.query(TickSql).filter(and_(TickSql.symbol == self.symbol,
                                                      TickSql.time >= int(start),
                                                      TickSql.time < int(end)))
        finally:
            self.getReadSession().remove()

        return [self.__sqlToTupleTick(row) for row in rows]

    def readTicks(self, start, end):
        ''' read ticks '''
        if end is None:
            end = sys.maxint

        session = self.getReadSession()()
        try:
            rows = session.query(TickSql).filter(and_(TickSql.symbol == self.symbol,
                                                      TickSql.time >= int(start),
                                                      TickSql.time < int(end)))
        finally:
            self.getReadSession().remove()

        return [self.__sqlToTick(row) for row in rows]

    def writeQuotes(self, quotes):
        ''' write quotes '''
        if self.first:
            Base.metadata.create_all(self.engine, checkfirst = True)
            self.first = False

        session = self.getWriteSession()
        session.add_all([self.__quoteToSql(quote) for quote in quotes])


    def writeTicks(self, ticks):
        ''' write ticks '''
        if self.first:
            Base.metadata.create_all(self.engine, checkfirst = True)
            self.first = False

        session = self.getWriteSession()
        session.add_all([self.__tickToSql(tick) for tick in ticks])

    def commit(self):
        ''' commit changes '''
        session = self.getWriteSession()
        session.commit()

    def destruct(self):
        ''' destructor '''
        if self.getWriteSession():
            self.WriteSession.remove()
            self.WriteSession = None
            self.writeSession = None
        if self.getReadSession():
            self.getReadSession().remove()
            self.ReadSession = None


    '''
    read/write fundamentals
    TODO: when doing fundamentals and quote/tick operation together,
    things may mess up
    '''
    def writeFundamental(self, keyTimeValueDict):
        ''' write fundamental '''
        if self.first:
            Base.metadata.create_all(self.__getEngine(), checkfirst = True)
            self.first = False

        sqls = self._fundamentalToSqls(keyTimeValueDict)
        session = self.Session()
        try:
            session.add_all(sqls)
        finally:
            self.Session.remove()

    def readFundamental(self):
        ''' read fundamental '''
        rows = self.__getSession().query(FmSql).filter(and_(FmSql.symbol == self.symbol))
        return self._sqlToFundamental(rows)

    def _sqlToFundamental(self, rows):
        keyTimeValueDict = {}
        for row in rows:
            if row.field not in keyTimeValueDict:
                keyTimeValueDict[row.field] = {}

            keyTimeValueDict[row.field][row.timeStamp] = row.value

        return keyTimeValueDict

    def _fundamentalToSqls(self, keyTimeValueDict):
        ''' convert fundament dict to sqls '''
        sqls = []
        for key, timeValues in keyTimeValueDict.iteritems():
            for timeStamp, value in timeValues.iteritems():
                sqls.append(FmSql(self.symbol, key, timeStamp, value))

        return sqls
