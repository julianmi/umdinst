import unittest
import sys
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck

class TestHeaderNotPresent(unittest.TestCase):
    def setUp(self):
	timezonecheck()
	
        # Sat Aug 13 19:04:24 2005
        self.starttime = 1123974264
        self.endtime = self.starttime+30
        self.sourcefiles = ['test/testsource/badheader.c']
        self.cd = wrap.CompileData(self.starttime,
                                   self.endtime,
                                   self.sourcefiles,
                                   subject = 'lorin',
                                   command = 'gcc -c test/testsource/badheader.c',
                                   success = False,
				   path = '/tmp')
    def testToXml(self):
        xml =  '\n'.join(["<log>,",
                          self.cd.toxml(),
                          "</log>"])
        dom = minidom.parseString(xml)
        # Just check and make sure that there's one source node
        # and no header nodes
        self.assertEquals(len(dom.getElementsByTagName('sourcefile')),1)
        self.assertEquals(len(dom.getElementsByTagName('headerfile')),0)
        

if __name__ == '__main__':
    unittest.main()
