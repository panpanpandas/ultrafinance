'''
Created on Feb 20, 2011

@author: ppa
'''
from matplotlib import pyplot
import math
from ultrafinance.lib.errors import ufException, Errors

import logging
LOG = logging.getLogger(__name__)

class PlotPortfolio(object):
    ''' plot portfolio curve. only two are supported '''
    def __init__(self, labelReturnDeviations):
        ''' constructor '''
        self.labelReturnDeviations = labelReturnDeviations
        pyplot.rc('axes', grid=True)
        pyplot.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

    def plot(self):
        ''' plot '''
        try:
            returns = []
            deviations = []
            portfolio1 = self.labelReturnDeviations[0]
            portfolio2 = self.labelReturnDeviations[1]

            for i in range(100):
                returns.append(portfolio1['return']*i/100 + portfolio2['return']*(100-i)/100)
                deviations.append(pow(portfolio1['deviation']*i/100, 2) + pow(portfolio2['deviation']*(100-i)/100, 2) + 2*(i/100)*((100-i)/100)*portfolio1['cov'])

            pyplot.plot([math.sqrt(deviation) for deviation in deviations], returns,'b-')
            pyplot.ylabel('Returns')
            pyplot.xlabel('Deviations')

        except ufException as excep:
            raise excep
        except BaseException as excep:
            raise ufException(Errors.UNKNOWN_ERROR, "plotPortfolio.plot got unknown error %s" % excep)

    def show(self):
        '''
        show the graph.
        NOTICE: after show(), You can't do savefig() anymore.
        This is a known bug: http://code.google.com/p/ultra-finance/issues/detail?id=3
        '''
        pyplot.show()

    def savefig(self, fileName):
        LOG.debug('Save portfolio to %s' % fileName)
        pyplot.savefig(fileName)