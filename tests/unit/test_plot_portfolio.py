'''
Created on May 6, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.lib.plotPortfolio import PlotPortfolio

class testPlotPortfolio(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPlotSaveFig(self):
        plotPortfolio = PlotPortfolio([{'label':'bond', 'return':0.08, 'deviation':12, 'cov':72},
                                       {'label':'stock', 'return':0.13, 'deviation':20, 'cov':72}])
        plotPortfolio.plot()
        plotPortfolio.savefig(os.path.join( os.path.dirname( os.path.dirname(os.path.abspath(__file__)) ),
                                            'output', 'portFolio.png' ))