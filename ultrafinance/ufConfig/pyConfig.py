'''
Created on Nov 30, 2010

@author: ppa
'''
import ConfigParser
from os import path
from ultrafinance.lib.errors import UfException, Errors

import logging
LOG = logging.getLogger()

class PyConfig(object):
    ''' class that handles configuration '''
    def __init__(self):
        ''' Constructor '''
        self.__dir = None
        self.__parser = None
        self.__fullPath = None

    def setSource(self, fileName):
        '''
        set source file name
        assume the fileName is full path first, if can't find it, use conf directory
        '''
        fullPath = path.abspath(fileName)

        if not path.exists(fullPath):
            fullPath = path.join(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'conf'),
                                 fileName)
            if not path.exists(fullPath):
                msg = "config file doesn't exist at: %s or %s" % (fileName, fullPath)
                LOG.error(msg)
                raise UfException(Errors.FILE_NOT_EXIST, msg)

        self.__parser = ConfigParser.SafeConfigParser(defaults={"here": self.__dir})
        self.__parser.read(fullPath)
        self.__fullPath = fullPath

    def getDir(self):
        ''' get directory of conf file'''
        self.__validateConfig()
        return path.dirname(self.__fullPath)


    def getSection(self, section):
        ''' load all configuration '''
        self.__validateConfig()

        configs = {}
        if self.__parser and self.__parser.has_section(section):
            for name, value in self.__parser.items(section):
                configs[name] = value
            return configs

        return configs

    def getOption(self, section, option):
        ''' whether an option exists in the section '''
        self.__validateConfig()

        if self.__parser and self.__parser.has_option(section, option):
            return self.__parser.get(section, option)
        else:
            return None

    def getFullPath(self):
        ''' get full path of config '''
        return self.__fullPath

    def override(self, section, key, value):
        ''' override/set a key value pair'''
        if not self.__parser.has_section(section):
            self.__parser.add_section(section)

        self.__parser.set(section, key, str(value))

    def __validateConfig(self):
        ''' validate config is ok '''
        if self.__parser is None:
            msg = "No config file is loaded, please use setSource method first"
            LOG.error(msg)
            raise UfException(Errors.FILE_NOT_EXIST, msg)



if __name__ == '__main__':
    config = PyConfig()
    config.setSource('test.ini')
    config.override("testSection", "123", "456")
    config.override("testSection", "123", "567")
    print(config.getOption('app_main', 'feeder'))
    print(config.getSection('app_main'))
    print(config.getOption("testSection", "123"))
