'''
Created on Nov 9, 2011

@author: ppa
'''

from ultrafinance.lib.errors import Errors, UfException

class DAMFactory(object):
    ''' DAM factory '''
    @staticmethod
    def createDAM(damType, settings = None):
        ''' create DAM '''
        if 'yahoo' == damType:
            from ultrafinance.dam.yahooDAM import YahooDAM
            dam = YahooDAM()
        elif 'google' == damType:
            from ultrafinance.dam.googleDAM import GoogleDAM
            dam = GoogleDAM()
        elif 'excel' == damType:
            from ultrafinance.dam.excelDAM import ExcelDAM
            dam = ExcelDAM()
        elif 'hbase' == damType:
            from ultrafinance.dam.hbaseDAM import HBaseDAM
            dam = HBaseDAM()
        elif 'sql' == damType:
            from ultrafinance.dam.sqlDAM import SqlDAM
            dam = SqlDAM()
        else:
            raise UfException(Errors.INVALID_DAM_TYPE,
                              "DAM type is invalid %s" % damType)

        dam.setup(settings)
        return dam

    @staticmethod
    def getAvailableTypes():
        ''' return all available types '''
        return ['yahoo', 'google', 'excel', 'hbase', 'sql']
