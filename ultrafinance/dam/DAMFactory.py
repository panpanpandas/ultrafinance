'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.excelDAM import ExcelDAM
from ultrafinance.dam.yahooDAM import YahooDAM
from ultrafinance.dam.googleDAM import GoogleDAM
from ultrafinance.dam.hbaseDAM import HBaseDAM

from ultrafinance.lib.errors import Errors, UfException

class DAMFactory(object):
    ''' DAM factory '''
    DAM_DICT = {'yahoo': YahooDAM,
               'google': GoogleDAM,
               'excel': ExcelDAM,
               'hbase': HBaseDAM}

    @staticmethod
    def createDAM(damType):
        ''' create DAM '''
        if damType not in DAMFactory.DAM_DICT:
            raise UfException(Errors.INVALID_DAM_TYPE,
                              "DAM type is invalid %s" % damType)
        return DAMFactory.DAM_DICT[damType]()

    @staticmethod
    def getAvailableTypes():
        ''' return all available types '''
        return DAMFactory.DAM_DICT.keys()
