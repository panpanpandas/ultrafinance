'''
Created on Dec 18, 2010

@author: ppa
'''
import ConfigParser
import os

import logging
LOG = logging.getLogger(__name__)

class Configuration(object):
    ''' class that handles configuration '''
    def __init__(self, configFilePath=None):
        ''' Constructor '''
        if configFilePath:
            self.configFilePath = configFilePath
        else:
            self.configFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'dev.ini')

    def getConfiguration(self, section):
        ''' load all configuration '''
        configs = {}
        parser = ConfigParser.SafeConfigParser()
        parser.read(self.configFilePath)
        if parser.has_section(section):
            for name, value in parser.items(section):
                configs[name] = value
            return configs
        else:
            return None

    def getOption(self, section, option):
        ''' whether a option exists in the section '''
        parser = ConfigParser.SafeConfigParser()
        parser.read(self.configFilePath)
        if parser.has_option(section, option):
            return parser.get(section, option)
        else:
            return None

app_global = Configuration().getConfiguration("app_main")

if __name__ == '__main__':
    print Configuration().getOption('app_main', 'feeder')