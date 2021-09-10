'''
Created on 8 Sep 2021

@author: hsth

NOTES:
    First coding done in a TDD manner. TDD = test driven development
    I.e. write the test first, then code to make the test pass

    WORK IN PROGRESS!!!

'''
import unittest

##########################################################

#  PLAN THE TEST:
#  
#  >>> GIVEN:
#    1    GIVEN a gcode file
#    2    GIVEN a working SB & console with software loaded
#  

#  >>> WHEN:
#    *    WHEN the boundary_walk check is undertaken (likely to be on the kivy preview screen)
#  

#  >>> THEN:
#    *    THEN an non-zero array BOUNDARY_array is returned that provides the boundary co-ordinates
#    *    THEN the BOUNDARY_array is a complete boundary (polygon), so the start and end point are the same
#    *    THEN no part of the gcode file will exceed the area described by the BOUNDARY_array


##########################################################

class UnitTestBoundaryWalkIsComplete(unittest.TestCase):
    
    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    
    def testBoundaryIsAnArray(self):  ## test method names begin 'test*'
        assert (1 + 2) == 33

    def testBoundaryIsACompletePolygon(self):
        self.assertEqual((0 * 10), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
