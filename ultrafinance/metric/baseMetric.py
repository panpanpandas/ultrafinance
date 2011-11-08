'''
Created on Nov 7, 2011

@author: ppa
'''
import abc

class BaseMetric:
    ''' base metric class '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def record(self, account):
        ''' keep record of the account '''
        return

    @abc.abstractmethod
    def printResult(self):
        ''' print result '''
        return
