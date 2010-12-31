'''
Created on Dec 18, 2010

@author: ppa
'''
from PluginManager import PluginManager

class UltraFinance():
    ''' base class for ultraFinance'''
    def __init__(self):
        ''' constructor '''
        self.pluginManager = PluginManager()
        self.pluginManager.setupPlugins()
            
    def setup(self):
        ''' setup feeder, output and processing plugins '''
        pass

    def start(self):
        ''' run function '''
        self.pluginManager.setInput('feeder', 'HistoricalDataFeeder', 'GOOG')
        
        for pluginName in self.pluginManager.plugins['feeder']:
            self.pluginManager.runPlugin('feeder', pluginName)
            self.pluginManager.triggerDispatcher('feeder', pluginName)

        print 'HAHAHA'

if __name__ == '__main__':
    ultraFinance = UltraFinance()
    ultraFinance.setup()
    ultraFinance.start()