'''
Created on Feb 20, 2011

@author: ppa
'''
from matplotlib import pyplot
import math

class PlotPortfolio(object):
    ''' plot portfolio curve. only two are supported '''
    def __init__(self, labelReturnDeviations):
        ''' constructor '''
        self.labelReturnDeviations = labelReturnDeviations
        pyplot.rc('axes', grid=True)
        pyplot.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

    def plot(self):
        ''' get average '''
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

        pyplot.show()

if __name__ == '__main__':
    plotPortfolio = PlotPortfolio([{'label':'bond', 'return':0.08, 'deviation':12, 'cov':72},
                                   {'label':'stock', 'return':0.13, 'deviation':20, 'cov':72}])
    plotPortfolio.plot()