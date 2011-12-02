'''
Created on July 30, 2011

@author: ppa
please refer to http://code.activestate.com/recipes/131499-observer-pattern/
'''
import unittest
from ultrafinance.lib.designPattern.observable import Observable

class Data(Observable):
    def __init__(self, name=''):
        Observable.__init__(self)
        self.name = name
        self.data = 0

    def setData(self, data):
        self.data = data
        self.notify()

    def getData(self):
        return self.data


class HexViewer:
    def __init__(self):
        self.data = 0

    def update(self, subject):
        self.data = subject.data
        print 'HexViewer: Subject %s has data 0x%x' % (subject.name, subject.getData())

class DecimalViewer:
    def __init__(self):
        self.data = 0

    def update(self, subject):
        self.data = subject.data
        print 'DecimalViewer: Subject %s has data %d' % (subject.name, subject.getData())

class testObservable(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAttachAndUnattach(self):
        data1 = Data('Data 1')
        view1 = DecimalViewer()
        view2 = HexViewer()
        data1.attach(view1)
        data1.attach(view2)

        print "Setting Data 1 = 10"
        data1.setData(10)
        self.assertEquals(10, data1.data)
        self.assertEquals(10, view1.data)
        self.assertEquals(10, view2.data)
        print "Setting Data 1 = 3"
        data1.setData(3)
        self.assertEquals(3, data1.data)
        self.assertEquals(3, view1.data)
        self.assertEquals(3, view2.data)
        print "Detach HexViewer from data1"
        data1.detach(view2)
        print "Setting Data 1 = 10"
        data1.setData(10)
        self.assertEquals(10, data1.data)
        self.assertEquals(10, view1.data)
        self.assertEquals(3, view2.data)