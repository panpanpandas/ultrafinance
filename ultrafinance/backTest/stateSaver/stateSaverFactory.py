'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import Errors, UfException
from ultrafinance.backTest.stateSaver.hbaseSaver import HbaseSaver
from ultrafinance.designPattern.singleton import Singleton

import logging
LOG = logging.getLogger()

class StateSaverFactory(Singleton):
    ''' factory for output saver '''
    SAVER_DICT = {'hbase': HbaseSaver}

    @staticmethod
    def createStateSaver(name):
        ''' create state saver '''
        if name not in StateSaverFactory.SAVER_DICT:
            raise UfException(Errors.INVALID_SAVER_NAME,
                              "Saver name is invalid %s" % name)

        return StateSaverFactory.SAVER_DICT[name]()
