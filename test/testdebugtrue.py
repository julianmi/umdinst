import unittest
import sys
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import timezonecheck, xmlifystring


class TestDebugTrue(unittest.TestCase):
    def setUp(self):
	        # Sat Aug 13 19:04:24 2005
	timezonecheck()
        self.starttime = 1123974264
        self.endtime = self.starttime+30.5
        self.sourcefiles = ['test/testsource/outerr.c']
        self.cd = wrap.CompileData(self.starttime,
				   self.endtime,
				   self.sourcefiles,
				   subject = 'borat',
				   command = 'CC -c test/testsource/outerr.c',
				   success = True,
				   path = '/tmp',
				   debugging=True)
        xml =  xmlifystring(self.cd.toxml())
        self.dom = minidom.parseString(xml)
        self.cnode = self.dom.getElementsByTagName('compile')[0]


    def testDebugTrue(self):
	self.assertEquals(self.cnode.attributes['debugging'].value,'1')


if __name__ == '__main__':
    unittest.main()
