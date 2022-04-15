'''
Created on Apr 15, 2022

@author: florian
'''
import unittest
from ideInterface import CoDeSysConnect

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testRunTest(self):
        
        ide = CoDeSysConnect('..\Examples\Sample1.pro')

        ide.runTest(['Test_Server_Room_expected.exp'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRunTest']
    unittest.main()