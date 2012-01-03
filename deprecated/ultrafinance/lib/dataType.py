'''
Created on Feb 5, 2011

@author: ppa
'''
from collections import namedtuple

DateValueType = namedtuple('DateValue', 'date, value')
StockDailyType = namedtuple('StockDailyType', 'date, open, high, low, close, volume, adjClose')

