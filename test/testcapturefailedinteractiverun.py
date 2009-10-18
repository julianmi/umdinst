import unittest
import sys
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck

class TestCaptureFailedInteractiveRun(unittest.TestCase):

    def setUp(self):
        # Sun Aug 21 17:18:29 2005
	timezonecheck()
        self.starttime = 1124659109
        self.endtime = self.starttime+5.5
	self.ir = wrap.InteractiveRunData(starttime = self.starttime,
					  endtime = self.endtime,
					  subject = 'barbaz',
					  command = 'mpirun C badprog',
					  success = False,
					  path = "/user/barbaz")
    def testFailure(self):
	dom = minidom.parseString(self.ir.toxml())
	irnode = dom.getElementsByTagName('job')[0]
	self.assertEquals(int(irnode.attributes['success'].value),0)


if __name__ == '__main__':
    unittest.main()
