'''
Created on Nov 7, 2011

@author: ppa
'''

class MetricManager:
    ''' metric manger'''

    def __init__(self):
        ''' constructor '''
        self.__metrics = {} # id: subscriber

    def getMetricById(self, subId):
        ''' get subscriber by Id '''
        return self.__subs.get(subId)

    def getMetrixbyName(self, name):
        ''' get subscribers by name '''
        subs = []

        for sub in self.__subs:
            if name == sub.name:
                subs.append(sub)

        return subs

    def addMetric(self, sub):
        ''' add subscriber '''
        if sub.subId not in self.__subs:
            self.__subs[sub.subId] = sub
