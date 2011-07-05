'''
Created on July 4, 2011

@author: ppa
copied from http://da44en.wordpress.com/2002/11/22/using-distutils/
'''
from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin, walk
import os

class TestCommand(Command):
    ''' test command for setup.py '''
    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        testfiles = []
        for t in glob(pjoin(self._dir, 'tests', 'unit', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', 'unit', splitext(basename(t))[0]])
                )

        print testfiles
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 1)
        t.run(tests)

class CleanCommand(Command):
    ''' clean command for setup.py '''
    user_options = [ ]

    def initialize_options(self):
        self._clean_me = [ ]
        for root, dirs, files in os.walk('.'):
            for f in files:
                if f.endswith('.pyc'):
                    self._clean_me.append(pjoin(root, f))

    def finalize_options(self):
        pass

    def run(self):
        for clean_me in self._clean_me:
            try:
                os.unlink(clean_me)
            except:
                pass