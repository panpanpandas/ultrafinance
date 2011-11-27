'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.excelDAM import ExcelDAM
from ultrafinance.dam.yahooDAM import YahooDAM
from ultrafinance.dam.googleDAM import GoogleDAM
from ultrafinance.dam.hbaseDAM import HBaseDAM

class DAMFactory:
    ''' DAO factory '''
    daoDict = {'yahoo': YahooDAM,
               'google': GoogleDAM,
               'excel': ExcelDAM,
               'hbase': HBaseDAM}

    @staticmethod
    def createDAO(self, name):
        return DAMFactory.daoDict.get(name)()

    @staticmethod
    def getAvailableTypes(self):
        ''' return all available types '''
        return DAMFactory.daoDict.keys()