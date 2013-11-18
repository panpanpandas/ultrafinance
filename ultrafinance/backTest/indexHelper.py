'''
Created on May 26, 2012

@author: ppa
'''
import logging
LOG = logging.getLogger()

class IndexHelper(object):
    ''' helper class providing index info '''

    def __init__(self):
        ''' constructor '''
        self.__tick = []

    def appendTick(self, tick):
        ''' self current tick '''
        self.__tick.append(tick)

        if len(self.__tick) >= 252:
            self.__tick.pop(0)
