'''
Created on Dec 18, 2010

@author: ppa
'''
import sys

import logging
LOG = logging.getLogger(__name__)

def import_class(path, fileName, className=None):
    ''' dynamically import class '''
    if not className:
        className = fileName[0].capitalize() + fileName[1:]
    sys.path.append(path)

    mod = __import__(fileName)
    return getattr(mod, className)