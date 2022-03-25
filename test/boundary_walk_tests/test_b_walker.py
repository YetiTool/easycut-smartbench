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
        self.b_setter.sort_gcode_input("")
        # set the boundary_datum (mid-mid of job envelope)
        self.b_setter.set_boundary_datum_point()

        if self.details_to_console == 1: 
            # what does this do exactly?
            # SHOULD at least print range_x and range_y
            self.b_setter.get_job_env()
            # print datums:
            print(" ___ datums x: {} and y: {}".format(self.b_setter.datum_x, self.b_setter.datum_y))
        
    def test_boundary_datum_is_not_blank(self):
        neither_are_zero = abs(self.b_setter.datum_x) + abs(self.b_setter.datum_y)
        self.assertFalse(neither_are_zero == 0, 
                         "missing datum data? or hopefully only DATUM FOUND")
        self.assertFalse(neither_are_zero == 2 * 495,
                         "... DATUM FOUND but still manually set!")

        print("... here")
        # ### FOCUS POINT <<>> !!! any datum point is already being excluded

    def test_without_arcs_one(self):
        without_string = "test/boundary_walk_test_files/w_n_w-out_arcs/without_1.gcode"
        print("testing: WITHOUT:")
        self.gcode_file_path = without_string
        self.b_setter.sort_gcode_input(self.gcode_file_path)
        self.b_setter.set_boundary_datum_point()
        # run test on latest: 
        self.test_boundary_datum_is_not_blank()
        
    def test_with_arcs_one(self):
        with_string = "test/boundary_walk_test_files/w_n_w-out_arcs/with_1.gcode"
        print("testing: WITH:")
        self.gcode_file_path = with_string
        self.b_setter.sort_gcode_input(self.gcode_file_path)
        self.b_setter.set_boundary_datum_point()
        # run test on latest:
        self.test_boundary_datum_is_not_blank()
            
if __name__ == "__main__": unittest.main()

def unit_test_b_walk_suite():
    suite = unittest.TestSuite()
    suite.addTest(BWalkerTest("test_boundary_datum_is_not_blank"))
    return suite

