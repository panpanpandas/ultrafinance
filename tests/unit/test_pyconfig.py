'''
Created on Nov 30, 2011

@author: ppa
'''
import unittest
from ultrafinance.config.pyConfig import PyConfig

class testPyConfig(unittest.TestCase):
    def setUp(self):
        self.config = PyConfig()
        self.config.setSource("test.ini")

    def tearDown(self):
        pass

    def testGetSession(self):
        keyValues = self.config.getSection("app_main")
        print keyValues
        self.assertNotEquals(0, len(keyValues))

        if not keyValues['field3']:
            print "field3 is None"

    def testGetOption(self):
        option = self.config.getOption("log", "file")
        print option
        self.assertEquals("test.log", option)
