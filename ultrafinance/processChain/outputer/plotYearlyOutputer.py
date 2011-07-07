'''
Created on Dec 18, 2010

@author: ppa
'''
from ultrafinance.processChain.baseModule import BaseModule
from ultrafinance.lib.plotDateValueDict import PlotDateValueDict

import logging
LOG = logging.getLogger(__name__)

class PlotYearlyOutputer(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' constructor '''
        super(PlotYearlyOutputer, self).__init__()

    def execute(self, dateValuesDict):
        ''' do output '''
        print 'dateValuesDict' + str(dateValuesDict)
        super(PlotYearlyOutputer, self).execute(input)
        p = PlotDateValueDict(dateValuesDict)
        p.plot()