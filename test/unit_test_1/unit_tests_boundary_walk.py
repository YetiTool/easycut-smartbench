'''
Created on 8 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com

NOTES:
    First coding done in a TDD manner. TDD = test driven development
    I.e. write the test first, then code to make the test pass

    WORK IN PROGRESS!!!

'''
import unittest

from geometry import boundary_calculator
from array import array
# from numpy.ma.core import isarray
import numpy as np

# import main
# import screen_test


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

class UnitTestsBoundaryWalk(unittest.TestCase):
    
    
    gcodefile = 0.0;
    
    def setUp(self):
        # get the GIVEN
        
        #    1    GIVEN a gcode file
        # def getGCodeFile(self):
            
        global gcodefile 
        #    2    GIVEN a working SB & console with software loaded
        boundarySetter = boundary_calculator.BoundaryCalculator(self)
        gcodefile = boundarySetter.get_boundary_as_gcode_array()
            
        return gcodefile


    def tearDown(self):
        pass
    
    
    def testBoundaryIsAnArray(self):  ## test method names begin 'test*'
        # global gcodefile 
        testFile = self.setUp()
        
#        self.assertTrue(is(gcodefile), " not an array, this gcodefile")
        
        self.assertTrue(isinstance(testFile, (list, tuple, np.ndarray)))

        
        assert (1 + 2) == 3

    def testBoundaryIsACompletePolygon(self):
        self.assertEqual((0 * 10), 0)
        
    def testBoundaryAvoidsTheFurthestCut(self):
        self.assertEqual(("this cut"), "this cut")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

    def unitTestBoundaryWalkSuite():
        suite = unittest.TestSuite()
        suite.addTest(UnitTestsBoundaryWalk("testBoundaryIsACompletePolygon"))
        suite.addTest(UnitTestsBoundaryWalk("testBoundaryAvoidsTheFurthestCut"))
        return suite
        # or could use: suite = unittest.makeSuite(WidgetTestCase,'test')
###
# CAN define suite as follows, but looks complex
#
# class BoundaryWalkTestSuite(unittest.TestSuite):
#     def __init__(self):
#         unittest.TestSuite.__init__(self,map(UnitTestsBoundaryWalk,
#                                               ("testBoundaryIsACompletePolygon",
#                                                "testBoundaryAvoidsTheFurthestCut"))) 
# 