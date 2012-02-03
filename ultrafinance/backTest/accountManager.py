'''
Created on Jan 29, 2011

@author: ppa
'''
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.account import Account
from ultrafinance.backTest.metric.metricFactory import MetricFactory
import re

import logging
LOG = logging.getLogger()

class AccountManager(object):
    '''
    account manager
    Note: set metricNames before creating accounts
    '''
    def __init__(self):
        ''' constructor '''
        self.__accounts = {}
        self.__metrix = {}
        self.saver = None

    def createAccountWithMetrix(self, metricNames, cash, commission = 0):
        ''' create account '''
        account = Account(cash, commission)
        self.__accounts[account.accountId] = account

        self.__metrix[account.accountId] = []
        for metricName in metricNames:
            metric = MetricFactory.createMetric(metricName)
            metric.setAccount(account)
            self.__metrix[account.accountId].append(metric)

        return account.accountId

    def getAccount(self, accountId):
        ''' get account '''
        return self.__accounts.get(accountId)

    def getAccounts(self, expression):
        ''' get accounts '''
        accounts = []
        pair = re.compile(expression)

        for accountId, account in self.__accounts.items():
            if pair.match(str(accountId)):
                accounts.append(account)

        return accounts

    def updateAccountsWithTickDict(self, tickDict):
        ''' calculate metrix for each account '''
        curTime = tickDict.values()[0].time

        for accountId, metrix in self.__metrix.items():
            account = self.getAccount(accountId)
            account.setLastTickDict(tickDict)

            for metric in metrix:
                metric.record(curTime)

            #record
            if self.saver:
                self.saver.write(curTime, "account-%s" % accountId, account.getTotalValue())

    def getMetrix(self):
        ''' get metrix '''
        return self.__metrix
