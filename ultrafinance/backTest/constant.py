'''
Created on Jan 20, 2012

@author: ppa
'''

#config constant


CONF_APP_MAIN = 'app_main'

CONF_ULTRAFINANCE_SECTION = 'ultrafinance'
CONF_TRADE_TYPE = 'backtest.tradetype'
CONF_SYMBOL_FILE = 'backtest.symbolfile'
CONF_INDEX = 'backtest.index'
CONF_INIT_CASH = "backtest.initcash"
CONF_INPUT_DAM = 'backtest.input_dam'
CONF_INPUT_DB = 'backtest.input_db'
CONF_STRATEGY_NAME = 'backtest.strategy_name'
CONF_SAVER = 'backtest.output_saver'
CONF_OUTPUT_DB = 'backtest.output_db'
CONF_START_TRADE_DATE = 'backtest.start_trade_date'

#period strategy
CONF_STRATEGY_PERIOD = 'period'

#app global
TICK = 'tick'
QUOTE = 'quote'
TRADE_TYPE = 'tradetype'
STOP_FLAG = "stopFlag"

#EVENT LIST
EVENT_TICK_UPDATE = 'tickUpdate'
EVENT_ORDER_EXECUTED = "orderExecuted"