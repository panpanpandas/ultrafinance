'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.excelDAM import ExcelDAM
from ultrafinance.dam.yahooDAM import YahooDAM
from ultrafinance.dam.googleDAM import GoogleDAM
from ultrafinance.dam.hbaseDAM import HBaseDAM
from ultrafinance.dam.sqlDAM import SqlDAM

from ultrafinance.lib.errors import Errors, UfException

class DAMFactory(object):
    ''' DAM factory '''
    DAM_DICT = {'yahoo': YahooDAM,
                'google': GoogleDAM,
                'excel': ExcelDAM,
                'hbase': HBaseDAM,
                'sql': SqlDAM}

    @staticmethod
    def createDAM(damType, settings = None):
        ''' create DAM '''
        if damType not in DAMFactory.DAM_DICT:
            raise UfException(Errors.INVALID_DAM_TYPE,
                              "DAM type is invalid %s" % damType)
        dam = DAMFactory.DAM_DICT[damType]()
        dam.setup(settings)
        return dam

    @staticmethod
    def getAvailableTypes():
        ''' return all available types '''
        return DAMFactory.DAM_DICT.keys()
