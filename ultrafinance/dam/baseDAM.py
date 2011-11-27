'''
Created on Nov 9, 2011

@author: ppa
'''
import abc

class BaseDAM:
    ''' base class for DAO '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        ''' constructor '''
        self.__symbol = None

    @abc.abstractmethod
    def readQuotes(self, start, end):
        ''' read quotes '''
        return

    @abc.abstractmethod
    def writeQuotes(self, quotes):
        ''' write quotes '''
        return

    @abc.abstractmethod
    def readTicks(self, start, end):
        ''' read ticks '''
        return

    @abc.abstractmethod
    def writeTicks(self, ticks):
        ''' read quotes '''
        return

    def setSymbol(self, symbol):
        ''' set symbol '''
        self.__symbol = symbol

    def __getSymbol(self):
        ''' get symbol '''
        return self.__symbol

    symbol = property(__getSymbol, setSymbol)