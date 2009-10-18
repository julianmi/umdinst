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

class TestCaptureProfiledRun(unittest.TestCase):
    def setUp(self):
        # Build the "loop.c" program 
        os.system("gcc -g -o loop test/testsource/loop.c")

        # Create a subdirectory to hold the log file
        dirname = 'testcaptureprofiledrun'
	self.logfiledir = os.path.abspath(os.path.join('.',dirname))
        try:
            os.mkdir(self.logfiledir)
        except OSError:
            pass

	# The profiler used depends on the OS
	# Linux: valgirnd
	# OS X: shark
	osname = commands.getoutput('uname')
	if osname=='Linux':
	    # Generates a file called cachegrind.out
	    self.runprog = 'test/testsource/valgrind.py'
            os.chmod(self.runprog, 0755)
	    self.args = 'valgrind --tool=cachegrind ./loop'.split()
	    self.outfile = 'cachegrind.out'
	elif osname=='Darwin':
	    # Delete all files that start with session_
	    for fname in os.listdir('.'):
		if fname.startswith('session_'):
		    os.unlink(fname)
	    
	    self.runprog = 'test/testsource/shark.py'
	    self.args = 'shark -G -i ./loop'.split()
	    self.outfile = 'session_001-report.txt'
            
        programcheck(self.runprog)

	logfile = wrap.getlogfilepath(self.logfiledir)
        wrap.capture_profiled_run(runprog=self.runprog,
				  outfile=self.outfile,
				  argv=self.args,
                                  logex=logfile)
	dom = minidom.parse(wrap.getlogfilepath(self.logfiledir))
	self.job = dom.getElementsByTagName('job')[0]

    def tearDown(self):
	# Remove the subject logfile, if it exists
	try: 
	    os.unlink(wrap.getlogfilepath(self.logfiledir))
	except OSError, e:
	    if e.errno!=errno.ENOENT:
		raise e
	os.rmdir(self.logfiledir)

    def testNodeIsAProfiledJob(self):
	self.assertEquals(self.job.attributes['type'].value,'profiled')

    def testSuccess(self):
	self.assertEquals(self.job.attributes['success'].value,'1')

    def testProfileData(self):
	self.assertEquals(getfield(self.job,'profiledata'),open(self.outfile).read())


if __name__ == '__main__':
    unittest.main()
