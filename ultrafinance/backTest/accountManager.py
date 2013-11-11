'''
Created on Jan 29, 2011

@author: ppa
'''
from ultrafinance.backTest.account import Account
from ultrafinance.backTest.constant import STATE_SAVER_ACCOUNT, STATE_SAVER_HOLDING_VALUE

import copy

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
        self.__accountPositions = {}
        self.saver = None

    def createAccount(self, cash, commission = 0):
        ''' create account '''
        account = Account(cash, commission)
        self.__accounts[account.accountId] = account
        self.__accountPositions[account.accountId] = [] # list contains tuple (time, position)

        return account.accountId

    def getAccountCopy(self, accountId):
        ''' get shallow copy of an account '''
        return copy.copy(self.__accounts.get(accountId))

    def getAccount(self, accountId):
        ''' get account '''
        return self.__accounts.get(accountId)

    def getAccounts(self):
        ''' get accounts '''
        return self.__accounts.values()

    def updateAccountsPosition(self, tickDict):
        ''' update account position based on new tick '''
        curTime = tickDict.values()[0].time

        for accountId, account in self.__accounts.items():
            account.setLastTickDict(tickDict)
            position = account.getTotalValue()
            holdingValue = account.getHoldingValue()

            self.__accountPositions[accountId].append((curTime, position))
            #record
            if self.saver:
                self.saver.write(curTime, STATE_SAVER_ACCOUNT, position)
                self.saver.write(curTime, STATE_SAVER_HOLDING_VALUE, holdingValue)

            if position < 0:
                raise Exception("account %s value %s less than 0" % (accountId, position))

    def getAccountPostions(self, accountId):
        ''' get account positions '''
        return self.__accountPositions.get(accountId)
