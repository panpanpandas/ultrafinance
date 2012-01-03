'''
Created on July 31, 2011

@author: ppa

copyied from http://code.activestate.com/recipes/131499-observer-pattern/
Not sure whether it's a good idea to remove observer class
'''
class Observable:
    ''' class for observer design pattern '''
    def __init__(self):
        ''' constructor '''
        self._observers = []

    def attach(self, observer):
        ''' add observer '''
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        ''' remove observer '''
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        ''' call update() method of observer '''
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)