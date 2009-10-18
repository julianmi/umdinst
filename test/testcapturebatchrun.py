import unittest
import sys
import os
import errno
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring
from testcapturecompile import programcheck

class TestCaptureBatchRun(unittest.TestCase):
    def setUp(self):
	# Create a subdirectory to hold the log file
	dirname = 'testcapturebatchrun'
	self.logfiledir = os.path.abspath(os.path.join('.',dirname))
	os.mkdir(self.logfiledir)
	self.runprog = '/bin/echo'
	programcheck(self.runprog)

    def tearDown(self):
	# Remove the subject logfile, if it exists
	try: 
	    os.unlink(wrap.getlogfilepath(self.logfiledir))
	except OSError, e:
	    if e.errno!=2:
		raise e
	os.rmdir(self.logfiledir)
    
    def testCapture(self):
	logfile = wrap.getlogfilepath(self.logfiledir)
	wrap.capture_batch_run(self.runprog,logex=logfile)
	dom = minidom.parse(logfile)
	self.assertEquals(dom.documentElement.tagName,'job')

if __name__ == '__main__':
    unittest.main()
