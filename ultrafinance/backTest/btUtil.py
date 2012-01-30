'''
Created on Jan 6, 2012

@author: ppa
'''
import re

OUTPUT_PREFIX = 'output'
OUTPUT_FIELDS = ['placedOrder', 'accountValue', 'executedOrder']

def findInListbyRe(itemList, reString):
    ''' find items in list by re '''
    items = []
    pair = re.compile(reString)

    for item in itemList:
        result = pair.match(item)
        if result and result.group(0) == item:
            items.append(item)

    return items

def validateTradeType(self):
    ''' validate whether global type is set or not'''
    types = [QUTOE, TICK]
    if appGlobal[TRADE_TYPE] not in types:
        raise UfException(Errors.INVALID_TYPE,
                          'Type %s is not accepted, allow types: %s' % (appGlobal[TRADE_TYPE], types))
