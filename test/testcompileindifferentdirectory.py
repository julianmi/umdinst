import unittest
import sys
#import quopri
import base64
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck

class TestCompileInDifferentDirectory(unittest.TestCase):
    def setUp(self):
        # Sat Aug 13 19:04:24 2005
	timezonecheck()
        self.starttime = 1123974264
        self.endtime = self.starttime+30
        self.sourcefiles = ['test/testsource/sub/foo.c']
        self.cd = wrap.CompileData(self.starttime,
                                   self.endtime,
                                   self.sourcefiles,
                                   subject = 'mike',
                                   command = 'gcc -c test/testsource/sub/foo.c',
                                   success = True,
				   path = '/tmp')
    def testToXml(self):
        xml =  '\n'.join(["<log>,",
                          self.cd.toxml(),
                          "</log>"])
        dom = minidom.parseString(xml)
        self.assertEquals(dom.documentElement.tagName,'log')
        sfnode = dom.getElementsByTagName('sourcefile')[0]
        self.assertEquals(getfield(sfnode,'name'),
                          'test/testsource/sub/foo.c')
        self.assertEquals(int(getfield(sfnode,'time')),
                          1123974264)
        self.assertEquals(getfield(sfnode,'timestr'),
                          'Sat Aug 13 19:04:24 2005')
        self.assertEquals(getfield(sfnode,'subject'),
                          'mike')
        self.assertEquals(getfield(sfnode,'command'),
                          'gcc -c test/testsource/sub/foo.c')
        self.assertEquals(float(getfield(sfnode,'time_interval')),
                          30)
        self.assertEquals(base64.decodestring(getfield(sfnode,'source')),
                          open('test/testsource/sub/foo.c').read())

        hfnode = dom.getElementsByTagName('headerfile')[0]
        self.assertEquals(getfield(hfnode,'name'),
                          'test/testsource/sub/foo.h')
        self.assertEquals(int(getfield(hfnode,'time')),
                          1123974264)
        self.assertEquals(getfield(hfnode,'timestr'),
                          'Sat Aug 13 19:04:24 2005')
        self.assertEquals(getfield(hfnode,'subject'),
                          'mike')
        self.assertEquals(getfield(hfnode,'command'),
                          'gcc -c test/testsource/sub/foo.c')

        self.assertEquals(int(getfield(hfnode,'time_interval')),
                          30)
        self.assertEquals(base64.decodestring(getfield(hfnode,'source')),
                          open('test/testsource/sub/foo.h').read())


if __name__ == '__main__':
    unittest.main()
