'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.excelDAM import ExcelDAM
from ultrafinance.dam.yahooDAM import YahooDAM
from ultrafinance.dam.googleDAM import GoogleDAM
from ultrafinance.dam.hbaseDAM import HBaseDAM

from ultrafinance.lib.errors import Errors, UfException

class DAMFactory:
    ''' DAO factory '''
    daoDict = {'yahoo': YahooDAM,
               'google': GoogleDAM,
               'excel': ExcelDAM,
               'hbase': HBaseDAM}

    @staticmethod
    def createDAM(name):
        ''' create DAM '''
        if name not in DAMFactory.daoDict:
            raise UfException(Errors.INVALID_DAM_NAME,
                              "DAM name is invalid %s" % name)
        return DAMFactory.daoDict.get(name)()

    @staticmethod
    def getAvailableTypes(self):
        ''' return all available types '''
        return DAMFactory.daoDict.keys()