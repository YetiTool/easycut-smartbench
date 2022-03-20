#!/usr/bin/python

'''
Created on 8 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com
@author hugh.harford@poscoconsulting.com

NOTES:
    First coding done in a TDD manner. TDD = test driven development
    I.e. write the test first, then code to make the test pass

    WORK IN PROGRESS!
    TODO
        refactor naming to Python conventions
            variables: with_underscores_and_lower_case
            methods: with_underscores_and_lower_case
            class names: CapWords
            modules: alllowercase_maybe_with_underscores
        create test harness to run > 1 file and check them
        test harness to pass gcodes in set_up

'''
import unittest
from src.asmcnc.geometry import b_calculator

##########################################################

#  PLAN THE TEST:
#  
#  >>> GIVEN:
#    G1    GIVEN a gcode file
#    G2    GIVEN a working SB & console with software loaded
#  
#  >>> WHEN:
#    W1    WHEN the b_calculator undertakes the check 
#  
#  >>> THEN:
#          THEN any difficult shapes are identified (circles, arcs - others?)

#    T1    THEN any difficult shapes are dealt with (especially circles)
#    T2    THEN a BOUNDARY_array provides the boundary co-ordinates
#    T3          and accounts for the datum (doesn't include datum)
#    T4    THEN no part of the gcode file will exceed the area 
#              described by the BOUNDARY_array

##########################################################

class BWalkerTest(unittest.TestCase):
    details_to_console = 1  # zero for quiet, 1 for basics, 11 for specifics

    gcode_file_path = ""
    
    def setUp(self):
        self.b_setter = b_calculator.BCalculator()
        # optional - but in use for now:
        # blank gcode file for now
        self.gcode_file_path = "test/gcode_test_files/paired_gCode/Circles_and_star_1.gcode"        
        self.b_setter.set_gcode_file(self.gcode_file_path)
        # set the boundary_datum (mid-mid of job envelope)
        self.b_setter.set_boundary_datum_point()

        if self.details_to_console == 1: 
            # what does this do exactly?
            # SHOULD at least print range_x and range_y
            self.b_setter.get_job_env()
            # print datums:
            print("22 03 20 datums x: {} and y: {}".format(self.b_setter.datum_x, self.b_setter.datum_y))
        
    def test_boundary_datum_is_not_blank(self):
        neither_are_zero = abs(self.b_setter.datum_x) + abs(self.b_setter.datum_y)
        self.assertFalse(neither_are_zero == 0, "missing datum data? or hopefully only DATUM FOUND")
        # ### FOCUS POINT <<>> !!! any datum point is already being excluded

            
if __name__ == "__main__": unittest.main()

def unit_test_b_walk_suite():
    suite = unittest.TestSuite()
    suite.addTest(BWalkerTest("test_boundary_datum_is_not_blank"))
    return suite
    # or could use: suite = unittest.makeSuite(WidgetTestCase,'test')
# ##
# CAN define suite as follows, but looks complex
#
# class BoundaryWalkTestSuite(unittest.TestSuite):
#     def __init__(self):
#         unittest.TestSuite.__init__(self,map(UnitTestsBoundaryWalk,
#                                               ("test_found_boundary_is_a_complete_polygon",
#                                                "test_boundary_avoids_the_furthest_cut"))) 
