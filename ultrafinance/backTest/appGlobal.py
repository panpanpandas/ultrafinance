'''
Created on Jan 24, 2012

@author: ppa
'''

from ultrafinance.designPattern.singleton import Singleton

class AppGlobal(dict, Singleton):
    ''' appGlobal class '''
    def __init__(self):
        super(AppGlobal, self).__init__()

appGlobal = AppGlobal.getInstance()

