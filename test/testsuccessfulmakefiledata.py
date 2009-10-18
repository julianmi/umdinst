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

# This hasn't been implemented yet!
class TestSuccessfulMakefileData(unittest.TestCase):
    def setUp(self):
        # Sat Aug 13 19:04:24 2005
	timezonecheck()
        self.starttime = 1123974264
        self.endtime = self.starttime+30.5
	self.mf = wrap.MakeData(self.starttime,
			  self.endtime,
			  subject = 'foofoo',
			  command = "make",
			  success = True,
			  path = '/Users/lorin/dev')
	xml = xmlifystring(self.mf.toxml())
	self.dom = minidom.parseString(xml)

    def testMakeNode(self):
	self.assertEquals(len(self.dom.getElementsByTagName('make')),1)


if __name__ == '__main__':
    unittest.main()
