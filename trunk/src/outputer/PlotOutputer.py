'''
Created on Dec 18, 2010

@author: ppa
'''
from BaseModule import BaseModule
from matplotlib import pyplot
from datetime import datetime
from operator import itemgetter
import pylab

class PlotOutputer(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' constructor '''
        super(PlotOutputer, self).__init__()
        
    def execute(self, input):
        ''' do output '''
        dateValues = sorted(input.items(), key=itemgetter(0))
        super(PlotOutputer, self).execute(input)
        fig = pylab.figure()
        ax = fig.gca()
 
        # Plotting here ...
        ax.plot_date([datetime.strptime(dateValue[0], '%Y-%m-%d') for dateValue in dateValues], \
                     [dateValue[1] for dateValue in dateValues], fmt='b-')
        pyplot.show()