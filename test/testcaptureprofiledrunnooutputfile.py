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

class TestCaptureProfiledRunNoOutputFile(unittest.TestCase):
    """Test capturing a profiled run when no output file is produced for whatever reason"""
    def setUp(self):
	# We'll just use "success", since it's a trivial program
	os.system("gcc -o success test/testsource/success.c")

	# Create a subdirectory to hold the log file
        dirname = 'testcaptureprofiledrunnooutput'
	self.logfiledir = os.path.abspath(os.path.join('.',dirname))
	os.mkdir(self.logfiledir)

	self.runprog = './success'
	self.outfile = './nonexistent-file'
	self.args = ['success']

	# Make sure the file really doesn't exist
	self.failIf(os.access(self.outfile,os.R_OK))
	

    def tearDown(self):
	# Remove the subject logfile, if it exists
	try: 
	    os.unlink(wrap.getlogfilepath(self.logfiledir))
	except OSError, e:
	    if e.errno!=errno.ENOENT:
		raise e
	os.rmdir(self.logfiledir)
	

    def testCapture(self):
	logfile = wrap.getlogfilepath(self.logfiledir)
        wrap.capture_profiled_run(runprog=self.runprog,
				  outfile=self.outfile,
				  argv=self.args,
                                  logex=logfile)

	dom = minidom.parse(wrap.getlogfilepath(self.logfiledir))
	self.job = dom.getElementsByTagName('job')[0]
	# Profile data should be just a space
	self.assertEquals(getfield(self.job,'profiledata'),' ')

if __name__ == '__main__':
    unittest.main()
