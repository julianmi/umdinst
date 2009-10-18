import unittest
import sys
import os
import errno
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring

def programcheck(progpath):
    if not os.path.exists(progpath):
	raise ValueError, "%s is not present on this system, causing this test to fail" % progpath

def xmlifyfile(f):
    """Load a logfile and convert it to valid XML"""
    return xmlifystring(open(f).read())

class TestCaptureCompile(unittest.TestCase):
    def setUp(self):
	# Create a subdir to hold the log file
	dirname = 'testcompile'
	self.logfiledir = os.path.abspath(os.path.join('.',dirname))
	os.mkdir(self.logfiledir)
	self.compiler = '/usr/bin/gcc'
	# Sanity check: make sure we can use this program
	programcheck(self.compiler)

    def tearDown(self):
	# Remove the subject logfile, if it exists
	try: 
	    os.unlink(wrap.getlogfilepath(self.logfiledir))
	except OSError, e:
	    if e.errno!=errno.ENOENT:
		raise e
	os.rmdir(self.logfiledir)

    def testCapture(self):
	command = 'gcc -c test/testsource/outerr.c'
	args = command.split()
	logfile = wrap.getlogfilepath(self.logfiledir)
	wrap.capture_compile(self.compiler,args,logex=logfile)
        xml = xmlifyfile(logfile)
        dom = minidom.parseString(xml)
            
	# Just check if it stored the fields
	self.assertEquals(dom.documentElement.tagName,'log')
	self.assertEquals(len(dom.getElementsByTagName('sourcefile')),1)
	self.assertEquals(len(dom.getElementsByTagName('headerfile')),1)	


if __name__ == '__main__':
    unittest.main()
