import unittest
import sys
#import quopri
import base64
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck

class TestEmptyCompileData(unittest.TestCase):
    def setUp(self):
        # Sun Aug 21 17:18:29 2005
	timezonecheck()
        self.starttime = 1124659109
        self.endtime = self.starttime+8
        self.cd = wrap.CompileData(self.starttime,
                                   self.endtime,
                                   sourcefiles= [],
                                   subject = 'fifi',
                                   command = 'gcc',
                                   success = False,
				   path = '/tmp')

    def testToXml(self):
        dom = minidom.parseString(self.cd.toxml())
        self.assertEquals(dom.documentElement.tagName,'compile')
        self.assertEquals(int(getfield(dom,'time')),1124659109)
        self.assertEquals(getfield(dom,'timestr'),'Sun Aug 21 17:18:29 2005')
        self.assertEquals(getfield(dom,'subject'),'fifi')
        self.assertEquals(getfield(dom,'command'),'gcc')
        self.assertEquals(int(getfield(dom,'time_interval')),8)

if __name__ == '__main__':
    unittest.main()
