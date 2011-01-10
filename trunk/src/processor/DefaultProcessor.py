'''
Created on Dec 18, 2010

@author: ppa
'''
from BaseModule import BaseModule

class DefaultProcessor(BaseModule):
    def __init__(self):
        ''' constructor '''
        super(DefaultProcessor, self).__init__()
        
    def execute(self, input):
        ''' processing data'''
        super(DefaultProcessor, self).execute(input)
        return input