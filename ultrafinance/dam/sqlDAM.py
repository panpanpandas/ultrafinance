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
        self.time = int(time)
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = int(volume)
        self.adjClose = float(adjClose) if adjClose else None

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
        self.time = int(time)
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = int(volume)

    def __repr__(self):
        return "<Tick('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
           % (self.symbol, self.time, self.open, self.high, self.low, self.close, self.volume)

class SqlDAM(BaseDAM):
    ''' SQL DAO '''

    def __init__(self, db = 'sqlite:////tmp/sqldam.sqlite', echo = False):
        ''' constructor '''
        super(SqlDAM, self).__init__()
        self.engine = create_engine(db, echo = echo)
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
        Base.metadata.create_all(self.engine)
        self.session.add_all([self.__quoteToSql(quote) for quote in quotes])

    def writeTicks(self, ticks):
        ''' write ticks '''
        Base.metadata.create_all(self.engine)
        self.session.add_all([self.__tickToSql(tick) for tick in ticks])


if __name__ == '__main__':
    dam = SqlDAM(echo = False)
    dam.setSymbol("test")

    quotes = [Quote(*['1320676200', '32.59', '32.59', '32.58', '32.58', '65213', None]),
              Quote(*['1320676201', '32.60', '32.60', '32.59', '32.59', '65214', None])]
    ticks = [Tick(*['1320676200', '32.59', '32.59', '32.58', '32.58', '65213']),
              Tick(*['1320676201', '32.60', '32.60', '32.59', '32.59', '65214'])]

    dam.writeQuotes(quotes)
    dam.writeTicks(ticks)
    print [str(quote) for quote in dam.readQuotes("0", None) ]
    print [str(tick) for tick in dam.readTicks("0", "1320676201")]
    print [str(tick) for tick in dam.readTicks("0", "1320676202")]
