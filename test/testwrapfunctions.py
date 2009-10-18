import unittest
import sys
import os

sys.path.append('bin')
from umdinst import wrap

class TestWrapFunctions(unittest.TestCase):
    
    def testRunFailure(self):
        """Make sure that the fail program exists. Build it if necessary"""
        if not (os.access('fail',os.X_OK) or os.access('fail.exe',os.X_OK)):
            res = os.system('gcc -o fail test/testsource/fail.c')
            if res!=0:
                raise ValueError, "Could not build fail program"

        success = wrap.run('./fail',['fail'])
        self.assertEquals(success,False)

    def testRunSuccess(self):
        """Make sure that the success program exists. Build it if necessary"""
        if not (os.access('success',os.X_OK) or os.access('success.exe',os.X_OK)):
            res = os.system('gcc -o success success.c')
            if res!=0:
                raise ValueError, "Could not build success program"

        success = wrap.run('./success',['success'])
        self.assertEquals(success,True)
