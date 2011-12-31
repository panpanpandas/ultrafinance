'''
Created on Nov 27, 2011

@author: ppa
'''
import unittest
from ultrafinance.dam.googleDAM import GoogleDAM

class testGoogleDam(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadQuotes(self):
        dam = GoogleDAM()
        dam.setSymbol('NASDAQ:EBAY')
        data = dam.readQuotes('20110101', '20110110')
        print data
        self.assertNotEquals(len(data), 0)

    def testReadTicks(self):
        dam = GoogleDAM()
        dam.setSymbol('EBAY')
        data = dam.readTicks('20111120', '20111201')
        print data
        self.assertNotEquals(len(data), 0)
