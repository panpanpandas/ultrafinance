'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.model import Quote, Tick
import sys

from sqlalchemy import Column, Integer, String, Float, Sequence, create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QuoteSql(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    symbol = Column(String(12))
    time = Column(Integer)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(String(12))
    adjClose = Column(String(12))

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
    volume = Column(String(12))

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
    ''' SQL DAO '''

    def __init__(self, echo = False):
        ''' constructor '''
        super(SqlDAM, self).__init__()
        self.echo = echo
        self.db = None
        self.session = None
        self.engine = None
        self.first = True

    def setup(self, setting):
        ''' set up '''
        if 'db' in setting:
            self.setDb(setting['db'])

    def setDb(self, db):
        self.db = db
        self.engine = create_engine(db, echo = self.echo)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()

    def __sqlToQuote(self, row):
        ''' convert row result to Quote '''
        return Quote(row.time, row.open, row.high, row.low, row.close, row.volume, row.adjClose)

    def __sqlToTick(self, row):
        ''' convert row result to Tick '''
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
        rows = self.session.query(QuoteSql).filter(and_(QuoteSql.symbol == self.symbol,
                                                        QuoteSql.time >= int(start),
                                                        QuoteSql.time < int(end)))

        return [self.__sqlToQuote(row) for row in rows]

    def readTicks(self, start, end):
        ''' read ticks '''
        if end is None:
            end = sys.maxint
        rows = self.session.query(TickSql).filter(and_(TickSql.symbol == self.symbol,
                                                       TickSql.time >= int(start),
                                                       TickSql.time < int(end)))

        return [self.__sqlToTick(row) for row in rows]

    def writeQuotes(self, quotes):
        ''' write quotes '''
        if self.first:
            Base.metadata.create_all(self.engine, checkfirst = True)
            self.first = False

        self.session.add_all([self.__quoteToSql(quote) for quote in quotes])

    def writeTicks(self, ticks):
        ''' write ticks '''
        if self.first:
            Base.metadata.create_all(self.engine, checkfirst = True)
            self.first = False

        self.session.add_all([self.__tickToSql(tick) for tick in ticks])

    def commit(self):
        ''' commit changes '''
        self.session.commit()
