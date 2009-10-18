import unittest

class TestInstall(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testNoModeOption(self):
        import os
        assert os.system('python setup.py install --id=ABC > /dev/null') <> 0
    def testModeIndividual(self):
        import os
        assert os.system('python setup.py install --mode=ind --id=ABC >/dev/null') == 0

if __name__ == '__main__':
    unittest.main()
