'''
Created on Dec 18, 2010

@author: ppa
'''
import abc
from pydispatch.dispatcher import send

class BaseModule(object):
    '''
    Base class for a feeder, processor and outputer
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        ''' constructor'''
        self.input = None
        self.output = None

    def before(self):
        ''' init operation for processing data'''
        pass

    def after(self):
        ''' operation for cleaing up(e.g. close connection, database ...) '''
        print 'send out signal %s' % self.__class__.__name__
        return send(self.__class__.__name__, self, \
                    input=self.output)

    def execute(self, input):
        ''' processsing data'''
        self.input = input
    
    def run(self, input):
        ''' full execution'''
        print 'running %s' % self.__class__.__name__
        self.before()
        self.output = self.execute(input)
        self.after()

    def __getName(self):
        ''' retrun name '''
        return self.__class__.__name__
    
    name = property(__getName)