'''
Created on Dec 18, 2010

@author: ppa
'''
from output.BaseOutput import BaseOutput

class DefaultOutput(BaseOutput):
    ''' Default feeder '''
    def before(self):
        ''' init output '''
        print 'before output'
        
    def after(self):
        ''' close output '''
        print 'after output'
        
    def run(self, data):
        ''' do output'''
        print 'doing output'
        return True