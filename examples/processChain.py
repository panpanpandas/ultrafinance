'''
Created on Dec 18, 2010

@author: ppa
'''
from ultrafinance.processChain.pluginManager import PluginManager
from ultrafinance.processChain.configuration import Configuration

import logging
LOG = logging.getLogger(__name__)

#TODO: use singleton pattern
class ProcessChain():
    ''' class processChain '''
    def __init__(self):
        ''' constructor '''
        self.pluginManager = PluginManager()
        self.pluginManager.setupPlugins()

    def setup(self):
        ''' setup feeder, output and processing plugins '''
        pass

    def start(self):
        ''' run function '''
        self.pluginManager.setInput('feeder', 'historicalDataFeeder', 'GOOG')

        pluginName = Configuration().getOption('app_main', 'feeder')
        if pluginName in self.pluginManager.plugins['feeder']:
            self.pluginManager.runPlugin('feeder', pluginName)
            self.pluginManager.triggerDispatcher('feeder', pluginName)

if __name__ == '__main__':
    processChain = ProcessChain()
    processChain.setup()
    processChain.start()
    print 'Finish Process Chain'