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
        
class ProcessingManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugin = import_class(os.getcwd() + '\\processing', app_global['processing'])
        
    def start(self):
        ''' start '''
        self.plugin().run({})
        print 'start processingManager'

class OutputManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugin = import_class(os.getcwd() + '\\output', app_global['output'])

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
        self.processingManager = ProcessingManager()
        self.outputManager = OutputManager()
        
    def start(self):
        ''' run function '''
        self.feederManager.start()
        self.processingManager.start()
        self.outputManager.start()
        print 'HAHAHA'

if __name__ == '__main__':
    ultraFinance = UltraFinance()
    ultraFinance.setup()
    ultraFinance.start()