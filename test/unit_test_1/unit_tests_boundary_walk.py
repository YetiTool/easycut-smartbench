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

import numpy as np
import os.path

from geometry import boundary_calculator

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
    detailsToConsole = 0
    gcodefile = 0.0
    gcode_file_path = ""
    boundarySetter = object
    
    def setUp(self):
        # get the GIVENs sorted i.e. what we need for the test(s):
        
        global boundarySetter
        global gcodefile, gcode_file_path
        # global st

        #    1    GIVEN a gcode file
        boundarySetter = boundary_calculator.BoundaryCalculator()
        gcodefile = boundarySetter.get_sample_boundary_as_gcode_list()
        gcode_file_path = boundarySetter.get_gcode_path()
               
        #    2    GIVEN a working SB & console with software loaded
        #    load screen_test
        
        #screen test manager:
        # stm = boundarySetter.stm
        # stm.screen_shapeCutter_1
        
        #    3    GIVEN a boundary_calculator feature
        ##         c.f. geometry.boundary_calculator
        boundarySetter.set_boundary_datum_point()
        
        if self.detailsToConsole == 1: 
            print("UnitTestsBoundaryWalk().setUp() ____ gcodefile = " + str(type(gcodefile)))

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
        if self.detailsToConsole == 1: 
            print("UnitTestsBoundaryWalk().testBoundaryIsAnArray() ____ gcodefile = " + str(type(gcodefile)))

        # testFile = self.goThroughData(gcodefile)
        ############# testFile = list(gcodefile)
        
        self.assertTrue(isinstance(gcodefile, (list, tuple, np.ndarray)), " not an array, this gcodefile")
        
        ## basic test-assert-is-working test: 
        # assert (1 + 2) == 33

    def testGcodeIsACompletePolygon(self):
        global gcodefile
        self.worker_checkFirstAndLast(gcodefile,"gcodefile")

    def testFoundBoundaryIsACompletePolygon(self):
        self.worker_checkFirstAndLast(
            boundarySetter.boundary_calc_by_segment,
            "boundarySetter.boundary_calc_by_segment")

    def worker_checkFirstAndLast(self,inputList,strInputName):
        first_item = inputList[0]
        last_item = inputList[-1]
                
        # [self.gcodefile[0], self.gcodefile[-1]]
        if self.detailsToConsole == 1:
            print("UnitTestsBoundaryWalk().worker_checkFirstAndLast() ____ inputList, for " + strInputName + " = " + str(type(inputList)))
            print("first_item is:   " + str(first_item))
            print("last_item is:    " + str(last_item))
        
        self.assertEquals(first_item, last_item, 
                          " start and end of DON'T MATCH: "
                          + strInputName + "\n\n" +
                          str(first_item) + ", " + str(last_item))
        ## basic test-assert-equals-is-working test: 
        # self.assertEqual((0 * 10), 0)
        
        
    def testGcodeFileWorks(self):
        global gcode_file_path
        self.assertTrue(os.path.isfile(gcode_file_path), "gcode supplied path/file isn't working...  " + gcode_file_path)


    def testBoundaryDatumIsNotBlank(self):
        global boundarySetter
        neither_are_zero = abs(boundarySetter.datum_x) + abs(boundarySetter.datum_y)
        self.assertTrue(neither_are_zero > 0, "the datum doesn't exist? ")
        
    def print_to_console_sorted_list(self):  
        for x in range(len(boundarySetter.angle_sorted_boundary_xy)):
            # print("sorted_c[x][0] = " + str(boundarySetter.angle_sorted_boundary_xy[x][0]))
            # print("sorted_c[x][0][0] = " + str(boundarySetter.angle_sorted_boundary_xy[x][0][0]))
            # print("sorted_c[x][0][1] = " + str(boundarySetter.angle_sorted_boundary_xy[x][0][1]))
            print("sorted_c[x][1] = " + str(boundarySetter.angle_sorted_boundary_xy[x-1][1]))
            # print("sorted_c[x][2] = " + str(boundarySetter.angle_sorted_boundary_xy[x][2]))
        
    def testJobEnvelopesMatch(self):
        boundarySetter.get_job_envelope_xy_list()
     

        
    def testBoundaryAvoidsTheFurthestCut(self):
        # this test is by far the most complex 
        # it is the critical test to ensure the boundary 
        # is actually what we want it to be
        
        # Approach:
        
        # ~~~ 1
        # find the x & y "cut_mid_point" coordinate of the job envelope 
        # will use the geometry.job_envelope module
        # this will be used as the reference point
        #    [n.b. this will be available as a 
        #     function in boundary_calculator]
        # DONE >>>>>>>>>> see in setUp
        # and tested in: testBoundaryDatumIsNotBlank
        pass # DONE
                    
        # ~~~ 2
        # convert the gcode input into gcode_radial
        # and find the distance from the datum at each angle
        # these need to be a datatype with 
        # radial data and distance at that angle from the cut_mid_point (jobEnvelope)
        #    [n.b. this conversion is available as 
        #     a function in boundary_calculator[]
        # SEE:
        #    angle_from_datum
        #    distance_from_datum
        #    
        #    creating boundary_xy with: add_coord_to_boundary()
        pass # DONE

        # ~~~ 3
        # sort the boundary_radial
        # then find the max distance for each 'radial segment'
        # the output of this is the "boundary"
        #    [n.b. this conversion is available as 
        #     a function in boundary_calculator[]
        #        SEE: run_via_angle_checking_max_dist_n_range()
        
        # ~~~ 4        
        
        ############ IMPLEMENTING PLAN ABOVE VIA THE NUMBERS LISTED:
        
        ### ~~~~~~~~~~~~~~# 1
        
        global gcode_file_path
        global gcodefile
        global boundarySetter

        # defines boundarySetter.boundary_xy based on the gcode supplied
        boundarySetter.set_gcode_as_list(gcode_file_path) # gcode_file_path
        # used sorted: sorting by angle boundarySetter.sorted_coordinates_by_angle
        boundarySetter.sort_boundary_data_by_angle()
        
        #
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #
        # go through by angle and record max distance going round
        # this is what provides the BOUNDARY:
        boundarySetter.run_via_angle_checking_max_dist_n_range()
        #
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #

        if self.detailsToConsole == 1:
            print("boundarySetter.datum_x = " + str(boundarySetter.datum_x))
            print("boundarySetter.datum_y = " + str(boundarySetter.datum_y))
            self.print_to_console_sorted_list()



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

    def unitTestBoundaryWalkSuite():
        suite = unittest.TestSuite()
        suite.addTest(UnitTestsBoundaryWalk("testFoundBoundaryIsACompletePolygon"))
        suite.addTest(UnitTestsBoundaryWalk("testBoundaryAvoidsTheFurthestCut"))
        return suite
        # or could use: suite = unittest.makeSuite(WidgetTestCase,'test')
###
# CAN define suite as follows, but looks complex
#
# class BoundaryWalkTestSuite(unittest.TestSuite):
#     def __init__(self):
#         unittest.TestSuite.__init__(self,map(UnitTestsBoundaryWalk,
#                                               ("testFoundBoundaryIsACompletePolygon",
#                                                "testBoundaryAvoidsTheFurthestCut"))) 
# 