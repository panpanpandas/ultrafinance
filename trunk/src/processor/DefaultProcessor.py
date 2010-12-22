'''
Created on Dec 18, 2010

@author: ppa
'''
from processor.BaseProcessor import BaseProcessor

class DefaultProcessor(BaseProcessor):
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