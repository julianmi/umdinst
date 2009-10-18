import unittest
from umdinst.setup import which

class TestWhich(unittest.TestCase):
    
    def testProgInPath(self):
        # This assumes /bin/sh is actually there
        self.assertEquals(which.which("sh"),"/bin/sh")
        
    def testProgNotInPath(self):
        self.assertEquals(which.which("foobarbaz"),None)

if __name__ == '__main__':
    unittest.main()
