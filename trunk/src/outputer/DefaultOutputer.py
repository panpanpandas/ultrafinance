'''
Created on Dec 18, 2010

@author: ppa
'''
from outputer.BaseOutputer import BaseOutputer

class DefaultOutputer(BaseOutputer):
    ''' Default feeder '''
    def before(self):
        ''' init output '''
        print 'before output'
        
    def after(self):
        ''' close output '''
        print 'after output'
        
    def run(self, input, data):
        ''' do output'''
        print input