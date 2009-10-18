import unittest
import sys

sys.path.append('bin')
from umdinst import wrap

class TestCaptureHeader(unittest.TestCase):
    def setUp(self):
        self.source = '''
#include <stdio.h>
#include <stdlib.h>
#include "outerr.h"
#include "foobar.h"


int main(int argc, char *argv[])
{
 return 0;
}
        
'''
    
    def testGetHeadersFromSource(self):
        self.assertEquals(wrap.parseheaders(self.source),['outerr.h','foobar.h'])

if __name__ == '__main__':
    unittest.main()
