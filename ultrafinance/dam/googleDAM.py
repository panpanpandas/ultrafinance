'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.dam.googleFinance import GoogleFinance

import logging
LOG = logging.getLogger(__name__)

class GoogleDAM(BaseDAM):
    ''' Google DAO '''

    def __init__(self):
        ''' constructor '''
        super(GoogleDAM, self).__init__()
        self.__gf = GoogleFinance()

    def readQuotes(self, start, end):
        ''' read quotes from google Financial'''
        if self.__symbol is None:
            LOG.debug('Symbol is None')
            return []

        return self.__gf.getQuotes(self.__symbol, start, end)

    def readTicks(self, start, end):
        ''' read ticks from google Financial'''
        if self.__symbol is None:
            LOG.debug('Symbol is None')
            return []

        return self.__gf.getTicks(self.__symbol, start, end)
