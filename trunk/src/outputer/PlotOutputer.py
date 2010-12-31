'''
Created on Dec 18, 2010

@author: ppa
'''
from BaseModule import BaseModule
from matplotlib import pyplot
from datetime import datetime
import pylab

class PlotOutputer(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' constructor '''
        super(PlotOutputer, self).__init__()
        
    def execute(self, input):
        ''' do output '''
        super(PlotOutputer, self).execute(input)
        fig = pylab.figure()
        ax = fig.gca()
 
        # Plotting here ...
        ax.plot_date([datetime.strptime(date, '%Y-%m-%d') for date in input.keys()], input.values(), fmt='bo')
        pyplot.show()
        return None