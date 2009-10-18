import unittest
import sys

sys.path.append('bin')
from umdinst import wrap

class TestIsSourceFile(unittest.TestCase):

    def testHasExtension(self):
        self.failUnless(wrap.hasextension('foo.c'))
        self.failIf(wrap.hasextension('bar'))        

    def testIsSourceFile(self):
        self.failUnless(wrap.issourcefile('foo.c'))
        self.failUnless(wrap.issourcefile('foo.cpp'))
        self.failUnless(wrap.issourcefile('foo.cc'))
        self.failUnless(wrap.issourcefile('foo.cxx'))
        self.failUnless(wrap.issourcefile('foo.C'))         
        self.failUnless(wrap.issourcefile('foo.upc'))
        self.failUnless(wrap.issourcefile('foo.f'))
        self.failUnless(wrap.issourcefile('foo.f77'))
        self.failUnless(wrap.issourcefile('foo.f90'))
        self.failIf(wrap.issourcefile('foo'))
        self.failIf(wrap.issourcefile('foo.exe'))
        self.failIf(wrap.issourcefile('foo.o'))
        self.failIf(wrap.issourcefile('foo.a'))

if __name__ == '__main__':
    unittest.main()
