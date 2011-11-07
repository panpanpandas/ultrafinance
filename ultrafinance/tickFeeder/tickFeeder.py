'''
Created on Nov 6, 2011

@author: ppa
'''
from ultrafinance.lib.errors import UfException, Errors
from threading import Thread

class TickFeeder:
    ''' constructor
        no tick operation should take more that 0.5 second
        threadMaxFails indicates how many times thread for a subscriber can timeout,
        if it exceeds, them unregister that subscriber
        TODO: read from config
    '''
    def __init__(self, subManager, threadTimeout = 0.5, threadMaxFail = 10):
        self.__subs = {} # securityIds: sub
        self.__subManger = subManager
        self.__fails = {} # subId: threadFails

    def validateSecurityIds(self, securityIds):
        ''' validate sercurity ids '''
        pass

    def validate(self, subId):
        ''' validate subsriber '''
        sub = self.__subManger.getSubById(subId)
        # only one subscriber should be found
        if sub is None:
            raise UfException(Errors.FEEDER_INVALID_ERROR,
                              'subscriber are not found for subId %s' % subId)

        securityIds, rules = sub.subRules()
        #check whether securityIds exist
        self.validateSecurityIds(securityIds)

        return securityIds, sub

    def register(self, subId):
        ''' register a subscriber
            rule is not used for now
        '''
        securityIds, sub = self.validate(subId)

        self.__subs[securityIds] = sub
        self.__fails[securityIds] = 0

    def unregister(self, subId):
        ''' unregiester'''
        securityIds, sub = self.validate(subId)

        if securityIds in self.__subs:
            del self.__subs[securityIds]

        if subId in self.__fails:
            del self.__fails[subId]

    def execute(self):
        ''' execute func '''
        # call data handler class to find all securiyIds as Input
        # for tick in time:
        #   save all ticks
        #   for securityIds in self.__subs.keys():
        #       thread = pubTicks(ticks, sub)
        #       thread.join()
        pass

    def pubTicks(self, ticks, sub):
        ''' publish ticks to sub '''
        thread = Thread(target = sub.comsume, args=(ticks, ))
        thread.start()
        return thread

    def getSubs(self):
        ''' get all subs, should not be used to change any sub '''
        return self.__subs

    def getSubManager(self):
        ''' get subManager '''
        return self.__subManger
