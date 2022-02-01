'''
Created on 13 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com
@author hugh.harford@poscoconsulting.com

Purpose: undertake geometry and return array of gcode coordinates that 
        represent a simple rectangular boundary

TODO:         ########## 
    hard coded .nc path to be refactored

'''
import os.path
import math
# this is almost manual dependency injection:
import src.asmcnc.geometry.job_envelope_inc_circles as job_envelope 

class BCalculator():
    '''
    Purpose: undertake geometry and return array of gcode 
    coordinates that represent a simple rectangular boundary
    '''
    # for debugging levels / details
    details_to_console = 11  
    envelope_of_work = object
    gcode_file_path = ""
    gcodefile = []
    boundary_xy = []
        # boundary_xy will later be: 
            # [0] = x coord
            # [1] = y coord
    datum_x = 0.0
    datum_y = 0.0
    bound_range_x = [0,0]
    bound_range_y = [0,0]
    
    def __init__(self):
        # re-set lists:
        self.boundary_xy = [[0.0, 0.0]]
        # get list of x,y gcode from gcode file 
        self.sort_gcode_input("")
    
    def sort_gcode_input(self, input_file_path_to_gcode = ""):
        '''
        sort_gcode_input: get list of x,y gcode from gcode file
        '''
        # test gcode_file_path...
        self.gcode_file_path = "test/gcode_test_files/paired_gCode/Circles_and_star_1.gcode"
        # "test/gcode_test_files/paired_gCode/Circles_and_star_1.gcode"
        # THE BELOW DOESN'T WORK - MUST PICK A FILE WITH .NC EXTENSION

        if (input_file_path_to_gcode != ""): # set path to file, if provided
            self.gcode_file_path = input_file_path_to_gcode

        # get job range
        self.envelope_of_work = job_envelope.BoundingBox()
        self.envelope_of_work.set_job_envelope(self.gcode_file_path)

    def get_job_envelope_from_gcode(self):
        
        if self.details_to_console == 11: 
            print(">>>> get_job_envelope_from_gcode ____________ ") # + self.gcode_file_path)

        found_envelope = (self.envelope_of_work.range_x, 
                          self.envelope_of_work.range_y) 
        return found_envelope

    def get_gcode_path(self):
        ## print("gcode_file_path = " + gcode_file_path)
        return self.gcode_file_path
    
    def get_job_envelope_xy_list(self):
        found_envelope = ((self.bound_range_x[0],
                           self.bound_range_x[1]),
                           (self.bound_range_y[0],
                            self.bound_range_y[1]))
        return found_envelope

    def set_boundary_datum_point(self):
        # ### FOCUS POINT <<>>
        # set single x,y datum at job_envelop mid point
        self.datum_x = abs((self.envelope_of_work.range_x[0] 
                            - 
                            self.envelope_of_work.range_x[1])
                            /2)
        self.datum_y = abs((self.envelope_of_work.range_y[0] 
                            - 
                            self.envelope_of_work.range_y[1])
                            /2)
        