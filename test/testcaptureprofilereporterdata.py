import unittest
import sys
import os
import errno
import commands
from xml.dom import minidom

sys.path.append('bin')
from umdinst import wrap

from testsuccessfulcompiledata import getfield, timezonecheck, xmlifystring
from testcapturecompile import programcheck

class TestCaptureProfileReporterData(unittest.TestCase):
    """Test that the object that encapsulates the profiler reported data acts correctly"""
    def setUp(self):
        # Make sure we are running in EST otherwise the time string test will fail
        timezonecheck()
        # Sun Aug 21 17:18:29 2005
        self.starttime = 1124659109
        self.endtime = self.starttime+.15
        self.rep = wrap.ProfilerReporterData(starttime = self.starttime,
                                             endtime = self.endtime,
                                             subject = 'lorin',
                                             command = 'gprof ./loop',
                                             success = True,
                                             path = '/foo/bar/baz',
                                             reportdata = "This <is> the report")
        self.xml = self.rep.toxml()
        self.dom = minidom.parseString(self.xml)
        self.repnode = self.dom.getElementsByTagName('profile_report')[0]

    def testNode(self):
        self.assertEquals(self.dom.documentElement.tagName,'profile_report')

    def testSubject(self):
        self.assertEquals(getfield(self.repnode,'subject'),'lorin')

    def testTime(self):
        self.assertEquals(int(getfield(self.repnode,'time')),1124659109)

    def testTimestr(self):
        self.assertEquals(getfield(self.repnode,'timestr'),'Sun Aug 21 17:18:29 2005')

    def testCommand(self):
        self.assertEquals(getfield(self.repnode,'command'),'gprof ./loop')


    def testPath(self):
        self.assertEquals(getfield(self.repnode,'path'),'/foo/bar/baz')


    def testTimeInterval(self):
        self.assertEquals(float(getfield(self.repnode,'time_interval')),.15)
    

    def testContents(self):
        self.assertEquals(getfield(self.repnode,'contents'),"This <is> the report")

if __name__ == '__main__':
    unittest.main()
