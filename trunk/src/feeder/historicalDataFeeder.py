'''
Created on Dec 18, 2010

@author: ppa
'''
from datetime import date

from lib.YahooFinance import YahooFinance
from feeder.BaseFeeder import BaseFeeder

class historicalDataFeeder(BaseFeeder):
    '''
    feeder that get stock data from Yahoo Finance
    '''
    def __init__(self):
        ''' Constructor '''
        self.__yahooFinance = YahooFinance()
        
    def before(self):
        ''' init connection '''
        pass
    
    def after(self):
        ''' close connection '''
        pass
        
    def run(self, input, data):
        ''' preparing data'''
        #print self.__yahooFinance.get_price(self.__symbol)
        values = self.__yahooFinance.get_historical_prices(input['symbol'], '199000101', str(date.today()).replace('-', ''))
        for value in values[1:]:
            data[value[0]] = value[4]