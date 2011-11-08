'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.model import Side
from ultrafinance.lib.errors import Errors, UfException
import uuid

import logging
LOG = logging.getLogger(__name__)

class Account:
    ''' account '''

    def __init__(self, name):
        ''' constructor '''
        self.__id = self.__generateId()
        self.__name = name
        self.__holdings = {}
        self.__cash = 0.0
        self.__lastTransition = None

    def __generateId(self):
        ''' generate id '''
        return uuid.uuid4()

    def __addHolding(self, symbol, share, price):
        ''' add holding '''
        if symbol not in self.__holdings:
            self.__hodlings[symbol] = [share, price]

        else:
            preShare, prePrice = self.__holdings[symbol]
            preValue = preShare * prePrice
            curShare = share + preShare
            curPrice = (share * price + preValue) / curShare
            self.__holdings[symbol] = [curShare, curPrice]

    def __reduceHolding(self, symbol, share):
        ''' reduce holding '''
        preShare, prePrice = self.__holdings[symbol]
        curShare = preShare - share
        self.__holdings[symbol] = [curShare, prePrice]

    def execute(self, transition):
        ''' execute transition'''
        if not self.validate(transition):
            raise UfException(Errors.TRANSITION_INVALID_ERROR,
                              ''' Transition is invalid: symbol %s, share %s, price %s'''\
                              % (transition.symbol, transition.share, transition.price) )

        value = self.__getTransitionValue(transition)
        if Side.BUY == transition.side:
            self.__cash = self.__cash - value - transition.fee
            self.__addHolding(transition.symbol, transition.share, transition.price)
        else:
            self.__cash = self.__cash + value - transition.fee
            self.__reduceHoding(transition.symbol, transition.share)

        self.__lastTransition = transition


    def validate(self, transition):
        ''' validate transition to check whether it's doable or not '''
        value = self.__getTransitionValue(transition)
        cost = value + transition.fee

        if Side.BUY == transition.side:
            if cost <= self.__cash:
                return True
            else:
                LOG.error('Transition fails validation: cash %.2f is smaller than cost %.2f' % (self.__cash, cost))
                return False
        else:
            if transition.symbol not in self.__holdings:
                LOG.error('Transition fails validation: symbol %s not in holdings' % transition.symbol)
                return False
            if transition.share < self.__holdings[transition.symbol]:
                LOG.error('Transition fails validation: share %s is not enough as %s' % (transition.share, self.__holdings[transition.symbol]) )
                return False
            if transition.fee < self.__cash:
                LOG.error('Transition fails validation: cash %s is not enough for trans fee %s' % (self.__cash, transition.fee) )
                return False
            else:
                return True

    def getCash(self):
        ''' get cash '''
        return self.__cash

    def getHoldingValue(self):
        ''' get value of holdings '''
        value = 0.0
        for share, price in self.__holdings.values():
            value += share * price

        return value

    def getTotalValue(self):
        ''' get total value '''
        return self.getCash() + self.getHoldingValue()

    def __getTransitionValue(self, transition):
        ''' get value of transition '''
        return transition.price * transition.share

    def __getId(self):
        ''' get id '''
        return self.__id

    def __getHoldings(self):
        ''' get holding'''
        return self.__holdings

    def __getLastTransition(self):
        ''' get last transition '''
        return self.__lastTransition

    accountId = property(__getId)
    holdings = property(__getHoldings)
    cash = property(getCash)
    lastTransition = property(__getLastTransition)