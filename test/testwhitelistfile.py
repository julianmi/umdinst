import unittest
import sys
import os

sys.path.append('bin')
from umdinst import wrap

class TestWhitelistFile(unittest.TestCase):
    def setUp(self):
	self.fname = 'whitelistfile.txt'
	f = open(self.fname,'w')
	f.write('foo\nbar\nbaz\n')
	f.close()
	
    def tearDown(self):
	os.unlink(self.fname)

    def testPresent1(self):
	self.assertEquals(wrap.is_in_whitelist('foo',self.fname),True)

    def testPresent2(self):
	self.assertEquals(wrap.is_in_whitelist('bar',self.fname),True)

    def testPresent3(self):
	self.assertEquals(wrap.is_in_whitelist('baz',self.fname),True)

    def testNotPresent(self):
	self.assertEquals(wrap.is_in_whitelist('quux',self.fname),False)
	

if __name__ == '__main__':
    unittest.main()
