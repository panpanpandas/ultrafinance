'''
Created on Dec 18, 2010

@author: ppa
'''
from feeder.BaseFeeder import BaseFeeder

class DefaultFeeder(BaseFeeder):
    ''' Default feeder '''
    def before(self):
        ''' init connection '''
        print 'connection established'
        
    def after(self):
        ''' close connection '''
        print 'connection closed'
        
    def run(self, data):
        ''' preparing data'''
        data = {'defaultStock':('12/18/2010', '$20')}
        return True