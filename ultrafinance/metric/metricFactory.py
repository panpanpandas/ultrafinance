'''
Created on Dec 26, 2011

@author: ppa
'''

from ultrafinance.metric.highestMetric import HighestMetric
from ultrafinance.metric.lowestMetric import LowestMetric
from ultrafinance.metric.sharpeRatioMetric import SharpeRatioMetric

from ultrafinance.lib.errors import Errors, UfException

class MetricFactory:
    ''' DAO factory '''
    metricDict = {'highest': HighestMetric,
                  'lowest': LowestMetric,
                  'sharpratio': SharpeRatioMetric}

    @staticmethod
    def createMetric(name):
        ''' create a metric '''
        if name not in MetricFactory.metricDict:
            raise UfException(Errors.INVALID_METRIC_NAME,
                              "Metric name is invalid %s" % name)
        return MetricFactory.metricDict[name]()

    @staticmethod
    def getAvailableTypes(self):
        ''' return all available types '''
        return MetricFactory.metricDict.keys()
