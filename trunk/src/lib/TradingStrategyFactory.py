'''
Created on Feb 26, 2011

@author: ppa
'''
def fixAmountPerPeriod(dateValues, interval):
    ''' fix amount investment for each time period'''
    amount = float(100)
    share = sum([amount/dateValues[index].value for index in range(len(dateValues)/interval)])
    return share * dateValues[-1].value / (amount * len(dateValues) / interval)

def fixAmountPerPeriodWithAddtionWhenDrop(dateValues, intervalSlidingWindow):
    ''' fix amount investment for each time period'''
    amount = float(100)
    interval = intervalSlidingWindow[0]
    slidingWindow = intervalSlidingWindow[1]
    fixShare = sum([amount/dateValues[index].value for index in range(len(dateValues)/interval)])
    #adjustShare = sum([amount/dateValues[index].value for index in range(len(dateValues)) if index >= slidingWindow and min([dateValue.value for dateValue in dateValues[index-slidingWindow:index+1]]) == dateValues[index]])
    adjustShare = sum([amount/dateValues[index].value for index in range(len(dateValues)) if index >= slidingWindow and min([dateValue.value for dateValue in dateValues[index-slidingWindow:index+1]]) == dateValues[index].value])
    share = adjustShare + fixShare
    return share * dateValues[-1].value / (amount * len(dateValues) / interval)

def adjustFixAmountPerPeriod(dateValues, intervalSlidingWindow):
    ''' fix amount investment for each time period'''
    amount = float(100)
    interval = intervalSlidingWindow[0]
    slidingWindow = intervalSlidingWindow[1]
    share = 0
    for frame in range(len(dateValues)/interval):
        bought = False
        for i in range(interval):
            index = frame*interval + i
            if index >= slidingWindow and min([dateValue.value for dateValue in dateValues[index-slidingWindow:index+1]]) == dateValues[index].value:
                share += amount/dateValues[index].value
                bought = True
                break

        if not bought:
            share += amount/dateValues[(frame+1) * interval - 1].value

    return share * dateValues[-1].value / (amount * len(dateValues) / interval)

class TradingStrategyFactory():
    ''' Factory method for trading Strategies '''
    strategyDict = {'fixAmountPerPeriod': fixAmountPerPeriod,
                    'adjustFixAmountPerPeriod': adjustFixAmountPerPeriod,
                    'fixAmountPerPeriodWithAddtionWhenDrop': fixAmountPerPeriodWithAddtionWhenDrop}

    def __init__(self, strategyName):
        ''' constructor '''
        if strategyName not in TradingStrategyFactory.strategyDict:
            raise Exception("strategyName %s not found" % strategyName)

        self.strategy = TradingStrategyFactory.strategyDict[strategyName]

    def calculateReturn(self, dateValues, data):
        return self.strategy(dateValues, data)

    def addStrategy(self, strategyName, strategy):
        TradingStrategyFactory[strategyName] = strategy

if __name__ == '__main__':
    from lib.DataType import DateValueType
    tradingStrategyFactory = TradingStrategyFactory('fixAmountPerPeriod')
    print tradingStrategyFactory.calculateReturn([DateValueType(1, 10.0), DateValueType(2, 20.0), DateValueType(3, 25.0), DateValueType(4, 50.0)], 1)
