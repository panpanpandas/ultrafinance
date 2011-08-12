'''
Created on Dec 18, 2010

@author: ppa
'''
import sys
from BeautifulSoup import BeautifulSoup
from datetime import datetime

import logging
LOG = logging.getLogger(__name__)

googCSVDateformat = "%d-%b-%y"

def import_class(path, fileName, className=None):
    ''' dynamically import class '''
    if not className:
        className = capitalize(fileName)
    sys.path.append(path)

    mod = __import__(fileName)
    return getattr(mod, className)

def capitalize(inputString):
    ''' capitalize first letter '''
    return inputString[0].upper() + inputString[1:] if len(inputString) > 1 else inputString[0].upper()

def deCapitalize(inputString):
    ''' de-capitalize first letter '''
    return inputString[0].lower() + inputString[1:] if len(inputString) > 1 else inputString[0].lower()

def splitByComma(inputString):
    ''' split string by comma '''
    return [name.strip() for name in inputString.split(',')]

def convertGoogCSVDate(googCSVDate):
    ''' convert date 25-Jul-2010 to 2010-07-25'''
    return datetime.strptime(googCSVDate, googCSVDateformat).date()

def findPatthen(page, pList):
    datas = [BeautifulSoup(page)]
    index = 0
    for key, pattern in pList:
        newDatas = []
        for data in datas:
            if 'id' == key:
                newDatas.extend(data.findAll(id=pattern, recursive=True))
            if 'text' == key:
                newDatas.extend(data.findAll(text=pattern, recursive=True))

        datas = newDatas
        index += 1
        if not datas:
            break

    return datas