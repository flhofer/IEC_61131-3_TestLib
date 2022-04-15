'''
-----------------------------------------------------------
Test Generator for the IEC61131-3 Test library - Unit test

Created Apr, 12, 2022

(C) 2017-2020 Hofer Florian, Bolzano, ITALY
Released under GNU Public License (GPL)
email info@florianhofer.it
-----------------------------------------------------------
'''

import unittest
import filecmp
import autogen

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testOutput(self):
        ''' Test generated export output with the ServerRoom export example '''

        autogen.main('')
        
        filecmp.clear_cache()        
        assert(filecmp.cmp('Test_Server_Room.exp', 'Test_Server_Room_expected.exp', shallow=False))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()