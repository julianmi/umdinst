import unittest
import sys
import socket

sys.path.append('bin')
from umdinst import wrap

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Determine the correct login name based on the machine identity"""
        hostname = socket.gethostname()
	logins = {'CANADA':'lorin',
		  'care.cs.umd.edu':'lorin',
		  'farnsworth.local':'lorin',
		  'Stacys-Computer.local':'lorin',
		  'localhost.localdomain':'taiga',
                  }
	try:
	    self.login = logins[hostname]
	except KeyError:
            raise ValueError, "Unknown hostname: " + hostname

    def testLogin(self):
        """Test if can retrieve login name"""
        # This is actually quite difficult
        self.assertEquals(wrap.getlogin(),self.login)

    def testLogfileName(self):
        """Test the function that determines the logfile path"""
        logfiledir = '/foo/bar/baz'

        self.assertEquals(wrap.getlogfilepath(logfiledir),
                          '/foo/bar/baz/' + wrap.getlogin() + '.log')
