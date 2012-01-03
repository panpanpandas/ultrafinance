'''
Created on Dec 18, 2010

@author: ppa
'''
from ultrafinance.processChain.pluginManager import PluginManager
from ultrafinance.processChain.configuration import Configuration
import threading
import time

import logging
LOG = logging.getLogger(__name__)

#TODO: use singleton pattern
class ProcessChain(threading.Thread):
    ''' class processChain '''
    def __init__(self, configFile):
        ''' constructor '''
        super(ProcessChain, self).__init__()
        self.configure = Configuration(configFile)
        #self.configure = Configuration()
        self.pluginManager = PluginManager(self.configure)

    def run(self):
        ''' thread run function '''
        self.pluginManager.setup()
        self.pluginManager.setInput('feeder', 'historicalDataFeeder', 'GOOG')
        self.pluginManager.runFeederPlugins()

def runProcessChain(configFile):
    ''' run process chain '''
    print "Using configuration file %s" % configFile
    processChain = ProcessChain(configFile)
    processChain.start()