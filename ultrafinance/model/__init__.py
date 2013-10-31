'''
Created on Nov 6, 2011

@author: ppa
'''
import json
from collections import namedtuple
from ultrafinance.lib.errors import UfException, Errors

# namedtuple are used to handle data getting from csv or internet
TICK_FIELDS = ['time', 'open', 'high', 'low', 'close', 'volume']
#QUOTE_FIELDS = ['time', 'open', 'high', 'low', 'close', 'volume', 'adjClose']
QUOTE_FIELDS = ['time', 'close', 'volume', 'low', 'high']

class Tick(object):
    ''' tick class '''
    def __init__(self, time, open, high, low, close, volume):
        ''' constructor '''
        self.time = time
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = int(volume)

    def __str__(self):
        ''' convert to string '''
        return json.dumps({"time": self.time,
                           "open": self.open,
                           "high": self.high,
                           "low": self.low,
                           "close": self.close,
                           "volume": self.volume})

    @staticmethod
    def fromStr(string):
        ''' convert from string'''
        d = json.loads(string)
        return Tick(d['time'], d['open'], d['high'],
                    d['low'], d['close'], d['volume'], d['adjClose'])

"""
class Quote(object):
    ''' tick class '''
    def __init__(self, time, open, high, low, close, volume, adjClose):
        ''' constructor '''
        self.time = time
        self.close = float(close)

    def __str__(self):
        ''' convert to string '''
        return json.dumps({"time": self.time,
                           "close": self.close})

    @staticmethod
    def fromStr(string):
        ''' convert from string'''
        d = json.loads(string)
        return Quote(d['time'], d.get('open'), d.get('high'),
                     d.get('low'), d['close'], d.get('volume'), d.get('adjClose'))

"""
class Quote(object):
    ''' tick class '''
    def __init__(self, time, open, high, low, close, volume, adjClose):
        ''' constructor '''
        self.time = time
        self.open = 0 if ("-" == open) else float(open)
        self.high = 0 if ("-" == high) else float(high)
        self.low = 0 if ("-" == low) else float(low)
        self.close = 0 if ("-" == close) else float(close)
        self.volume = int(volume)
        self.adjClose = adjClose

    def __str__(self):
        ''' convert to string '''
        return json.dumps({"time": self.time,
                           "open": self.open,
                           "high": self.high,
                           "low": self.low,
                           "close": self.close,
                           "volume": self.volume,
                           "adjClose": self.adjClose})

    @staticmethod
    def fromStr(string):
        ''' convert from string'''
        d = json.loads(string)
        return Quote(d['time'], d['open'], d['high'],
                     d['low'], d['close'], d['volume'], d['adjClose'])

#Tick = namedtuple('Tick', ' '.join(TICK_FIELDS))
TupleQuote = namedtuple('Quote', ' '.join(QUOTE_FIELDS))
#DateValue = namedtuple('DateValue', 'date, value')

class Action(object):
    ''' action class '''
    SELL = 'sell'
    BUY = 'buy'
    SELL_SHORT = 'sell_short'
    BUY_TO_COVER = 'buy_to_cover'

    @staticmethod
    def validate(action):
        if action not in [Action.BUY, Action.SELL, Action.SELL_SHORT, Action.BUY_TO_COVER]:
            raise UfException(Errors.SIDE_TYPE_ERROR, 'Action error: %s is not accepted' % action)

        return action


class Type(object):
    ''' type class '''
    MARKET = 'market'
    STOP = 'stop'
    LIMIT = 'limit' # not support yet

    @staticmethod
    def validate(type):
        if type not in [Type.MARKET, Type.STOP, Type.LIMIT]:
            raise UfException(Errors.SIDE_TYPE_ERROR, 'Type error: %s is not accepted' % type)

        return type


class Order(object):
    ''' order class'''
    OPEN = 'open'
    FILLED = 'filled'
    CANCELED = 'canceled'

    def __init__(self, accountId, action, type, symbol, share, price = None, orderId = None,
                 status = OPEN, filledTime = None, executedTime = None):
        ''' constructor '''
        self.__action = Action.validate(action)
        self.__type = Type.validate(type)
        self.__orderId = None
        self.__status = None
        self.accountId = accountId
        self.symbol = symbol
        self.price = price
        self.share = share
        self.filledTime = filledTime
        self.executedTime = executedTime

        self.setOrderId(orderId)
        self.setStatus(status)

    def setStatus(self, status):
        ''' set status '''
        if status not in [Order.OPEN, Order.FILLED, Order.CANCELED]:
            raise UfException(Errors.ORDER_TYPE_ERROR, 'Order status error: %s is not accepted' % status)

        self.__status = status

    def setOrderId(self, orderId):
        ''' set order id, should be only set once '''
        if self.__orderId is not None:
            raise UfException(Errors.ORDER_TYPE_ERROR, 'OrderId already set: %s' % self.orderId)

        self.__orderId = orderId

    def getOrderId(self):
        ''' get order id '''
        return self.__orderId

    def getStatus(self):
        ''' get status '''
        return self.__status

    def getAction(self):
        ''' get action '''
        return self.__action

    def setAction(self, action):
        ''' set action '''
        self.__side = Action.validate(action)

    def getType(self):
        ''' get type '''
        return self.__type

    def setType(self, type):
        ''' set action '''
        self.__side = Type.validate(type)

    def __str__(self):
        ''' override buildin function '''
        return json.dumps({'accountId': str(self.accountId), 'action': self.__action, 'type': self.__type, 'symbol': self.symbol,
                           'price': self.price, 'share': self.share, 'orderId': str(self.orderId), 'status': self.status})

    @staticmethod
    def fromStr(string):
        ''' convert from string'''
        d = json.loads(string)
        return Order(d['accountId'], d['action'], d['type'], d['symbol'], d['share'], d.get('price'),
                     d.get('orderId'), d.get('status'), d.get('filledTime'), d.get('executedTime'))


    type = property(getType, setType)
    action = property(getAction, setAction)
    orderId = property(getOrderId, setOrderId)
    status = property(getStatus, setStatus)
