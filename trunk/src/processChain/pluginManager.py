'''
Created on Dec 25, 2010

@author: ppa
'''

import os
import fnmatch
from util import import_class
from pydispatch.dispatcher import connect, send

from configuration import Configuration

import logging
LOG = logging.getLogger(__name__)

class PluginManager(object):
    ''' plugin manager that init and run all plugins '''
    groupNames = ['feeder', 'processor', 'outputer']

    def __init__(self):
        ''' constructor '''
        self.plugins = {}
        for groupName in PluginManager.groupNames:
            self.plugins[groupName] = {}

    def __loadGroupPlugins(self, groupName):
        ''' load a group of plugins under a folder '''
        path = os.getcwd() + '\\' + groupName
        for pluginName in [os.path.splitext(filename)[0] for filename in fnmatch.filter(os.listdir(path), '*.py')]:
            if '__init__' != pluginName:
                self.plugins[groupName][pluginName] = import_class(path, pluginName)()

    def setupPlugins(self):
        ''' dynamically load all plugins '''
        for groupName in PluginManager.groupNames:
            self.__loadGroupPlugins(groupName)

        for groupName in PluginManager.groupNames:
            for pluginName in self.plugins[groupName]:
                self.__setup_dispatcher(groupName, pluginName)

    def __setup_dispatcher(self, groupName, pluginName):
        ''' setup dispatcher according to config file '''
        if 'outputer' != groupName: #can not be the last one in groupNames
            gIndex = PluginManager.groupNames.index(groupName)
            nextGroupName = PluginManager.groupNames[gIndex + 1]
            receiverNames = Configuration().getOption(pluginName + '_mapping', 'receiver')
            if None != receiverNames:
                for receiverName in [name.strip() for name in receiverNames.split(',')]:
                    if pluginName in self.plugins[groupName] and receiverName in self.plugins[nextGroupName]:
                        print 'connect %s to receiver %s' % (pluginName, receiverName)
                        connect(
                            self.plugins[nextGroupName][receiverName].run,
                            signal = pluginName,
                            sender = self.plugins[groupName][pluginName],
                        )

    def runPlugin(self, groupName, pluginName):
        self.plugins[groupName][pluginName].run(self.plugins[groupName][pluginName].input)

    def triggerDispatcher(self, groupName, pluginName):
        ''' trigger dispatcher with the output '''
        send(pluginName, pluginName, input = self.plugins[groupName][pluginName].input)

    def setInput(self, groupName, pluginName, input):
        self.plugins[groupName][pluginName].input = input