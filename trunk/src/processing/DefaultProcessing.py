'''
Created on Dec 18, 2010

@author: ppa
'''
from processing.BaseProcessing import BaseProcessing

class DefaultProcessing(BaseProcessing):
    ''' Default feeder '''
    def before(self):
        ''' init processing '''
        print 'init processing'
        
    def after(self):
        ''' after processing '''
        print 'after processing'
        
    def run(self, data):
        ''' processing data'''
        print 'Cong! YOU JUST WIN A DOLLOA'
        return True