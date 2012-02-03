'''
Created on Dec 26, 2011

@author: ppa
'''

from ultrafinance.backTest.metric.highestMetric import HighestMetric
from ultrafinance.backTest.metric.lowestMetric import LowestMetric
from ultrafinance.backTest.metric.sharpeRatioMetric import SharpeRatioMetric

from ultrafinance.lib.errors import Errors, UfException

class MetricFactory(object):
    ''' DAO factory '''
    METRIC_DICT = {'highest': HighestMetric,
                  'lowest': LowestMetric,
                  'sharpratio': SharpeRatioMetric}

    @staticmethod
    def createMetric(name):
        ''' create a metric '''
        if name not in MetricFactory.METRIC_DICT:
            raise UfException(Errors.INVALID_METRIC_NAME,
                              "Metric name is invalid %s" % name)
        return MetricFactory.METRIC_DICT[name]()

    @staticmethod
    def getAvailableTypes():
        ''' return all available types '''
        return MetricFactory.METRIC_DICT.keys()
