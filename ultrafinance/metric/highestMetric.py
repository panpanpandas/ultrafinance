'''
Created on Nov 7, 2011

@author: ppa
'''
import time

class HighestMetric:
    ''' Highest metric class '''

    def __init__(self):
        ''' constructor '''
        self.__highest = 0
        self.__time = None

    def getHighest(self):
        ''' get highest '''
        return self.__highest

    def record(self, account):
        ''' keep record of the account '''
        totalValue = account.getTotalValue()
        if totalValue > self.__highest:
            self.__highest = totalValue
            self.__time = time.ctime()

    def printResult(self):
        ''' print result '''
        print "Highest account value %.2f at %s" % (self.__highest, self.__time)
