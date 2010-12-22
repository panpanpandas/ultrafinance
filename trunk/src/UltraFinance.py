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
        print 'app_gloabl is ' + str(app_global)
        self.plugin = import_class(os.getcwd() + '\\feeder', app_global['feeder'])
        
    def start(self, input, data):
        ''' start '''
        print 'start feederManager'
        self.plugin().run(input, data)
        
class ProcessorManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugin = import_class(os.getcwd() + '\\processor', app_global['processor'])
        
    def start(self, input, data):
        ''' start '''
        print 'start processorManager'
        self.plugin().run(input, data)

class OutputerManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugin = import_class(os.getcwd() + '\\outputer', app_global['outputer'])

    def start(self, input, data):
        ''' start '''
        print 'start outputManager'
        self.plugin().run(input, data)

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
        feederInput = {'symbol': 'GOOG'}
        feederData = {}
        processorData = {}
        outputerData = {}
        self.feederManager.start(feederInput, feederData)
        self.processorManager.start(feederData, processorData)
        self.outputerManager.start(processorData, outputerData)
        print 'HAHAHA'

if __name__ == '__main__':
    ultraFinance = UltraFinance()
    ultraFinance.setup()
    ultraFinance.start()