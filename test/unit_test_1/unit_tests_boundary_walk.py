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
    
    
    gcodefile = 0.0
    detailsToConsole = 0
    
    def setUp(self):
        # get the GIVEN
        
        #    1    GIVEN a gcode file
        # def getGCodeFile(self):
            
        global gcodefile 
        #    2    GIVEN a working SB & console with software loaded
        ##         c.f. geometry.boundary_calculator line 20 (est)
        boundarySetter = boundary_calculator.BoundaryCalculator(self)
        gcodefile = boundarySetter.get_boundary_as_gcode_array()
            
        return gcodefile


    def tearDown(self):
        pass
    
    
    def goThroughData(self, inputGCodeFile):
        
        stringTestFile = []
        
        for i in inputGCodeFile:
            stringTestFile[i] = str(inputGCodeFile(i))
        
        return stringTestFile
    
    
    def testBoundaryIsAnArray(self):  ## test method names begin 'test*'
        # get global gcodefile as string
        # double running of setUp:   testFile = self.setUp()
        global gcodefile
        # testFile = self.goThroughData(gcodefile)
        testFile = gcodefile
        
        self.assertTrue(isinstance(testFile, (list, tuple, np.ndarray)), " not an array, this gcodefile")
        
        ## basic test-assert-is-working test: 
        # assert (1 + 2) == 33

    def testBoundaryIsACompletePolygon(self):
        tester = [5,10,15,15]
        
        # ~~~~~~~~~~~~ @@@ ~~~~~~~~~~~ #
        #
        #        get the tester replaced with the 
        #        incoming list/string array datatype.
        #
        #        the same is defined in boundary_calculator, but gets 
        #        transformed or messed with...
        #
        # ~~~~~~~~~~~~ @@@ ~~~~~~~~~~~ #

        
        # self.gcodefile
        first_item = tester[0]
        last_item = tester[-1]
                
        # [self.gcodefile[0], self.gcodefile[-1]]
        if self.detailsToConsole == 1:
            print("first_item is:   " + str(first_item))
            print("last_item is:    " + str(last_item))
        
        self.assertEquals(first_item, last_item, " start and end of gcode file are not the same coordinates... ")
        
        
        ## basic test-assert-equals-is-working test: 
        # self.assertEqual((0 * 10), 0)
        
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