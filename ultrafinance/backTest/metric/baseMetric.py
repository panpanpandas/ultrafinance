'''
Created on Nov 7, 2011

@author: ppa
'''
import abc
from ultrafinance.lib.errors import Errors, UfException

class BaseMetric(object):
    ''' base metric class '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        ''' constructor '''
        self.account = None

    def setAccount(self, account):
        ''' set account '''
        if not self.account:
            self.account = account
        else:
            raise UfException(Errors.ACCOUNT_ALEADY_SET,
                              "account should only be set once")

    def record(self, curTime):
        ''' keep record of the account '''
        return

    @abc.abstractmethod
    def printResult(self):
        ''' print result '''
        return


