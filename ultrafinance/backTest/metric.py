'''
Created on Apr 29, 2012

@author: ppa
'''
import abc
from ultrafinance.pyTaLib.indicator import stddev, sharpeRatio, mean

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
    SRATIO = 'sratio'
    START_TIME = "stime"
    END_TIME="etime"
    END_VALUE="evalue"

    def __init__(self):
        super(BasicMetric, self).__init__()
        self.result = {BasicMetric.MAX: (None, -1),
                       BasicMetric.MIN: (None, -1),
                       BasicMetric.STDDEV:-1,
                       BasicMetric.SRATIO:-1,
                       BasicMetric.START_TIME:-1,
                       BasicMetric.END_TIME:-1,
                       BasicMetric.END_VALUE:-1}

    def calculate(self, timePositions):
        ''' calculate basic metrics '''
        for (timeStamp, position) in timePositions:
            if self.result[BasicMetric.MAX][0] is None or self.result[BasicMetric.MAX][1] < position:
                self.result[BasicMetric.MAX] = timeStamp, position
            if self.result[BasicMetric.MIN][0] is None or self.result[BasicMetric.MIN][1] > position:
                self.result[BasicMetric.MIN] = timeStamp, position

        self.result[BasicMetric.START_TIME] = timePositions[0][0]
        self.result[BasicMetric.END_TIME] = timePositions[-1][0]
        self.result[BasicMetric.END_VALUE] = timePositions[-1][1]
        self.result[BasicMetric.STDDEV] = stddev([timePosition[1] for timePosition in timePositions])
        self.result[BasicMetric.SRATIO] = sharpeRatio([timePosition[1] for timePosition in timePositions])

        return self.result

    def formatResult(self):
        ''' format result '''
        return "Lowest value %.2f at %s; Highest %.2f at %s; %s - %s end values %.1f; Sharpe ratio is %.2f" % \
            (self.result[BasicMetric.MIN][1], self.result[BasicMetric.MIN][0],
             self.result[BasicMetric.MAX][1], self.result[BasicMetric.MAX][0],
             self.result[BasicMetric.START_TIME], self.result[BasicMetric.END_TIME], self.result[BasicMetric.END_VALUE],
             self.result[BasicMetric.SRATIO])

class MetricCalculator(object):
    ''' TODO: make it more generic for more metrics '''
    def __init__(self):
        ''' constructor '''
        self.__calculated = {}

    def calculate(self, symbols, timePositions):
        ''' calculate metric base on positions '''
        metric = BasicMetric()
        metric.calculate(timePositions)
        self.__calculated['_'.join(symbols)] = metric

    def formatMetrics(self):
        ''' output all calculated metrics '''
        bestSymbol = None
        bestMetric = None
        worstSymbol = None
        worstMetric = None

        output = []
        for symbols, metric in self.__calculated.items():
            output.append("%s: %s" % (symbols, metric.formatResult()))

            if bestSymbol == None or metric.result[BasicMetric.END_VALUE] > bestMetric.result[BasicMetric.END_VALUE]:
                bestSymbol = symbols
                bestMetric = metric

            if worstSymbol == None or metric.result[BasicMetric.END_VALUE] < worstMetric.result[BasicMetric.END_VALUE]:
                worstSymbol = symbols
                worstMetric = metric

        output.append("MEAN end value: %.1f, mean sharp ratio: %.2f" % (mean([m.result[BasicMetric.END_VALUE] for m in self.__calculated.values()]),
                                                                    mean([m.result[BasicMetric.SRATIO] for m in self.__calculated.values()])))
        output.append("Best %s: %s" % (bestSymbol, bestMetric.formatResult()))
        output.append("Worst %s: %s" % (worstSymbol, worstMetric.formatResult()))
        return '\n'.join(output)

