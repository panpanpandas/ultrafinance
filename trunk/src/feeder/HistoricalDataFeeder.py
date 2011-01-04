'''
Created on Dec 18, 2010

@author: ppa
'''
from datetime import date

from lib.YahooFinance import YahooFinance
from BaseModule import BaseModule
from operator import itemgetter

class HistoricalDataFeeder(BaseModule):
    '''
    feeder that get stock data from Yahoo Finance
    '''
    def __init__(self):
        ''' Constructor '''
        super(HistoricalDataFeeder, self).__init__()
        self.__yahooFinance = YahooFinance()
        
    def execute(self, input):
        ''' preparing data'''
        super(HistoricalDataFeeder, self).execute(input)
        data = {}
        #print self.__yahooFinance.get_price(self.__symbol)
        values = self.__yahooFinance.get_historical_prices(input, '199000101', str(date.today()).replace('-', ''))
        for value in values[1:]:
            data[value[0]] = value[4]
        
        dateValues = sorted(data.items(), key=itemgetter(0))
        return dateValues