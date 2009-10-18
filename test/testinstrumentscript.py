import unittest
import sys
import os
import errno
import commands
import shutil
from xml.dom import minidom

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring
from testcapturecompile import programcheck


class TestInstrumentScript(unittest.TestCase):
    def setUp(self):

	# These two will gt rmtree's, so make sure you don't put a bad dir here!
	self.repository = os.path.abspath('./.umdinst/repository')
	self.sandbox = os.path.abspath('./.umdinst/sandbox')

        os.system('cp bin/instrument instrument.py')
        import instrument
        self.i_nojava = instrument.Instrumenter(dirnames = [],
                                    hackystat_key = None,
                                    keyfile = None,
                                    registerdir = None,
                                    javapath = None,
                                    libdir = None,
                                    with_hackystat = None,
                                    hackystat_host = None,
                                    logfiledir = None,
                                    privatelogfiledir = None,
                                    with_pooledlog = False,
                                    with_privatelog = False,
                                    with_privatecvs = False,
				    repository=self.repository,
				    sandbox=self.sandbox)

	
        self.i_java = instrument.Instrumenter(dirnames = [],
                                    hackystat_key = None,
                                    keyfile = None,
                                    registerdir = None,
                                    javapath = '/usr/bin/java',
                                    libdir = None,
                                    with_hackystat = None,
                                    hackystat_host = None,
                                    logfiledir = None,
                                    privatelogfiledir = None,
                                    with_pooledlog = False,
                                    with_privatelog = False,
                                    with_privatecvs = False,
				    repository=self.repository,
				    sandbox=self.sandbox)
        self.i = self.i_nojava

        # Create a text file
        self.txtfile = 'testfile.txt'
        f = open(self.txtfile,'w')
        f.write("""The rain
in spain
falls mainly
on the plain
""")
        f.close()

    def tearDown(self):
        os.unlink(self.txtfile)
	if os.access(self.repository,os.R_OK):
	    shutil.rmtree(self.repository)
	if os.access(self.sandbox,os.R_OK):
	    shutil.rmtree(self.sandbox)
    
    def testJavaIsInstalled(self):
        self.failUnless(self.i_java.java_is_installed())
    
    def testJavaIsNotInstalled(self):
        self.failIf(self.i_nojava.java_is_installed())

    def testAddLineWhenItIsNotPresent(self):
        line = "This is an additional line"
        already_present = self.i.add_line_if_not_present(line,self.txtfile)
        self.failIf(already_present)

        # Now, open the file and check the contents
        file_contents = open(self.txtfile).read()
        expected_contents = """The rain
in spain
falls mainly
on the plain
This is an additional line
"""
        self.assertEquals(file_contents,expected_contents)

    def testAddLineWhenItIsPresent(self):
        line = "falls mainly"
        already_present = self.i.add_line_if_not_present(line,self.txtfile)
        self.failUnless(already_present)

        file_contents = open(self.txtfile).read()
        expected_contents = """The rain
in spain
falls mainly
on the plain
"""
        self.assertEquals(file_contents,expected_contents)

    def testAddLineWhenNotPresentWithNewline(self):
        line = "This line has a newline\n"
        already_present = self.i.add_line_if_not_present(line,self.txtfile)
        self.failIf(already_present)

        # Now, open the file and check the contents
        file_contents = open(self.txtfile).read()
        expected_contents = """The rain
in spain
falls mainly
on the plain
This line has a newline
"""
        self.assertEquals(file_contents,expected_contents)
        

    def testAddLineWhenPresentWithNewline(self):
        line = "on the plain\n"
        already_present = self.i.add_line_if_not_present(line,self.txtfile)
        self.failUnless(already_present)

        # Now, open the file and check the contents
        file_contents = open(self.txtfile).read()
        expected_contents = """The rain
in spain
falls mainly
on the plain
"""
        self.assertEquals(file_contents,expected_contents)

    def testRepositoryCreated(self):
	self.i.init_cvs()
	self.failUnless(os.access(self.repository,os.R_OK))
	# Make sure it's actually a repository
	self.failUnless(os.access(os.path.join(self.repository,'CVSROOT'),os.R_OK))
	
	self.failUnless(os.access(self.sandbox,os.R_OK))
	# Make sure it's actually a sandbox
	self.failUnless(os.access(os.path.join(self.sandbox,'CVS'),os.R_OK))


if __name__ == '__main__':
    unittest.main()
