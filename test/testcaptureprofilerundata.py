import unittest
import sys
#import quopri
import base64
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring

class TestCaptureProfileRunData(unittest.TestCase):
    def setUp(self):
	timezonecheck()
        self.starttime = 1124659109
        self.endtime = self.starttime+.15
        pr = wrap.ProfileRunData(starttime = self.starttime,
                                 endtime = self.endtime,
                                 subject = 'foobar',
                                 command = "pat_hwpc -f -o test/testsource/perflog aprun -n4 ./cg 1000 1000",
                                 success = True,
                                 path = '/home/resh/lorin/src',
                                 profiledata = open('test/testsource/perflog.hwpc').read())
        xml = xmlifystring(pr.toxml())
        dom = minidom.parseString(xml)
        self.job = dom.getElementsByTagName('job')[0]

    def testSubject(self):
	self.assertEquals(getfield(self.job,'subject'),'foobar')

    def testType(self):
	self.assertEquals(self.job.attributes['type'].value,"profiled")

    def testTime(self):
	self.assertEquals(int(getfield(self.job,'time')),1124659109)

    def testTimestr(self):
	self.assertEquals(getfield(self.job,'timestr'),
			  'Sun Aug 21 17:18:29 2005')

    def testCommand(self):
	self.assertEquals(getfield(self.job,'command'),"pat_hwpc -f -o test/testsource/perflog aprun -n4 ./cg 1000 1000")

	
    def testSuccess(self):
	self.assertEquals(self.job.attributes['success'].value,'1')

	       
    def testPath(self):
        self.assertEquals(getfield(self.job,'path'),'/home/resh/lorin/src')

    def testTimeInterval(self):
        self.assertEquals(float(getfield(self.job,'time_interval')),.15)

    def testProfileData(self):
        self.assertEquals(getfield(self.job,'profiledata'),open('test/testsource/perflog.hwpc').read())


if __name__ == '__main__':
    unittest.main()
