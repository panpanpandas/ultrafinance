'''
Created on Dec 18, 2010

@author: ppa
'''
import sys

def import_class(path, name):
    sys.path.append(path)
    mod = __import__(name)
    return getattr(mod, name)     