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
#    T1    THEN any difficult shapes are dealt with (especially circles)
#    T2    THEN a BOUNDARY_array provides the boundary co-ordinates
#    T3          and accounts for the datum (doesn't include datum)
#    T4    THEN no part of the gcode file will exceed the area 
#              described by the BOUNDARY_array

##########################################################

class BWalkerTest(unittest.TestCase):
    # -1 to print method testNames, 1 to print other detail
    details_to_console = 11  # zero for quiet, 1 for basics, 11 for specifics

    gcodefile = [0, 0]
    gcode_file_path = ""
    b_setter = object
    # accepted accuracy of boundary v gcode_file actual:
    # accuracy_percent = 0.0001
    
    def setUp(self):
        if self.details_to_console == -1: 
            print(">> ____ setUp ____ ")
        self.gcode_file_path = ""
        #    G1    GIVEN a gcode file
        self.b_setter = b_calculator.BCalculator()
        
        if self.details_to_console == 1: 
            print("UnitTestsBoundaryWalk().set_up() ____ gcodefile = " + 
                  str(type(self.b_setter.get_gcode_path())))

    def test_boundary_datum_is_not_blank(self):
        if self.details_to_console == 11: print(">> ____ test_boundary_datum_is_not_blank ____ ")
        self.b_setter.get_job_envelope_from_gcode()
        # set the boundary_datum (mid-mid of job envelope)
        self.b_setter.set_boundary_datum_point()
        neither_are_zero = abs(self.b_setter.datum_x) + abs(self.b_setter.datum_y)
        print("b_setter.datum_x {}".format(self.b_setter.datum_x))
        
        self.assertFalse(neither_are_zero == 0, "missing datum data? or hopefully only DATUM FOUND")
        # ### FOCUS POINT <<>> !!! any datum point is already being excluded
        
        if self.details_to_console == 1: 
            print("datums: " + str(self.b_setter.datum_x) + "," + str(self.b_setter.datum_y))

            
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
