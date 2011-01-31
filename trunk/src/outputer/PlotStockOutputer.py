'''
Created on Dec 18, 2010

@author: ppa
'''
from BaseModule import BaseModule
from matplotlib import pyplot
from datetime import datetime
#from operator import itemgetter
import pylab

class PlotStockOutputer(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' constructor '''
        super(PlotStockOutputer, self).__init__()
        
    def execute(self, dateValuesDict):
        ''' do output '''
        print 'dateValues'
        super(PlotStockOutputer, self).execute(input)
        fig = pylab.figure()
        ax = fig.gca()
 
        # Plotting here ...
        for dateValues in dateValuesDict.values():
            ax.plot_date([datetime.strptime(dateValue.date, '%Y-%m-%d') for dateValue in dateValues], \
                     [dateValue.adjClose for dateValue in dateValues], fmt='b-')
            pylab.grid()
            pyplot.show()