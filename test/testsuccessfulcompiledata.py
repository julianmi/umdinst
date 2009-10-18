import unittest
import sys
#import quopri
import base64
import time
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

def getfield(node,fieldname):
    return node.getElementsByTagName(fieldname)[0].firstChild.data

def timezonecheck():
    # The time tests only work if it's EST or EDT. If it's one of those,
    # time.tzname seems to be ('EST','EDT')
    if time.tzname!=('EST','EDT'):
	raise ValueError, "System time zone not EST/EDT."

def xmlifystring(s):
    "Take a log fragment and convert it to valid XML"
    header = '<?xml version="1.0" ?>\n<log>'
    footer = '</log>\n'
    return '\n'.join([header,s,footer])

class TestSuccessfulCompileData(unittest.TestCase):
    def setUp(self):
        # Sat Aug 13 19:04:24 2005
	timezonecheck()
        self.starttime = 1123974264
        self.endtime = self.starttime+30.5
        self.sourcefiles = ['test/testsource/outerr.c']
        self.cd = wrap.CompileData(self.starttime,
                              self.endtime,
                              self.sourcefiles,
                              subject = 'borat',
                              command = 'CC -c test/testsource/outerr.c',
                              success = True,
			      path = '/tmp')
        xml =  xmlifystring(self.cd.toxml())
        self.dom = minidom.parseString(xml)
        self.sfnode = self.dom.getElementsByTagName('sourcefile')[0]
        self.hfnode = self.dom.getElementsByTagName('headerfile')[0]


	
    def testLogField(self):
        self.assertEquals(self.dom.documentElement.tagName,'log')

    def testCompileTag(self):
	self.assertEquals(len(self.dom.getElementsByTagName('compile')),1)

    def testSuccessAtr(self):
	self.assertEquals(int(self.sfnode.attributes['success'].value),1)

    def testName(self):
        self.assertEquals(getfield(self.sfnode,'name'),
                          'test/testsource/outerr.c')
    def testTime(self):
        self.assertEquals(int(getfield(self.sfnode,'time')),
                          1123974264)

    def testTimestr(self):
        self.assertEquals(getfield(self.sfnode,'timestr'),
                          'Sat Aug 13 19:04:24 2005')

    def testSubject(self):
        self.assertEquals(getfield(self.sfnode,'subject'),
                          'borat')

    def testCommand(self):
        self.assertEquals(getfield(self.sfnode,'command'),
                          'CC -c test/testsource/outerr.c')

    def testTimeInterval(self):
        self.assertEquals(float(getfield(self.sfnode,'time_interval')),
                          30.5)

    def testSource(self):
        self.assertEquals(base64.decodestring(getfield(self.sfnode,'source')),
                          open('test/testsource/outerr.c').read())

    def testHeaderName(self):
        self.assertEquals(getfield(self.hfnode,'name'),
                          'test/testsource/outerr.h')
    def testHeaderTime(self):
        self.assertEquals(int(getfield(self.hfnode,'time')),
                          1123974264)

    def testHeaderTimestr(self):
        self.assertEquals(getfield(self.hfnode,'timestr'),
                          'Sat Aug 13 19:04:24 2005')

    def testHeaderSubject(self):
        self.assertEquals(getfield(self.hfnode,'subject'),
                          'borat')

    def testHeaderCommand(self):
        self.assertEquals(getfield(self.hfnode,'command'),
                          'CC -c test/testsource/outerr.c')

    def testHeaderTimeInterval(self):
        self.assertEquals(int(getfield(self.hfnode,'time_interval')),
                          30)

    def testHeaderSource(self):
        self.assertEquals(base64.decodestring(getfield(self.hfnode,'source')),
                          open('test/testsource/outerr.h').read())
        
if __name__ == '__main__':
    unittest.main()
