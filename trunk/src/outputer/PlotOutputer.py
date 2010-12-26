'''
Created on Dec 18, 2010

@author: ppa
'''
from outputer.BaseOutputer import BaseOutputer
from matplotlib import pyplot
from datetime import datetime
import pylab

class PlotOutputer(BaseOutputer):
    ''' Default feeder '''
    def before(self):
        ''' init output '''
        print 'before output'
        
    def after(self):
        ''' close output '''
        print 'after output'
        
    def run(self, input, data):
        ''' do output '''
        fig = pylab.figure()
        ax = fig.gca()
 
        # Plotting here ...
        ax.plot_date([datetime.strptime(date, '%Y-%m-%d') for date in input.keys()], input.values(), fmt='bo')
        pyplot.show()