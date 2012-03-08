'''
Created on Nov 9, 2011

@author: ppa
'''
import abc
from ultrafinance.lib.errors import UfException, Errors

class BaseDAM(object):
    ''' base class for DAO '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        ''' constructor '''
        self.__symbol = None

    def readQuotes(self, start, end):
        ''' read quotes '''
        raise UfException(Errors.UNDEFINED_METHOD, "readQuotes method is not defined")

    def writeQuotes(self, quotes):
        ''' write quotes '''
        raise UfException(Errors.UNDEFINED_METHOD, "writeQuotes method is not defined")

    def readTicks(self, start, end):
        ''' read ticks '''
        raise UfException(Errors.UNDEFINED_METHOD, "readTicks method is not defined")

    def writeTicks(self, ticks):
        ''' read quotes '''
        raise UfException(Errors.UNDEFINED_METHOD, "writeTicks method is not defined")

    def setSymbol(self, symbol):
        ''' set symbol '''
        self.__symbol = symbol

    def __getSymbol(self):
        ''' get symbol '''
        return self.__symbol

    def setup(self, settings):
        ''' setup dam '''
        pass

    def commit(self):
        ''' commit write changes '''
        pass

    symbol = property(__getSymbol, setSymbol)
