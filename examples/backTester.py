'''
Created on Dec 3, 2011

@author: ppa
'''
from ultrafinance.module.backTester import BackTester

if __name__ == "__main__":

    backTester = BackTester("backtest_smaPortfolio.ini", startTickDate = 20101010, startTradeDate =  20111220)
    backTester.setup()
    backTester.runTests()
    backTester.printMetrics()
