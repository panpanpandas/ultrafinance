'''
Created on Feb 26, 2011

@author: ppa
'''
import logging
LOG = logging.getLogger(__name__)

def fixAmountPerPeriod(dateValues, interval):
    ''' fix amount investment for each time period'''
    amount = float(100)
    share = sum([amount/dateValues[index].value for index in range(len(dateValues)/interval)])
    return share * dateValues[-1].value / (amount * len(dateValues) / interval)

def fixAmountPerPeriodWithAddtionWhenDrop(dateValues, interval, slidingWindow):
    ''' fix amount investment for each time period'''
    amount = float(100)
    fixShare = sum([amount/dateValues[index].value for index in range(len(dateValues)/interval)])
    #adjustShare = sum([amount/dateValues[index].value for index in range(len(dateValues)) if index >= slidingWindow and min([dateValue.value for dateValue in dateValues[index-slidingWindow:index+1]]) == dateValues[index]])
    adjustShare = sum([amount/dateValues[index].value for index in range(len(dateValues)) if index >= slidingWindow and min([dateValue.value for dateValue in dateValues[index-slidingWindow:index+1]]) == dateValues[index].value])
    share = adjustShare + fixShare
    return share * dateValues[-1].value / (amount * len(dateValues) / interval)

def adjustFixAmountPerPeriod(dateValues, interval, slidingWindow):
    ''' fix amount investment for each time period'''
    amount = float(100)
    share = 0
    for frame in range(len(dateValues)/interval):
        bought = False
        for i in range(interval):
            index = frame*interval + i
            if index >= slidingWindow and min([dateValue.value for dateValue in dateValues[index-slidingWindow:index+1]]) == dateValues[index].value:
                share += amount/dateValues[index].value
                bought = True
                break

        if not bought:
            share += amount/dateValues[(frame+1) * interval - 1].value

    return share * dateValues[-1].value / (amount * len(dateValues) / interval)