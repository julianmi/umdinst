import unittest
import sys
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck

class TestCaptureInteractiveRunData(unittest.TestCase):
    def setUp(self):
	timezonecheck()
        # Sun Aug 21 17:18:29 2005
        self.starttime = 1124659109
        self.endtime = self.starttime+.15
	self.ir = wrap.InteractiveRunData(starttime = self.starttime,
					  endtime = self.endtime,
					  subject = 'foobar',
					  command = "mpirun C ./life 100 100 100 out.txt",
					  success = True,
					  path = '/foo/bar/baz')
	self.xml = self.ir.toxml()
	dom = minidom.parseString(self.xml)
        self.assertEquals(dom.documentElement.tagName,'job')
        self.irnode = dom.getElementsByTagName('job')[0]

    def testType(self):
	self.assertEquals(self.irnode.attributes['type'].value,'interactive')

    def testSubject(self):
	self.assertEquals(getfield(self.irnode,'subject'),'foobar')

    def testTime(self):
        self.assertEquals(int(getfield(self.irnode,'time')),
                          1124659109)
    def testTimestr(self):
        self.assertEquals(getfield(self.irnode,'timestr'),
                          'Sun Aug 21 17:18:29 2005')
    def testTimeInterval(self):
	self.assertEquals(float(getfield(self.irnode,'time_interval')),
			  .15)
    def testSuccess(self):
	self.assertEquals(int(self.irnode.attributes['success'].value),1)

    def testArgs(self):
	self.assertEquals(getfield(self.irnode,'command'),'mpirun C ./life 100 100 100 out.txt')

    def testPath(self):
	self.assertEquals(getfield(self.irnode,'path'),'/foo/bar/baz')


if __name__ == '__main__':
    unittest.main()
