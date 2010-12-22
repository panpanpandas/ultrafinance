'''
Created on Dec 18, 2010

@author: ppa
'''

from lib.YahooFinance import YahooFinance
from feeder.BaseFeeder import BaseFeeder

class YahooFinanceFeeder(BaseFeeder):
    '''
    feeder that get stock data from Yahoo Finance
    '''
    def __init__(self):
        ''' Constructor '''
        self.__yahooFinance = YahooFinance()
        self.__symbol = 'GOOG'
        
    def before(self):
        ''' init connection '''
        pass
    
    def after(self):
        ''' close connection '''
        pass
        
    def run(self, data):
        ''' preparing data'''
        print self.__yahooFinance.get_price(self.__symbol)
        return True