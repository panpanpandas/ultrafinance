'''
Created on Dec 18, 2010

@author: ppa
'''
from processor.BaseProcessor import BaseProcessor
import math

class AvgDivProcessor(BaseProcessor):
    ''' Default feeder '''
    def before(self):
        ''' init processing '''
        print 'init processing'
        
    def after(self):
        ''' after processing '''
        print 'after processing'
        
    def run(self, input, data):
        ''' processing input'''
        sum = math.fsum(float(value) for value in input.values())
        avg = sum / len(input)
        var = math.fsum(math.pow((float(value) - avg), 2) for value in input.values())
        stdDiv = math.sqrt(var / len(input))
        
        data.update({'days': len(input), 'avg': avg, 'standard diviation': stdDiv})