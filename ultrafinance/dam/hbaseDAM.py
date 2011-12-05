'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.dam.hbaseLib import HBaseLib
from ultrafinance.model import TICK_FIELDS, QUOTE_FIELDS
from hbase.Hbase import Mutation, ColumnDescriptor

class HBaseDAM(BaseDAM):
    ''' HBase DAO '''
    QUOTE = 'quote'
    TICK = 'tick'

    def __init__(self, ip="localhost", port=9090):
        ''' constructor '''
        super(HBaseDAM, self).__init__()
        self.__hbase = HBaseLib(ip, port)

    def tableName(self, kind):
        return "%s-%s" % (self.symbol, kind)

    def __rowResultToQuote(self, row):
        ''' convert rowResult from Hbase to Quote'''
        keyValues = row.columns
        return Quote(*[keyValues["%s:%s" % (HBaseDAM.QUOTE, field)] for field in QUOTE_FIELDS])

    def __rowResultToTick(self, row):
        ''' convert rowResult from Hbase to Tick'''
        keyValues = row.columns
        return Tick(*[keyValues["%s:%s" % (HBaseDAM.TICK, field)] for field in TICK_FIELDS])

    def readQuotes(self, start, end):
        ''' read quotes '''
        rows = self.__hbase.scanTable(self.tableName(HBaseDAM.QUOTE), [HBaseDAM.QUOTE], start, end)

        return [self.__rowResultToQuote(row) for row in rows]

    def writeQuotes(self, quotes):
        ''' write quotes '''
        tName = self.tableName(HBaseDAM.QUOTE)
        if tName not in self.__hbase.getTableNames():
            self.__hbase.createTable(tName, [ColumnDescriptor(name=HBaseDAM.QUOTE, maxVersions=5)])

        for quote in quotes:
            self.__hbase.updateRow(self.tableName(HBaseDAM.QUOTE),
                                   quote.time,
                                   [Mutation(column = "%s:%s" % (HBaseDAM.QUOTE, field),
                                             value = getattr(quote, field) ) for field in QUOTE_FIELDS])

    def readTicks(self, start, end):
        ''' read ticks '''
        rows = self.__hbase.scanTable(self.tableName(HBaseDAM.TICK), [HBaseDAM.TICK], start, end)
        return [self.__rowResultToTick(row) for row in rows]

    def writeTicks(self, ticks):
        ''' read quotes '''
        tName = self.tableName(HBaseDAM.TICK)
        if tName not in self.__hbase.getTableNames():
            self.__hbase.createTable(tName, [ColumnDescriptor(name=HBaseDAM.TICK, maxVersions=5)])

        for tick in ticks:
            self.__hbase.updateRow(self.tableName(HBaseDAM.TICK),
                                   tick.time,
                                   [Mutation(column = "%s:%s" % (HBaseDAM.TICK, field),
                                             value = getattr(tick, field) ) for field in TICK_FIELDS])

if __name__ == '__main__':
    from ultrafinance.model import Quote, Tick
    dam = HBaseDAM()
    quotes = [Quote(*['1320676200', '32.59', '32.59', '32.58', '32.58', '65213', None]),
              Quote(*['1320676201', '32.60', '32.60', '32.59', '32.59', '65214', None])]
    ticks = [Tick(*['1320676200', '32.59', '32.59', '32.58', '32.58', '65213']),
              Tick(*['1320676201', '32.60', '32.60', '32.59', '32.59', '65214'])]

    dam.writeQuotes(quotes)
    dam.writeTicks(ticks)
    print dam.readQuotes("0", None)
    print dam.readTicks("0", "1320676201")
    print dam.readTicks("0", "1320676202")
