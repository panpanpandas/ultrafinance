'''
Created on Nov 6, 2011

@author: ppa
'''
import uuid

class Account:
    ''' account '''

    def __init__(self, name):
        ''' constructor '''
        self.__id = self.__generateId()
        self.__name = name
        self.__holdings = {}
        self.__cash = 0.0

    def __generateId(self):
        ''' generate id '''
        return uuid.uuid4()

    def __getId(self):
        ''' get id '''
        return self.__id

    accountId = property(__getId)
