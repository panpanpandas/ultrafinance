'''
Created on Nov 6, 2011

@author: ppa
'''

class SubManager:
    ''' subscriber manger'''

    def __init__(self):
        ''' constructor '''
        self.__subs = {} # id: subscriber

    def getSubById(self, subId):
        ''' get subscriber by Id '''
        return self.__subs.get(subId)

    def getSubsbyName(self, name):
        ''' get subscribers by name '''
        subs = []

        for sub in self.__subs:
            if name == sub.name:
                subs.append(sub)

        return subs

    def addSub(self, sub):
        ''' add subscriber '''
        if sub.subId not in self.__subs:
            self.__subs[sub.subId] = sub
