import unittest
import sys
import os
import errno
import commands
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring
from testcapturecompile import programcheck

def createemptyfile(fname):
    """Creates an empty file. Throws an exception if the file alrady exists"""
    if os.access(fname,os.R_OK):
        raise ValueError,"File already exists"
    f = open(fname,'w')
    f.close()

class TestIdentifySourcefiles(unittest.TestCase):
    def setUp(self):
        # Create some source files
        createemptyfile("foo.c")
        createemptyfile("bar.cpp")
        createemptyfile("baz.upc")
        createemptyfile("quux.f77")
        self.args = "foo.c bar.cpp baz.upc quux.f77 others x.o y.exe -Dgoomba".split()
        self.argsdasho = "foo.c -o baz.upc bar.cpp".split()
    
    def testBasic(self):
        files = wrap.identify_sourcefiles(self.args)
        self.assertEquals(files,
                          ['foo.c','bar.cpp','baz.upc','quux.f77'])

    def testWithDashO(self):
        files = wrap.identify_sourcefiles(self.argsdasho)
        self.assertEquals(files,['foo.c','bar.cpp'])

    def tearDown(self):
        os.remove("foo.c")
        os.remove("bar.cpp")
        os.remove("baz.upc")
        os.remove("quux.f77")

if __name__ == '__main__':
    unittest.main()
