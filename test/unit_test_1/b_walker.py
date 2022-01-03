'''
Created on 8 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com
@author hugh.harford@poscoconsulting.com


NOTES:
    First coding done in a TDD manner. TDD = test driven development
    I.e. write the test first, then code to make the test pass

    WORK IN PROGRESS!!!
    
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
from geometry import b_calculator

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
#    *    INCORRECT. Expunged: THEN the BOUNDARY_array is a complete boundary (polygon), so the start and end point are the same
#    *    THEN no part of the gcode file will exceed the area described by the BOUNDARY_array

##########################################################

class BWalker(unittest.TestCase):
    # -1 to print method testNames, 1 to print other detail
    details_to_console = 1 # zero for quiet, 1 for basics

    gcodefile = [0,0]
    gcode_file_path = ""
    b_setter = object
    # accepted accuracy of boundary v gcode_file actual:
    accuracy_percent = 0.0001
    
    def setUp(self):
        if self.details_to_console == -1: 
            print(">> ____ setUp ____ ")
        self.gcode_file_path = ""
        #    1    GIVEN a gcode file
        self.b_setter = b_calculator.BCalculator()
        
        #    2    GIVEN a working SB & console with software loaded
        #    load screen_test
        #screen test manager: # stm = b_setter.stm # stm.screen_shapeCutter_1
        
        #    3    GIVEN a b_calculator feature
        ##         c.f. geometry.b_calculator
        
        if self.details_to_console == 1: 
            print("UnitTestsBoundaryWalk().set_up() ____ gcodefile = " + 
                  str(type(self.b_setter.get_gcode_path())))


    def test_boundary_datum_is_not_blank(self):
        if self.details_to_console == 11: 
            print(">> ____ test_boundary_datum_is_not_blank ____ ")
        # set the boundary_datum (mid-mid of job envelope)
        
        ## moved these two into boundary_calculator.
        self.b_setter.get_job_envelope_from_gcode()
        self.b_setter.set_boundary_datum_point()
        
        neither_are_zero = abs(self.b_setter.datum_x) + abs(self.b_setter.datum_y)
        self.assertTrue(neither_are_zero > 0, "the datum doesn't exist? ")
        if self.details_to_console == 1: 
            print("datums: " + str(self.b_setter.datum_x) + "," + str(self.b_setter.datum_y))

            
if __name__ == "__main__":
    unittest.main()
    

    def unit_test_b_walk_suite():
        suite = unittest.TestSuite()
        suite.addTest(BWalker("test_boundary_datum_is_not_blank"))
        return suite
        # or could use: suite = unittest.makeSuite(WidgetTestCase,'test')
###
# CAN define suite as follows, but looks complex
#
# class BoundaryWalkTestSuite(unittest.TestSuite):
#     def __init__(self):
#         unittest.TestSuite.__init__(self,map(UnitTestsBoundaryWalk,
#                                               ("test_found_boundary_is_a_complete_polygon",
#                                                "test_boundary_avoids_the_furthest_cut"))) 
# 
