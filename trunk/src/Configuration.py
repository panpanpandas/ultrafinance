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
    
    def getConfiguration(self, section):
        ''' load all configuration '''
        configs = dict()
        parser = ConfigParser.SafeConfigParser()
        parser.read('config/dev.ini')
        if parser.has_section(section):
            for name, value in parser.items(section):
                configs[name] = value
            return configs
        else:
            return None

    def getOption(self, section, option):
        ''' whether a option exists in the section '''
        parser = ConfigParser.SafeConfigParser()
        parser.read('config/dev.ini')
        if parser.has_option(section, option):
            return parser.get(section, option)
        else:
            return None 

app_global = Configuration().getConfiguration("app_main")

if __name__ == '__main__':
    print Configuration().getOption('HistoricalDataFeeder_mapping', 'receiver')