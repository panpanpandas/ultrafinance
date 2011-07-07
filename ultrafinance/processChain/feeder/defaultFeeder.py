'''
Created on Dec 18, 2010

@author: ppa
'''
from ultrafinance.processChain.baseModule import BaseModule

import logging
LOG = logging.getLogger(__name__)

class DefaultFeeder(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' Constructor '''
        super(DefaultFeeder, self).__init__()

    def execute(self, input):
        ''' preparing data'''
        super(DefaultFeeder, self).execute(input)
        data = {'defaultStock':('12/18/2010', '$20')}
        return data