'''
Created on Jan 3, 2011

@author: ppa
'''
from matplotlib import pyplot
from datetime import datetime

import logging
LOG = logging.getLogger(__name__)

class PlotDateValueDict(object):
    ''' plot dict with date value '''
    def __init__(self, dateValueDict, dateFormat='%Y', lowMargin=0.05, upMargin=0.05, rightMargin=0.05, leftMargin=0.05, betweenMargin=0.05):
        ''' constructor '''
        self.dateValueDict = dateValueDict
        self.length = len(dateValueDict.keys())
        self.lowMargin = lowMargin
        self.upMargin = upMargin
        self.leftMargin = leftMargin
        self.rightMargin = rightMargin
        self.dateFormat = dateFormat

        self.rect = []
        height =  float(1 - self.lowMargin - self.upMargin - (self.length-1)*betweenMargin)/self.length
        pre = self.lowMargin
        for index in range(self.length):
            self.rect.append([self.leftMargin, pre, 1 - self.leftMargin - self.rightMargin , height])
            pre = pre + height + betweenMargin

        pyplot.rc('axes', grid=True)
        pyplot.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

    def plot(self):
        ''' get average '''
        fig = pyplot.figure()

        i = 0
        ax0 = None
        for label, dateValues in self.dateValueDict.items():
            print dateValues
            if 0 == i:
                ax = fig.add_axes(self.rect[i])
                ax0 = ax
            else:
                ax = fig.add_axes(self.rect[i], sharex=ax0)
            i += 1
            ax.plot_date([datetime.strptime(dateValue.date, self.dateFormat) for dateValue in dateValues],
                     [dateValue.value for dateValue in dateValues], fmt='b-')
            ax.set_ylabel(label)
            ax.set_ylim(min([int(dateValue.value) for dateValue in dateValues]) /1.1, max([int(dateValue.value) for dateValue in dateValues]) * 1.1 )
            #ax.set_ylim(0, 1000)

        pyplot.show()