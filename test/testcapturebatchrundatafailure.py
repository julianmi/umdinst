import unittest
import sys
#import quopri
import base64
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring

class TestCaptureBatchRunDataFailure(unittest.TestCase):
    def setUp(self):
	# Sun Aug 21 17:18:29 2005
	timezonecheck()
        self.starttime = 1124659109
        self.endtime = self.starttime+.15
	br = wrap.BatchRunData(starttime = self.starttime,
			       endtime = self.endtime,
			       script = 'run.sh',
			       subject = 'foobar',
			       command = "qsub -lnodes=2 run.sh",
			       success = False,
			       path = '/tmp')
	xml = xmlifystring(br.toxml())
	dom = minidom.parseString(xml)
	self.job = dom.getElementsByTagName('job')[0]

    def testJob(self):
	self.assertEquals(self.job.attributes['type'].value,'batch')

    def testSuccess(self):
	self.assertEquals(self.job.attributes['success'].value,'0')


if __name__ == '__main__':
    unittest.main()
