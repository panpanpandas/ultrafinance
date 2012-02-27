'''
Created on Jan 08, 2012

@author: ppa
'''
import unittest
import os

from ultrafinance.lib.util import capitalize, importClass

class Test_util(object):
    ''' test class for importClass test '''
    pass

class Class1(object):
    ''' test class for importClass test '''
    pass

class testUtil(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCapitalize(self):
        ''' test capitalize() '''
        self.assertEquals("_123abc", capitalize("_123abc"))
        self.assertEquals("Abc123", capitalize("abc123"))
        self.assertEquals("A", capitalize("a"))
        self.assertEquals("", capitalize(""))

    def testImportClass(self):
        ''' test importClass() '''
        curDir = os.path.dirname(os.path.abspath(__file__))
        cl1 = importClass(curDir, "test_util")
        self.assertNotEquals(None, cl1)

        cl2 = importClass(curDir, "test_util", 'Class1')
        self.assertNotEquals(None, cl2)

        self.assertRaises(AttributeError, importClass, curDir, "test_util", 'Class2')
