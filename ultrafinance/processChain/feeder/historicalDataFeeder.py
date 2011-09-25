'''
Created on Dec 18, 2010

@author: ppa
'''
from datetime import date

from ultrafinance.lib.yahooFinance import YahooFinance
from ultrafinance.processChain.baseModule import BaseModule

import logging
LOG = logging.getLogger(__name__)

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
        return {'history stock': self.__yahooFinance.getHistoricalPrices(input, '1990-01-01', date.today())}