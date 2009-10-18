import unittest
import sys
import os
import errno
import commands
from xml.dom import minidom
from umdinst.setup import which

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring
from testcapturecompile import programcheck

### Not yet in use
class TestCaptureProfileReporter(unittest.TestCase):
    """Test the program which captures profile reports"""

    def setUp(self):
        # Uses gprof data, so make sure that the "loop"
        # program has been instrumented for gprof
        os.system("gcc -o loop test/testsource/loop.c -pg")

        # Make sure the gmon.out file is there
        self.profiledata = 'test/testsource/gmon.out'
        self.failUnless(os.access(self.profiledata,os.R_OK))
        self.runprog = which.which('gprof')
        self.failUnless(self.runprog is not None)
        self.args = 'gprof ./loop'.split()

	# Create a subdirectory to hold the log file
        dirname = 'testcaptureprofilereporter'
	self.logfiledir = os.path.abspath(os.path.join('.',dirname))
	os.mkdir(self.logfiledir)

    def tearDown(self):
	# Remove the subject logfile, if it exists
	try: 
	    os.unlink(wrap.getlogfilepath(self.logfiledir))
	except OSError, e:
	    if e.errno!=errno.ENOENT:
		raise e
	os.rmdir(self.logfiledir)
        
        
    def testCapture(self):

        # gprof will output a lot to standard out, which we will redirect
        # to /dev/null 
        stdout = sys.stdout

        try:
            sys.stdout.flush()
            sys.stdout = open('/dev/null','w')
            logfile = wrap.getlogfilepath(self.logfiledir)
            wrap.capture_profile_report(self.runprog,
                                        argv=self.args,
                                        logex=logfile)
        finally:
            sys.stdout = stdout

        logfile = wrap.getlogfilepath(self.logfiledir)
        dom = minidom.parseString(wrap.printable(open(logfile).read()))
        report = dom.getElementsByTagName('profile_report')[0]
        # Contents should be the same as contents of running gprof
        gprof_output = commands.getoutput('gprof ./loop')
        self.assertEquals(getfield(report,'contents'),wrap.printable(gprof_output))


if __name__ == '__main__':
    unittest.main()
