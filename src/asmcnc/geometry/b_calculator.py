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
import asmcnc.geometry.job_env_w_arc as job_env 

class BCalculator():
    '''
    Purpose: undertake geometry and return array of gcode 
    coordinates that represent a simple rectangular boundary
    '''
    gcode_file_path = ""
    gcodefile = []
    datum_x = 0.999
    datum_y = 0.999
    bound_range_x = [0,0]
    bound_range_y = [0,0]
    
    def __init__(self):
        '''
        Resets boundary for security
        '''
        self.boundary_xy = [[0.0, 0.0]]  # re-set lists
        self.sort_gcode_input("")  # get list of x,y gcode from gcode file
    
    def set_gcode_file(self, to_set_file_path_to_gcode):
        self.gcode_file_path = to_set_file_path_to_gcode
    
    def sort_gcode_input(self, to_sort_file_path_to_gcode = ""):
        '''
        sort_gcode_input: get list of x,y gcode from gcode file
        blank string parameter defaults to path set inside this function:
        "test/gcode_test_files/paired_gCode/Circles_and_star_1.gcode"
        "test/gcode_test_files/paired_gCode/Square_1.gcode"
        "test/gcode_test_files/paired_gCode/Square 1 - maximum job dimensions.gcode"

        '''
        # default test gcode_file_path...
        workable_gcode_file_path = "test/gcode_test_files/paired_gCode/Square 1 - maximum job dimensions.gcode"
        if to_sort_file_path_to_gcode == "" and self.gcode_file_path == "":  
            # set path to file, if provided
            self.gcode_file_path = workable_gcode_file_path
        elif self.gcode_file_path != to_sort_file_path_to_gcode:
            # set if not already
            self.set_gcode_file(to_sort_file_path_to_gcode)
        
        # get job range
        self.job_env = job_env.BoundingBox()
        self.job_env.set_job_envelope(self.gcode_file_path)

    def get_job_env(self):
        return (self.job_env.range_x,
                          self.job_env.range_y) 

    def get_gcode_path(self):
        return self.gcode_file_path
    
    def get_job_env_bound(self):
        return ((self.bound_range_x[0],
                self.bound_range_x[1]),
                (self.bound_range_y[0],
                self.bound_range_y[1]))

    def set_boundary_datum_point(self):
        # ### FOCUS POINT <<>>
        # set single x,y datum at job_envelop mid point
        self.datum_x = abs((self.job_env.range_x[0] 
                            - 
                            self.job_env.range_x[1])
                            /2)
        self.datum_y = abs((self.job_env.range_y[0] 
                            - 
                            self.job_env.range_y[1])
                            /2)
        