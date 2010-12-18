'''
Created on Dec 18, 2010

@author: ppa
'''
from feeder.DefaultFeeder import DefaultFeeder
from processing.DefaultProcessing import DefaultProcessing
from output.DefaultOutput import DefaultOutput

class FeederManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugins = []
        
    def start(self):
        ''' start '''
        print 'start feederManager'
        
class ProcessingManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugins = []
        
    def start(self):
        ''' start '''
        print 'start processingManager'

class OutputManager():
    ''' manager to control feeders '''
    def __init__(self):
        ''' constructor '''
        self.plugins = []

    def start(self):
        ''' start '''
        print 'start outputManager'

class UltraFinance():
    ''' base class for ultraFinance'''
    def __init__(self):
        ''' constructor '''
        pass
    
    def setup(self):
        ''' setup feeder, output and processing plugins '''
        self.feederManager = FeederManager()
        self.feederManager.plugins.append(DefaultFeeder)
        
        self.processingManager = ProcessingManager()
        self.processingManager.plugins.append(DefaultProcessing)

        self.outputManager = OutputManager()
        self.outputManager.plugins.append(DefaultOutput)
                
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