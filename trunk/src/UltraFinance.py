'''
Created on Dec 18, 2010

@author: ppa
'''
import os
from util import import_class
from Configuration import app_global

class FeederManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        print app_global
        self.plugin = import_class(os.getcwd() + '\\feeder', app_global['feeder'])
        
    def start(self):
        ''' start '''
        self.plugin().run({})
        print 'start feederManager'
        
class ProcessorManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugin = import_class(os.getcwd() + '\\processor', app_global['processor'])
        
    def start(self):
        ''' start '''
        self.plugin().run({})
        print 'start processorManager'

class OutputerManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugin = import_class(os.getcwd() + '\\outputer', app_global['outputer'])

    def start(self):
        ''' start '''
        self.plugin().run({})
        print 'start outputManager'

class UltraFinance():
    ''' base class for ultraFinance'''
    def __init__(self):
        ''' constructor '''
        pass
    
    def setup(self):
        ''' setup feeder, output and processing plugins '''
        self.feederManager = FeederManager()
        self.processorManager = ProcessorManager()
        self.outputerManager = OutputerManager()
        
    def start(self):
        ''' run function '''
        self.feederManager.start()
        self.processorManager.start()
        self.outputerManager.start()
        print 'HAHAHA'

if __name__ == '__main__':
    ultraFinance = UltraFinance()
    ultraFinance.setup()
    ultraFinance.start()