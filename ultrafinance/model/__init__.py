'''
Created on Nov 6, 2011

@author: ppa
'''
import json
from collections import namedtuple
from ultrafinance.lib.errors import UfException, Errors

# namedtuple are used to handle data getting from csv or internet
TICK_FIELDS = ['time', 'open', 'high', 'low', 'close', 'volume']
QUOTE_FIELDS = ['time', 'open', 'high', 'low', 'close', 'volume', 'adjClose']

Tick = namedtuple('Tick', ' '.join(TICK_FIELDS))
Quote = namedtuple('Quote', ' '.join(QUOTE_FIELDS))
DateValue = namedtuple('DateValue', 'date, value')

class Side(object):
    ''' side class '''
    SELL = 'sell'
    BUY = 'buy'

    @staticmethod
    def validate(side):
        if side not in [Side.BUY, Side.SELL]:
            raise UfException(Errors.SIDE_TYPE_ERROR, 'Side error: %s is not accepted' % side)

        return side

class Order(object):
    ''' order class'''
    OPEN = 'open'
    FILLED = 'filled'
    CANCELED = 'canceled'

    def __init__(self, accountId, side, symbol, price, share, orderId = None,
                 status = OPEN, filledTime = None, executedTime = None):
        ''' constructor '''
        self.__side = Side.validate(side)
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
        ''' get order ids '''
        return self.__orderId

    def getStatus(self):
        ''' get status '''
        return self.__status

    def getSide(self):
        ''' get side '''
        return self.__side

    def setSide(self, side):
        ''' set side '''
        self.__side = Side.validate(side)

    def __str__(self):
        ''' override buildin function '''
        return json.dumps({'accountId': str(self.accountId), 'side': self.__side, 'symbol': self.symbol, 'price': self.price,
                           'orderId': str(self.orderId), 'status': self.status})

    side = property(getSide, setSide)
    orderId = property(getOrderId, setOrderId)
    status = property(getStatus, setStatus)