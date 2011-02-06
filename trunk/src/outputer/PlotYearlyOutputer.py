'''
Created on Dec 18, 2010

@author: ppa
'''
from BaseModule import BaseModule
from lib.PlotDateValueDict import PlotDateValueDict
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