'''
Created on Nov 6, 2011

@author: ppa
'''
import abc
import uuid

class TickSubsriber:
    ''' tick subscriber '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        ''' constructor '''
        self.__id = self.__generateId()
        self.__name = name

    def __generateId(self):
        ''' generate id '''
        return uuid.uuid4()

    def __getId(self):
        ''' get id '''
        return self.__id

    def __getName(self):
        ''' get name '''
        return self.__name

    @abc.abstractmethod
    def consume(self, ticks):
        ''' consume ticks '''
        return

    @abc.abstractmethod
    def subRules(self):
        ''' call back from framework
            return (symbolRe, rules)
        '''
        return

    subId = property(__getId)
    name = property(__getName)
