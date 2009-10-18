import unittest
import sys

sys.path.append('bin')
from umdinst import wrap

class TestGetCommand(unittest.TestCase):
    def test(self):
	command = "gcc -c foo.c -o foo"
	args = command.split()
	self.assertEquals(command,wrap.getcommand(args))

if __name__ == '__main__':
    unittest.main()
