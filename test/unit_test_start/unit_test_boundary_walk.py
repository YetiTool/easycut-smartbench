'''
Created on 8 Sep 2021

@author: hsth

NOTES:
    First coding done in a TDD manner. TDD = test driven development
    I.e. write the test first, then code to make the test pass

    WORK IN PROGRESS!!!

'''
import unittest

class UnitTestBoundaryWalkIsComplete(unittest.TestCase):
    
    def testBoundaryIsAnArray(self):  ## test method names begin 'test*'
        assert (1 + 2) == 33

    def testBoundaryIsACompletePolygon(self):
        self.assertEqual((0 * 10), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
