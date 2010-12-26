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
        
    def run(self, input, data):
        ''' processing data'''
        data.update(input)
        return True