'''
Created on Dec 18, 2010

@author: ppa
'''
from BaseModule import BaseModule
import math

class AvgDivProcessor(BaseModule):
    ''' Calculate average and standard deviation '''
    def __init__(self):
        ''' constructor '''
        super(AvgDivProcessor, self).__init__()
        
    def execute(self, input):
        ''' processing input'''
        super(AvgDivProcessor, self).execute(input)
        data = {}
        sum = math.fsum(float(value) for value in input.values())
        avg = sum / len(input)
        var = math.fsum(math.pow((float(value) - avg), 2) for value in input.values())
        stdDiv = math.sqrt(var / len(input))
        
        data.update({'days': len(input), 'avg': avg, 'standard diviation': stdDiv})
        return data