'''
Created on Dec 25, 2010

@author: ppa
'''

import os
import fnmatch
from pydispatch.dispatcher import connect, send
from ultrafinance.lib.util import import_class, splitByComma

import logging
LOG = logging.getLogger(__name__)

class PluginManager(object):
    ''' plugin manager that init and run all plugins '''
    groupNames = ['feeder', 'processor', 'outputer']

    def __init__(self, configure):
        ''' constructor '''
        self.plugins = {}
        self.configure = configure
        for groupName in PluginManager.groupNames:
            self.plugins[groupName] = {}

    def __loadGroupPlugins(self, groupName):
        ''' load a group of plugins under a folder '''
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), groupName)
        print "Loading plugins under %s" % path
        for pluginName in [os.path.splitext(filename)[0] for filename in fnmatch.filter(os.listdir(path), '*.py')]:
            # __init__ will not be loaded
            if '__init__' != pluginName:
                print "Plugin loaded: %s" % pluginName
                self.plugins[groupName][pluginName] = import_class(path, pluginName)()

    def runFeederPlugins(self):
        feederStrings = self.configure.getOption('app_main', 'feeder')
        if not feederStrings:
            print "No feeders provided: %s" % feederStrings

        for feederName in splitByComma(feederStrings):
            if feederName in self.plugins['feeder']:
                self.runPlugin('feeder', feederName)

    def setup(self):
        ''' setup plugins '''
        self.loadPlugins()
        self.setupDispatchers(self.configure)

    def loadPlugins(self):
        ''' load all plugins '''
        print "Start loading plugins....."
        for groupName in PluginManager.groupNames:
            self.__loadGroupPlugins(groupName)

    def setupDispatchers(self, configure):
        ''' setup dispatchers '''
        print "Start setting up dispatcher......"
        for groupName in PluginManager.groupNames:
            for pluginName in self.plugins[groupName]:
                receiverStrings = configure.getOption(pluginName + '_mapping', 'receiver')
                if receiverStrings:
                    self.__setup_dispatcher(groupName, pluginName, splitByComma(receiverStrings))

    def __setup_dispatcher(self, groupName, pluginName, receiverNames):
        ''' setup dispatcher according to config file '''
        if 'outputer' != groupName: #can not be the last one in groupNames
            gIndex = PluginManager.groupNames.index(groupName)
            nextGroupName = PluginManager.groupNames[gIndex + 1]
            for receiverName in receiverNames:
                if pluginName in self.plugins[groupName] and receiverName in self.plugins[nextGroupName]:
                    print 'connect %s to receiver %s' % (pluginName, receiverName)
                    connect(
                        self.plugins[nextGroupName][receiverName].run,
                        signal = pluginName,
                        sender = self.plugins[groupName][pluginName]
                    )
        else:
            print "Can't set dispatcher for outputer plugin: %s" % pluginName

    def runPlugin(self, groupName, pluginName):
        ''' run plugin '''
        print "Running plugin: %s" % pluginName
        self.plugins[groupName][pluginName].run(self.plugins[groupName][pluginName].input)

#    def triggerDispatcher(self, groupName, pluginName):
#        ''' trigger dispatcher '''
#        print "Trigger dispatcher: %s" % pluginName
#        send(pluginName, pluginName, input = self.plugins[groupName][pluginName].input)

    def setInput(self, groupName, pluginName, input):
        self.plugins[groupName][pluginName].input = input