'''
Created on Apr 29, 2012

@author: ppa
'''
import abc
from ultrafinance.pyTaLib.indicator import stddev, sharpeRatio, mean, rsquared

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
    MAX_TIME_VALUE = 'maxTimeValue'
    MIN_TIME_VALUE = 'minTimeValue'
    MAX_DRAW_DOWN = "maxDrawDown"
    STDDEV = 'stddev'
    SRATIO = 'sharpeRatio'
    START_TIME = "startTime"
    END_TIME="endTime"
    END_VALUE="endValue"
    R_SQUARED = "rSquared"

    def __init__(self):
        super(BasicMetric, self).__init__()
        self.result = {BasicMetric.MAX_TIME_VALUE: (None, -1),
                       BasicMetric.MIN_TIME_VALUE: (None, -1),
                       BasicMetric.STDDEV:-1,
                       BasicMetric.SRATIO:-1,
                       BasicMetric.R_SQUARED:-1,
                       BasicMetric.START_TIME:-1,
                       BasicMetric.END_TIME:-1,
                       BasicMetric.END_VALUE:-1}

    def calculate(self, timePositions, iTimePositionDict):
        ''' calculate basic metrics '''
        if not timePositions:
            return self.result

        # get max value, min value, max draw down
        lastHigest = 0
        maxDrawDownTimeStamp = 0
        maxDrawDownPosition = 0
        for (timeStamp, position) in timePositions:
            if self.result[BasicMetric.MAX_TIME_VALUE][0] is None or self.result[BasicMetric.MAX_TIME_VALUE][1] < position:
                self.result[BasicMetric.MAX_TIME_VALUE] = timeStamp, position
            if self.result[BasicMetric.MIN_TIME_VALUE][0] is None or self.result[BasicMetric.MIN_TIME_VALUE][1] > position:
                self.result[BasicMetric.MIN_TIME_VALUE] = timeStamp, position
            if position > lastHigest:
                lastHigest = position
                maxDrawDownPosition = position
                maxDrawDownTimeStamp = timeStamp
            elif maxDrawDownPosition > position:
                maxDrawDownPosition = position
                maxDrawDownTimeStamp = timeStamp

        self.result[BasicMetric.MAX_DRAW_DOWN] = (0, 0) if lastHigest == 0 else \
            (maxDrawDownTimeStamp, 1 - (maxDrawDownPosition / lastHigest))
        self.result[BasicMetric.START_TIME] = timePositions[0][0]
        self.result[BasicMetric.END_TIME] = timePositions[-1][0]
        self.result[BasicMetric.END_VALUE] = timePositions[-1][1]
        self.result[BasicMetric.STDDEV] = stddev([timePosition[1] for timePosition in timePositions])
        self.result[BasicMetric.SRATIO] = sharpeRatio([timePosition[1] for timePosition in timePositions])
        self.result[BasicMetric.R_SQUARED] = rsquared([tp[1] for tp in timePositions], [iTimePositionDict.get(tp[0], tp[1]) for tp in timePositions])

        return self.result

    def formatResult(self):
        ''' format result '''
        return "Lowest value %.2f at %s; Highest %.2f at %s; %s - %s end values %.1f; %s - %s end values %.1f; Sharpe ratio is %.2f; r squared is %.2f" % \
            (self.result[BasicMetric.MIN_TIME_VALUE][1], self.result[BasicMetric.MIN_TIME_VALUE][0],
             self.result[BasicMetric.MAX_TIME_VALUE][1], self.result[BasicMetric.MAX_TIME_VALUE][0],
             self.result[BasicMetric.START_TIME], self.result[BasicMetric.END_TIME], self.result[BasicMetric.END_VALUE],
             self.result[BasicMetric.MAX_DRAW_DOWN][1], self.result[BaseMetric.MAX_DRAW_DOWN][0],
             self.result[BasicMetric.SRATIO], self.result[BasicMetric.R_SQUARED])

class MetricManager(object):
    ''' TODO: make it more generic for more metrics '''
    def __init__(self):
        ''' constructor '''
        self.__calculated = {}

    def calculate(self, symbols, timePositions, iTimePositionDict):
        ''' calculate metric base on positions '''
        metric = BasicMetric()
        metric.calculate(timePositions, iTimePositionDict)
        self.__calculated['_'.join(symbols)] = metric.result
        return metric.result

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

        output.append("MEAN end value: %.1f, mean sharp ratio: %.2f" % (mean([m[BasicMetric.END_VALUE] for m in self.__calculated.values() if m[BasicMetric.END_VALUE] > 0]),
                                                                    mean([m[BasicMetric.SRATIO] for m in self.__calculated.values() if m[BasicMetric.SRATIO] > -1])))
        output.append("Best %s: %s" % (bestSymbol, bestMetric.formatResult()))
        output.append("Worst %s: %s" % (worstSymbol, worstMetric.formatResult()))
        return '\n'.join(output)


    def getMetrics(self):
        ''' get metrics '''
        return self.__calculated
