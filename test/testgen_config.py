import unittest
from umdinst.setup import gen_config

class TestConfigFileWriter(unittest.TestCase):

    def setUp(self):
        self.modulename = 'testconfiglocal'
        self.fname =self.modulename + '.py'
        class Environment:
            prefix = ''
            id = ''
            whitelistfile = ''
            keyfile = ''
            encoding = ''
            javapath = ''
            with_pooledlog = False
            with_privatelog = False
            with_privatecvs = False
            with_workflow = False
            with_hackystat = False
            hackystat_host = ''
        env = Environment()
        self.cfg = gen_config.gen_platform_specific_config(env, self.fname)
        # FIXME: the current generator closes the config file, so
        # this test cannot be conducted
        #self.cfg.writevar('foo','bar')
        #self.cfg.writevar('mylist',[1,2,3,4])
        #self.cfg.close()
        self.module = __import__(self.modulename)

    def tearDown(self):
        # Delete the generated file
        try:
            os.remove(self.fname)
        except:
            pass
                

    def testWriteStr(self):
        #self.assertEquals(self.module.vars['foo'],'bar')
        pass

    def testWriteList(self):
        #self.assertEquals(self.module.vars['mylist'],[1,2,3,4])
        pass
