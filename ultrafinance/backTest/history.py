'''
Created on May 26, 2012

@author: ppa
'''
import logging
LOG = logging.getLogger()

class History(object):
    ''' helper class providing history info '''
    INDEX = "I"

    def __init__(self):
        ''' constructor '''
        self.timeSymbolTick = {}

    def update(self, timeStamp, symbolTickDict, indexTick):
        ''' do update '''
        #each timestamp can only be updated once
        if timeStamp not in self.timeSymbolTick:
            self.timeSymbolTick[timeStamp] = {}

            for symbol, tick in symbolTickDict.iteritems():
                self.timeSymbolTick[timeStamp][symbol] = tick

            self.timeSymbolTick[timeStamp][History.INDEX] = indexTick
