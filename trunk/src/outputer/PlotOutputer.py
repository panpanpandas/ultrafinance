'''
Created on Dec 18, 2010

@author: ppa
'''
from BaseModule import BaseModule
from matplotlib import pyplot
from datetime import datetime
#from operator import itemgetter
import pylab

class PlotOutputer(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' constructor '''
        super(PlotOutputer, self).__init__()
        
    def execute(self, dateValues):
        ''' do output '''
        print 'dateValues'
        print dateValues
        super(PlotOutputer, self).execute(input)
        fig = pylab.figure()
        ax = fig.gca()
 
        # Plotting here ...
        ax.plot_date([datetime.strptime(dateValue.date, '%Y-%m-%d') for dateValue in dateValues], \
                     [dateValue.adjClose for dateValue in dateValues], fmt='b-')
        pylab.grid()
        pyplot.show()