import unittest
import sys
import os

sys.path.append('bin')
from umdinst import wrap

class TestRunProgram(unittest.TestCase):
    def setUp(self):
	self.tempfilename = 'emptyfile' # This is in createfile.sh
	self.failIf(os.path.exists(self.tempfilename))

        # Find the "touch" program
        if os.path.exists('/usr/bin/touch'):
            self.touchprog = '/usr/bin/touch'
        elif os.path.exists('/bin/touch'):
            self.touchprog = '/bin/touch'
        else:
            raise ValueError, "Cannot locate the 'touch' program, which is needed for testing"

        # Build a "failing" program, that just returns non-zero status
        status = os.system("gcc -o fail test/testsource/fail.c")
        self.failIf(status!=0)

        self.failprog = './fail'

        # Build a "succeeding" program, that returns zero status
        status = os.system("gcc -o success test/testsource/success.c")
        self.failIf(status!=0)
        self.successprog = './success'

        

    def tearDown(self):
	if os.path.exists(self.tempfilename):
	    os.unlink(self.tempfilename)
    
    def testRunWithArgs(self):
	prog = self.touchprog
	# Make sure the file doesn't exist
	self.failIf(os.path.exists(self.tempfilename))
	# Create a temporary file
	args = [self.tempfilename]
	wrap.run(prog,args)
	self.failUnless(os.path.exists(self.tempfilename))

    def testRunNoArgs(self):
	# Run a program with no arguments
        os.chmod('test/testsource/createfile.sh',0755)
	s = wrap.run('test/testsource/createfile.sh',[])
	self.failUnless(os.path.exists(self.tempfilename))


    def testRunSuccess(self):
        # Run a program that succeeds
        s = wrap.run(self.successprog,[self.successprog])
        self.failUnless(s)
        
        

    def testRunFailure(self):
        # Runa  program that fails and test for failure
        s = wrap.run(self.failprog,[self.failprog])
        self.failIf(s)


if __name__ == '__main__':
    unittest.main()
