'''
Created on 8 Sep 2021

@author: hsth
'''
import unittest


class BasicUnitTestB(unittest.TestCase):
    def runTest(self): 
    ## default test method is runTest. e.g. function name runTest_1 does not run'
    ## However, note that if testThis is uncommented below, then runTest will not fire'
        assert 100 == 50 + 500, 'incorrect maths'
        
#    def testThis(self):
#        self.assertEqual(0 + 1, 11), '!= after all'

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()