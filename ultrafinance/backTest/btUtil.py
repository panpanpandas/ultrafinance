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
