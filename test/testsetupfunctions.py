import unittest

from umdinst.setup import verifyperms

class TestSetupFunctions(unittest.TestCase):
    def testParentNoTrailingSlash(self):
        self.assertEquals(verifyperms.parent('/usr/local/bin'),
                          '/usr/local')
    def testParentTrailingSlash(self):
        self.assertEquals(verifyperms.parent('/usr/local/bin/'),
                          '/usr/local')
    def testMultipleCalls(self):
        self.assertEqual(verifyperms.parent(verifyperms.parent('/usr/local/bin')),
                         '/usr')
    def testUptoRoot(self):
        self.assertEqual(verifyperms.parent(verifyperms.parent(verifyperms.parent('/usr/local/bin'))),
                         '/')
    def testPastRoot(self):
        self.assertEqual(verifyperms.parent(verifyperms.parent(verifyperms.parent(verifyperms.parent('/usr/local/bin')))),
                         '')
                          

if __name__ == '__main__':
    unittest.main()
