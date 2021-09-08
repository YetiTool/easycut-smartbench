'''
Created on 8 Sep 2021

@author: hsth
'''
import unittest

class BasicUnitTestA(unittest.TestCase):
    def testAdd(self):  ## test method names begin 'test*'
        assert (1 + 2) == 3
        self.assertEqual(0 + 1, 7)
    def testMultiply(self):
        self.assertEqual((0 * 10), 0)
        self.assertEqual((5 * 8), 40)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()