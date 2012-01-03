'''
Created on Dec 18, 2010

@author: ppa
'''
from ultrafinance.processChain.baseModule import BaseModule
from matplotlib import pyplot
from datetime import datetime
import pylab

import logging
LOG = logging.getLogger(__name__)

class PlotStockOutputer(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' constructor '''
        super(PlotStockOutputer, self).__init__()

    def execute(self, dateValuesDict):
        ''' do output '''
        super(PlotStockOutputer, self).execute(input)
        #pyplot.ion() # turns interactive mode on
        fig = pylab.figure()
        ax = fig.gca()

        # Plotting here ...
        for dateValues in dateValuesDict.values():
            ax.plot_date([datetime.strptime(dateValue.date, '%Y-%m-%d') for dateValue in dateValues],
                         [dateValue.adjClose for dateValue in dateValues], fmt='b-')
            pylab.grid()
            pyplot.show()