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
        self.configure = Configuration()
        self.pluginManager = PluginManager(self.configure)

    def setup(self):
        ''' setup feeder, output and processing plugins '''
        self.pluginManager.setup()
        self.pluginManager.setInput('feeder', 'historicalDataFeeder', 'GOOG')

    def start(self):
        ''' run function '''
        self.pluginManager.runFeederPlugins()

if __name__ == '__main__':
    processChain = ProcessChain()
    processChain.setup()
    processChain.start()
    print 'Finish Process Chain'