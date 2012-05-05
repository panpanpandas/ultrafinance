'''
Created on Apr 29, 2012

@author: ppa
'''
import abc
from ultrafinance.pyTaLib import stddev, sharpeRatio

class BaseMetric(object):
    ''' base metric class '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate(self, timePositions):
        ''' keep record of the account '''
        return

    @abc.abstractmethod
    def formatResult(self):
        ''' print result '''
        return

class BasicMetric(BaseMetric):
    ''' basic metrics '''
    MAX = 'max'
    MIN = 'min'
    STDDEV = 'stddev'
    SRATIO = 'sRatio'
    SINTERVAL = 22

    def __init__(self):
        super(BasicMetric, self).__init__()
        self.result = {BasicMetric.MAX: (None, None),
                       BasicMetric.MIN: (None, None),
                       BasicMetric.STDDEV: None,
                       BasicMetric.SRATIO: None}

    def calculate(self, timePositions):
        ''' calculate basic metrics '''
        for (timeStamp, position) in timePositions:
            if self.result[BasicMetric.MAX][0] is None or self.result[BasicMetric.MAX][1] < position:
                self.result[BasicMetric.MAX] = timeStamp, position
            if self.result[BasicMetric.MIN][0] is None or self.result[BasicMetric.MIN][1] > position:
                self.result[BasicMetric.MIN] = timeStamp, position

        self.result[BasicMetric.STDDEV] = stddev([timePosition[1] for timePosition in timePositions])
        self.result[BasicMetric.SRATIO] = sharpeRatio([timePosition[1] for timePosition in timePositions],
                                                      BasicMetric.SINTERVAL)

        return self.result

    def formatResult(self):
        ''' format result '''
        return "Lowest point %.2f at %s; Highest point %.2f at %s; STDDEV is %s; Sharpe ratio is %s" % \
            (self.result[BasicMetric.MIN][1], self.result[BasicMetric.MIN][0],
             self.result[BasicMetric.MAX][1], self.result[BasicMetric.MAX][0],
             self.result[BasicMetric.STDDEV],
             self.result[BasicMetric.SRATIO])

class MetricCalculator(object):
    ''' basic metrics'''
    def __init__(self):
        ''' constructor '''
        self.__metrics = [BasicMetric]

    def formatMetrics(self, timePositions):
        ''' calculate metrics base on positions '''
        output = []
        for metricClass in self.__metrics:
            metric = metricClass()
            metric.calculate(timePositions)
            output.append(metric.formatResult())

        return '\n'.join(output)
