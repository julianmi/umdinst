import unittest
import sys
import os
import errno
import commands
import shutil
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring
from testcapturecompile import programcheck

def init_cvs(repos,sandbox,modulename):
    """Helper function to make a CVS repository and a sandbox"""
    os.mkdir(repos)
    commands.getoutput("cvs -d %s init" % repos)
    
    # Import an empty directory
    os.mkdir('/tmp/empty-dir')
    commands.getoutput('cd /tmp/empty-dir ; cvs -d %s import -m " " testinst umdinst start' % repos)
    os.rmdir('/tmp/empty-dir')
    
	
    # Create the sandbox directory
    os.mkdir(sandbox)
    commands.getoutput("cvs -d %s co -d %s %s" % (repos,sandbox,modulename))
    

class TestCVSUtils(unittest.TestCase):
    def setUp(self):

	# Create a CVS repository
	self.repos = '/tmp/repos'
	self.sandbox = '/tmp/sandbox'
	self.modulename = 'testinst'
	init_cvs(self.repos,self.sandbox,self.modulename)


	# Create a testfile in ~/foobarbaz
        self.commitmsg = 'ABC'
	self.cvs = wrap.CVSUtils(self.sandbox,self.commitmsg)
	os.mkdir(os.path.expanduser('~/foobarbaz'))
	self.testfile = os.path.expanduser('~/foobarbaz/testfile')
	f = open(self.testfile,'w')
	f.write('This is a testfile\n')
	f.close()

	
		 
    def tearDown(self):
	os.remove(self.testfile)
	os.rmdir(os.path.expanduser('~/foobarbaz'))
		 
	shutil.rmtree(self.sandbox)
	shutil.rmtree(self.repos)

    def testCheckAndCreateDir(self):
	dirname = os.path.join(self.sandbox,'foo/bar/baz')
	self.cvs._check_and_create_dir(dirname)
	self.failUnless(os.path.exists(dirname))
	result = commands.getoutput("cd %s ; cvs add %s" % (self.sandbox,dirname))
	self.failUnlessEqual(result,"cvs add: %s/CVS already exists" % dirname)


    # This shouldn't be done yet
    def testCopyToSandbox(self):
 	self.cvs._copy_to_sandbox(self.testfile)
 	sandboxfile = os.path.join(self.sandbox,'_HOME/foobarbaz/testfile')
 	self.failUnless(os.path.exists(sandboxfile))
 	self.assertEqual(open(sandboxfile).read(),'This is a testfile\n')

	# Check it's in CVS by trying to add again
	result = commands.getoutput("cd %s ; cvs add %s" % (self.sandbox,sandboxfile))
	self.failUnlessEqual(result,"cvs add: %s has already been entered" % sandboxfile)


    def testCommitSandboxFiles(self):
	# Add a new file to the sandbox, commit it, and check that it's in the repository
 	self.cvs._copy_to_sandbox(self.testfile)
	self.cvs._commit_sandbox_files()
	fname = os.path.join(self.repos,self.modulename,'_HOME/foobarbaz/testfile,v')
	self.failUnless(os.path.exists(fname))

	

    def testChangeBaseDir(self):
        #print self.cvs._change_base_directory('/foo/bar/baz.c','/foo/','/quux/bling/')
        #print self.cvs._change_base_directory('/foo/bar/baz.c','/quux/bling/')
	#self.assertEquals(self.cvs._change_base_directory('/foo/bar/baz.c','/quux/bling/'),
        #'/quux/bling/bar/baz.c')
	self.assertEquals(self.cvs._change_base_directory('/foo/bar/baz.c','/quux/bling/'),
			  '/quux/bling/foo/bar/baz.c')

    def testRelativePath(self):
	self.assertEquals(self.cvs._relative_path('/foo/bar/baz.c','/foo'),'bar/baz.c')


if __name__ == '__main__':
    unittest.main()
