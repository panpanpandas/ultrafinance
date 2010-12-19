'''
Created on Dec 18, 2010

@author: ppa
'''
import ConfigParser

class Configuration(object):
    ''' class that handles configuration '''
    def __init__(self):
        ''' Constructor '''
        pass
    
    def getConfiguration(self):
        configs = dict()
        self.__config = ConfigParser.SafeConfigParser()
        self.__config.read('config/dev.ini')
        for name, value in self.__config.items("app_main"):
            configs[name] = value
        
        return configs

app_global = Configuration().getConfiguration()