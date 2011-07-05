'''
Created on May 6, 2011

@author: ppa
By Gary Robinson, grobinson@flyfi.com
'''
import unittest
import time
from ultrafinance.lib.designPattern.singleton import *

class testSingleton(unittest.TestCase):
        def testReturnsSameObject(self):
            """
            Demonstrates normal use -- just call getInstance and it returns a singleton instance
            """

            class A(Singleton):
                def __init__(self):
                    super(A, self).__init__()

            a1 = A.getInstance()
            a2 = A.getInstance()
            self.assertEquals(id(a1), id(a2))

        def testInstantiateWithMultiArgConstructor(self):
            """
            If the singleton needs args to construct, include them in the first
            call to get instances.
            """

            class B(Singleton):

                def __init__(self, arg1, arg2):
                    super(B, self).__init__()
                    self.arg1 = arg1
                    self.arg2 = arg2

            b1 = B.getInstance('arg1 value', 'arg2 value')
            b2 = B.getInstance()
            self.assertEquals(b1.arg1, 'arg1 value')
            self.assertEquals(b1.arg2, 'arg2 value')
            self.assertEquals(id(b1), id(b2))

        def testInstantiateWithKeywordArg(self):

            class B(Singleton):

                def __init__(self, arg1=5):
                    super(B, self).__init__()
                    self.arg1 = arg1

            b1 = B.getInstance('arg1 value')
            b2 = B.getInstance()
            self.assertEquals(b1.arg1, 'arg1 value')
            self.assertEquals(id(b1), id(b2))

        def testTryToInstantiateWithoutNeededArgs(self):

            class B(Singleton):

                def __init__(self, arg1, arg2):
                    super(B, self).__init__()
                    self.arg1 = arg1
                    self.arg2 = arg2

            self.assertRaises(SingletonException, B.getInstance)

        def testPassTypeErrorIfAllArgsThere(self):
            """
            Make sure the test for capturing missing args doesn't interfere with a normal TypeError.
            """
            class B(Singleton):

                def __init__(self, arg1, arg2):
                    super(B, self).__init__()
                    self.arg1 = arg1
                    self.arg2 = arg2
                    raise TypeError, 'some type error'

            self.assertRaises(TypeError, B.getInstance, 1, 2)

        def testTryToInstantiateWithoutGetInstance(self):
            """
            Demonstrates that singletons can ONLY be instantiated through
            getInstance, as long as they call Singleton.__init__ during construction.

            If this check is not required, you don't need to call Singleton.__init__().
            """

            class A(Singleton):
                def __init__(self):
                    super(A, self).__init__()

            self.assertRaises(SingletonException, A)

        def testDontAllowNew(self):

            def instantiatedAnIllegalClass():
                class A(Singleton):
                    def __init__(self):
                        super(A, self).__init__()

                    def __new__(metaclass, strName, tupBases, dct):
                        return super(MetaSingleton, metaclass).__new__(metaclass, strName, tupBases, dct)

            self.assertRaises(SingletonException, instantiatedAnIllegalClass)


        def testDontAllowArgsAfterConstruction(self):
            class B(Singleton):

                def __init__(self, arg1, arg2):
                    super(B, self).__init__()
                    self.arg1 = arg1
                    self.arg2 = arg2

            B.getInstance('arg1 value', 'arg2 value')
            self.assertRaises(SingletonException, B, 'arg1 value', 'arg2 value')

        def test_forgetClassInstanceReferenceForTesting(self):
            class A(Singleton):
                def __init__(self):
                    super(A, self).__init__()
            class B(A):
                def __init__(self):
                    super(B, self).__init__()

            # check that changing the class after forgetting the instance produces
            # an instance of the new class
            a = A.getInstance()
            assert a.__class__.__name__ == 'A'
            A._forgetClassInstanceReferenceForTesting()
            b = B.getInstance()
            assert b.__class__.__name__ == 'B'

            # check that invoking the 'forget' on a subclass still deletes the instance
            B._forgetClassInstanceReferenceForTesting()
            a = A.getInstance()
            B._forgetClassInstanceReferenceForTesting()
            b = B.getInstance()
            assert b.__class__.__name__ == 'B'

        def test_forgetAllSingletons(self):
            # Should work if there are no singletons
            forgetAllSingletons()

            class A(Singleton):
                ciInitCount = 0
                def __init__(self):
                    super(A, self).__init__()
                    A.ciInitCount += 1

            A.getInstance()
            self.assertEqual(A.ciInitCount, 1)

            A.getInstance()
            self.assertEqual(A.ciInitCount, 1)

            forgetAllSingletons()
            A.getInstance()
            self.assertEqual(A.ciInitCount, 2)

        def test_threadedCreation(self):
            # Check that only one Singleton is created even if multiple
            #  threads try at the same time.  If fails, would see assert in _addSingleton
            class Test_Singleton(Singleton):
                def __init__(self):
                    super(Test_Singleton, self).__init__()

            class Test_SingletonThread(threading.Thread):
                def __init__(self, fTargetTime):
                    super(Test_SingletonThread, self).__init__()
                    self._fTargetTime = fTargetTime
                    self._eException = None

                def run(self):
                    try:
                        fSleepTime =  self._fTargetTime - time.time()
                        if fSleepTime > 0:
                            time.sleep(fSleepTime)
                        Test_Singleton.getInstance()
                    except Exception, e:
                        self._eException = e

            fTargetTime = time.time() + 0.1
            lstThreads = []
            for _ in xrange(100):
                t = Test_SingletonThread(fTargetTime)
                t.start()
                lstThreads.append(t)
            eException = None
            for t in lstThreads:
                t.join()
                if t._eException and not eException:
                    eException = t._eException
            if eException:
                raise eException

        def testNoInit(self):
            """
            Demonstrates use with a class not defining __init__
            """

            class A(Singleton):
                pass

                #INTENTIONALLY UNDEFINED:
                #def __init__(self):
                #    super(A, self).__init__()

            A.getInstance() #Make sure no exception is raised

        def testMultipleGetInstancesWithArgs(self):

            class A(Singleton):

                ignoreSubsequent = True

                def __init__(self, a, b=1):
                    pass

            a1 = A.getInstance(1)
            a2 = A.getInstance(2) # ignores the second call because of ignoreSubsequent

            class B(Singleton):

                def __init__(self, a, b=1):
                    pass

            b1 = B.getInstance(1)
            self.assertRaises(SingletonException, B.getInstance, 2) # No ignoreSubsequent included

            class C(Singleton):

                def __init__(self, a=1):
                    pass

            c1 = C.getInstance(a=1)
            self.assertRaises(SingletonException, C.getInstance, a=2) # No ignoreSubsequent included

        def testInheritance(self):
            """
            It's sometimes said that you can't subclass a singleton (see, for instance,
            http://steve.yegge.googlepages.com/singleton-considered-stupid point e). This
            test shows that at least rudimentary subclassing works fine for us.
            """

            class A(Singleton):

                def setX(self, x):
                    self.x = x

                def setZ(self, z):
                    raise NotImplementedError

            class B(A):

                def setX(self, x):
                    self.x = -x

                def setY(self, y):
                    self.y = y

            a = A.getInstance()
            a.setX(5)
            b = B.getInstance()
            b.setX(5)
            b.setY(50)
            self.assertEqual((a.x, b.x, b.y), (5, -5, 50))
            self.assertRaises(AttributeError, eval, 'a.setY', {}, locals())
            self.assertRaises(NotImplementedError, b.setZ, 500)