import unittest
import sys
#import quopri
import base64
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck

class TestFailedCompileData(unittest.TestCase):
    def setUp(self):
        # Sun Aug 21 17:18:29 2005
	timezonecheck()
        self.starttime = 1124659109
        self.endtime = self.starttime+5
        self.sourcefiles = ['test/testsource/syntax_error.c', 'test/testsource/outerr.c']
        self.cd = wrap.CompileData(self.starttime,
                                   self.endtime,
                                   self.sourcefiles,
                                   subject = 'foobar',
                                   command = 'mpicc -o foobar test/testsource/syntax_error.c test/testsource/outerr.c',
                                   success = False,
				   path = '/tmp')

    def testToXml(self):
        xml =  '\n'.join(["<log>,",
                          self.cd.toxml(),
                          "</log>"])
        dom = minidom.parseString(xml)
        self.assertEquals(dom.documentElement.tagName,'log')
        sfnodes = dom.getElementsByTagName('sourcefile')
        self.assertEquals(getfield(sfnodes[0],'name'),
                          'test/testsource/syntax_error.c')
        self.assertEquals(getfield(sfnodes[1],'name'),
                          'test/testsource/outerr.c')
        self.assertEquals(base64.decodestring(getfield(sfnodes[0],'source')),
                          open('test/testsource/syntax_error.c').read())
        self.assertEquals(base64.decodestring(getfield(sfnodes[1],'source')),
                          open('test/testsource/outerr.c').read())

        for sfnode in sfnodes:
            self.assertEquals(int(getfield(sfnode,'time')),
                              1124659109)
            self.assertEquals(getfield(sfnode,'timestr'),
                              'Sun Aug 21 17:18:29 2005')
            self.assertEquals(getfield(sfnode,'subject'),
                              'foobar'),
            self.assertEquals(getfield(sfnode,'command'),
                              'mpicc -o foobar test/testsource/syntax_error.c test/testsource/outerr.c')

        
        hfnodes = dom.getElementsByTagName('headerfile')
        self.assertEquals(getfield(hfnodes[0],'name'),
                          'test/testsource/outerr.h')
        self.assertEquals(getfield(hfnodes[1],'name'),
                          'test/testsource/syntax_error.h')
        self.assertEquals(base64.decodestring(getfield(hfnodes[0],'source')),
                          open('test/testsource/outerr.h').read())
        self.assertEquals(base64.decodestring(getfield(hfnodes[1],'source')),
                          open('test/testsource/syntax_error.h').read())

        for hfnode in hfnodes:
            self.assertEquals(int(getfield(hfnode,'time')),
                              1124659109)
            self.assertEquals(getfield(hfnode,'timestr'),
                              'Sun Aug 21 17:18:29 2005')
            self.assertEquals(getfield(hfnode,'subject'),
                              'foobar'),
            self.assertEquals(getfield(hfnode,'command'),
                              'mpicc -o foobar test/testsource/syntax_error.c test/testsource/outerr.c')

if __name__ == '__main__':
    unittest.main()
