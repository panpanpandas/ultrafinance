'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.designPattern.singleton import Singleton

import logging
LOG = logging.getLogger()

class StateSaverFactory(Singleton):
    ''' factory for output saver '''
    @staticmethod
    def createStateSaver(name, setting, tableName = None):
        ''' create state saver '''
        if 'habse' == name:
            from ultrafinance.backTest.stateSaver.hbaseSaver import HbaseSaver
            saver = HbaseSaver()
        elif 'sql' == name:
            from ultrafinance.backTest.stateSaver.sqlSaver import SqlSaver
            saver = SqlSaver()
        else:
            raise UfException(Errors.INVALID_SAVER_NAME,
                              "Saver name is invalid %s" % name)

        saver.setup(setting, 'output' if tableName is None else tableName)
        return saver
