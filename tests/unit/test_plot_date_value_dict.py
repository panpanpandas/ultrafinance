'''
Created on May 6, 2011

@author: ppa
'''
import unittest

from ultrafinance.lib.plotDateValueDict import PlotDateValueDict

class testPlotDateValueDict(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPlotOneDateValue(self):
        stock1 = [('20101101', 1), ('20101102', 2), ('20101103', 3)]
        stock2 = [('20101101', 3), ('20101102', 2), ('20101103', 1)]
        stock3 = [('20101101', 1), ('20101102', 2), ('20101103', 3)]
        stock4 = [('20101101', 3), ('20101102', 2), ('20101103', 1)]
        dateValues = {'testStock1': stock1, 'testStock2': stock2, 'testStock3': stock3, 'testStock4': stock4}
        p = PlotDateValueDict(dateValues, '%Y%m%d')
        p.plot()
