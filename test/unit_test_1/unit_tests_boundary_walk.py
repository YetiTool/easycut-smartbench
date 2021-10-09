'''
Created on 8 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com

NOTES:
    First coding done in a TDD manner. TDD = test driven development
    I.e. write the test first, then code to make the test pass

    WORK IN PROGRESS!!!
    
    TODO
        refactor naming to Python conventions
            variables: with_underscores_and_lower_case
            class names: CapWords
            modules: alllowercase_maybe_with_underscores
        create test harness to run > 1 file and check them
        test harness to pass gcodes in setUp

'''
import unittest
import numpy as np
import os.path
from geometry import boundary_calculator
from numpy.ma.core import isarray
from operator import is_
from pandas.core.dtypes.missing import isnull
from numpy import isnan

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
    gcodefile = [0,0]
    gcode_file_path = ""
    b_setter = object
    
    # accepted accuracy of boundary v gcode_file actual:
    accuracy_percent = 0.0001
    
    def setUp(self):
        self.gcode_file_path = ""
        #    1    GIVEN a gcode file
        # gcode file path is set automatically in boundary_calculator if not supplied:
        self.b_setter = boundary_calculator.BoundaryCalculator()
        
        # self.print_to_console_sorted_list()
        
        # test harness could pass gcodes in here...
        # self.b_setter.set_gcode_as_list(self.gcode_file_path)
        ### BUT actually would be best to pass in via line 60 
        
        #    2    GIVEN a working SB & console with software loaded
        #    load screen_test
        #screen test manager: # stm = b_setter.stm # stm.screen_shapeCutter_1
        
        #    3    GIVEN a boundary_calculator feature
        ##         c.f. geometry.boundary_calculator
        
        if self.detailsToConsole == 1: 
            print("UnitTestsBoundaryWalk().setUp() ____ gcodefile = " + 
                  str(type(self.b_setter.get_gcode_path())))

    def tearDown(self):
        pass
    
    def testBoundaryIsAnArray(self):  
        if self.detailsToConsole == 1: 
            print("UnitTestsBoundaryWalk().testBoundaryIsAnArray() ____ gcodefile = " + 
                  str(type(self.b_setter.gcodefile)))

        self.assertTrue(isinstance(self.b_setter.gcodefile, (list, tuple, np.ndarray)), 
                        " not an array, this gcodefile")

    # def testGcodeIsACompletePolygon(self):
    #     self.worker_checkFirstAndLast(self.b_setter.gcodefile,"gcodefile input")

    def testFoundBoundaryIsACompletePolygon(self):
        self.worker_checkFirstAndLast(
            self.b_setter.boundary_calc_by_segment,
            "b_setter.boundary_calc_by_segment")

    def worker_checkFirstAndLast(self, inputList, strInputName):
        print("worker_checkFirstAndLast: " + strInputName + "... size of inputList is: " + str(len(inputList)))
        try:
            first_item = inputList[0]
            last_item = inputList[-1]
        except:
            pass
        finally:
            print("inputList: " + str(inputList) + " from: " + strInputName)
            return
        
            
        # [self.gcodefile[0], self.gcodefile[-1]]
        if self.detailsToConsole == 1:
            print("UnitTestsBoundaryWalk().worker_checkFirstAndLast() ____ inputList, for " + strInputName + " = " + str(type(inputList)))
            print("first_item is:   " + str(first_item))
            print("last_item is:    " + str(last_item))
        
        self.assertEquals(first_item, last_item, 
                          " start and end of " +
                          + strInputName + " DON'T MATCH: \n\n" +
                          str(first_item) + ", " + str(last_item))
        
    def testGcodeFileWorks(self):
        self.assertTrue(os.path.isfile(self.b_setter.gcode_file_path), 
                        "gcode supplied path/file isn't working...  " + 
                        self.b_setter.gcode_file_path)


    def testBoundaryDatumIsNotBlank(self):
        neither_are_zero = abs(self.b_setter.datum_x) + abs(self.b_setter.datum_y)
        self.assertTrue(neither_are_zero > 0, "the datum doesn't exist? ")
        if self.detailsToConsole == 1: 
            print("datums: " + str(self.b_setter.datum_x) + "," + str(self.b_setter.datum_y))
        
    def print_to_console_sorted_list(self):  
        for x in range(len(self.b_setter.angle_sorted_boundary_xy)):
            # print("sorted_c[x][0] = " + str(b_setter.angle_sorted_boundary_xy[x][0]))
            # print("sorted_c[x][0][0] = " + str(b_setter.angle_sorted_boundary_xy[x][0][0]))
            # print("sorted_c[x][0][1] = " + str(b_setter.angle_sorted_boundary_xy[x][0][1]))
            print("sorted_c[x][1] = " + str(self.b_setter.angle_sorted_boundary_xy[x-1][2]))
            # print("sorted_c[x][2] = " + str(b_setter.angle_sorted_boundary_xy[x][2]))
        
        
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
        
        # defines b_setter.boundary_xy based on the gcode supplied
        # self.b_setter.set_gcode_as_list(self.gcode_file_path) # gcode_file_path
        # THIS IS DONE IN SETUP
        
        # sort boundary_xy by angle
        # used sorted: sorting by angle b_setter.sorted_coordinates_by_angle
        # THIS IS DONE IN SETUP
        
        #
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #
        # go through by angle and record max distance going round
        # this is what provides the BOUNDARY:
        
        #
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #

        if self.detailsToConsole == 1:
            print("b_setter.datum_x = " + str(self.b_setter.datum_x))
            print("b_setter.datum_y = " + str(self.b_setter.datum_y))
            self.print_to_console_sorted_list()


    def testJobEnvelopesMatch(self):
        
        job_envelope_g = self.b_setter.get_job_envelope_from_gcode()

        # actual, from gcode_file: x max - x min
        gcode_size_x = job_envelope_g[0][1] - job_envelope_g[0][0]
        gcode_size_y = job_envelope_g[1][1] - job_envelope_g[1][0]

        # found, from boundary calc: x max - x min
        b_size_x = self.b_setter.bound_range_x[1] - self.b_setter.bound_range_x[0]
        b_size_y = self.b_setter.bound_range_y[1] - self.b_setter.bound_range_y[0]



        # what is the difference? assume boundary bigger...
        x_size_diff = abs(b_size_x - gcode_size_x)
        y_size_diff = abs(b_size_y - gcode_size_y)
        
        self.assertTrue(
            x_size_diff < gcode_size_x*self.accuracy_percent, 
            " x not close enough, accuracy(" + 
            str(self.accuracy_percent) + "), gcode_size_x(" + 
            str(gcode_size_x) + "), " +
            "x_size_diff(" + str(x_size_diff) + ")")

        self.assertTrue(
            y_size_diff < gcode_size_y*self.accuracy_percent, 
            " y not close enough, accuracy(" + 
            str(self.accuracy_percent) + "), gcode_size_y(" 
            + str(gcode_size_y) + "), " +
            "y_size_diff(" + str(y_size_diff) + ")")
        
        if self.detailsToConsole == 1: 
            print("gcode found_envelope x(" + str(job_envelope_g[0][0]) + "," + str(job_envelope_g[0][1]) 
                  + ") y(" + str(job_envelope_g[1][0])  + "," + str(job_envelope_g[1][1]) + ")")
            print("x_size_diff: " + str(x_size_diff) + 
                  ", and y_size_diff: " + str(y_size_diff))
            print("BOUNDARY RANGE: b_size_x = " + str(b_size_x) + ", b_size_y = " + str(b_size_y))

     

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
