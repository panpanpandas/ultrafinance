'''
Created on May 6, 2011

@author: ppa
'''
import traceback

class Errors(object):
    """ class hosts error code constants """
    # general errors
    UNKNOWN_ERROR = 1
    FILE_NOT_EXIST = 2
    FILE_EXIST = 3
    UNDEFINED_METHOD = 4

    NETWORK_ERROR = 100
    NETWORK_400_ERROR = 101

    INDEX_RANGE_ERROR = 200
    INVALID_DAM_TYPE = 201

    STOCK_SYMBOL_ERROR = 300
    STOCK_PARSING_ERROR = 301

    HBASE_CREATE_ERROR = 401
    HBASE_UPDATE_ERROR = 402

    #type eroor
    SIDE_TYPE_ERROR = 500
    ORDER_TYPE_ERROR = 501
    TRANSITION_TYPE_ERROR = 502

    #tickFeeder
    FEEDER_INVALID_ERROR = 600
    SYMBOL_EXIST = 601
    INVALID_TYPE = 602
    SYMBOL_NOT_IN_SOURCE = 604
    FEEDER_TIMEOUT = 605

    #account error
    ORDER_INVALID_ERROR = 700
    MISSING_SYMBOL = 701

    #excelLib error
    SHEET_NAME_EXIST = 800
    SHEET_NAME_INVALID = 801
    INVALID_EXCEL_MODE = 802

    #trading error
    INVALID_ACCOUNT = 901

    #metric
    INVALID_METRIC_NAME = 1001
    ACCOUNT_ALEADY_SET = 1002
    ACCOUNT_NOT_SET = 1003
    INVALID_RISK_FREE_RETURN = 1004

    #strategy
    INVALID_STRATEGY_NAME = 1200
    NONE_ACCOUNT_ID = 1201
    NONE_TRADING_CENTER = 1202
    INVALID_SYMBOLS = 1203

    #outputSaver
    TABLENAME_NOT_SET = 1300
    TABLENAME_ALREADY_SET = 1301
    INVALID_SAVER_NAME = 1302

class UfException(Exception):
    """ Ultra-Finance exception """
    def __init__(self, error, errorMsg):
        """ constructor  """
        super(UfException, self).__init__()
        self.__error = error
        self.__errorMsg = errorMsg

    def __str__(self):
        """ string """
        return repr(self.__errorMsg)

    def getCode(self):
        """ accessor """
        return self.__error

    def getMsg(self):
        """ accessor """
        return "%s: %s" % (self.__errorMsg, traceback.format_exc(5))
