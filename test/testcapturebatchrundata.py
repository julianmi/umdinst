import unittest
import sys
#import quopri
import base64
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring

class TestCaptureBatchRunData(unittest.TestCase):
    def setUp(self):
	# Sun Aug 21 17:18:29 2005
	timezonecheck()
        self.starttime = 1124659109
        self.endtime = self.starttime+.15
	br = wrap.BatchRunData(starttime = self.starttime,
			       endtime = self.endtime,
			       script = open('test/testsource/run.sh').read(),
			       subject = 'foobar',
			       command = "qsub -lnodes=2 test/testsource/run.sh",
			       success = True,
			       path = '/tmp')
	xml = xmlifystring(br.toxml())
	dom = minidom.parseString(xml)
	self.job = dom.getElementsByTagName('job')[0]

    def testSubject(self):
	self.assertEquals(getfield(self.job,'subject'),'foobar')

    def testType(self):
	self.assertEquals(self.job.attributes['type'].value,'batch')

    def testTime(self):
	self.assertEquals(int(getfield(self.job,'time')),1124659109)

    def testTimestr(self):
	self.assertEquals(getfield(self.job,'timestr'),
			  'Sun Aug 21 17:18:29 2005')

    def testCommand(self):
	self.assertEquals(getfield(self.job,'command'),"qsub -lnodes=2 test/testsource/run.sh")
	
    def testSuccess(self):
	self.assertEquals(self.job.attributes['success'].value,'1')
	       
    def testPath(self):
	self.assertEquals(getfield(self.job,'path'),'/tmp')

    def testTimeInterval(self):
	self.assertEquals(float(getfield(self.job,'time_interval')),
			  .15)


    def testScript(self):
	scr = """#!/usr/bin/bash
# This is an example of a test script
lamboot $PBS_NODEFILE

mpirun C myprog

lamhalt
"""
	self.assertEquals(base64.decodestring(getfield(self.job,'script')),scr)


if __name__ == '__main__':
    unittest.main()
