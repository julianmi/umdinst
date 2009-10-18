import unittest
import sys
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck

class TestRecordAbsolutePath(unittest.TestCase):
    # Test that the program captures the absolute path
    def setUp(self):
	# Sat Aug 13 19:04:24 2005
	timezonecheck()
        self.starttime = 1123974264
        self.endtime = self.starttime+30
        self.sourcefiles = ['test/testsource/sub/foo.c']
        self.cd = wrap.CompileData(self.starttime,
                                   self.endtime,
                                   self.sourcefiles,
                                   subject = 'mike',
                                   command = 'gcc -c test/testsource/sub/foo.c',
                                   success = True,
				   path = '/foo/bar/baz')

	
    def testRecordingPath(self):
        xml =  '\n'.join(["<log>,",
                          self.cd.toxml(),
                          "</log>"])
	dom = minidom.parseString(xml)
	sfnode = dom.getElementsByTagName('sourcefile')[0]
	self.assertEquals(getfield(sfnode,'path'),'/foo/bar/baz')


if __name__ == '__main__':
    unittest.main()
