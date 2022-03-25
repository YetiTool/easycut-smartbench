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
    datum_x = 0.9999999898989
    datum_y = 0.9999999787878
    # bound_range_x = [0,0]
    # bound_range_y = [0,0]
    
    def __init__(self):
        '''
        Resets boundary for security
        '''
        self.job_env = job_env.BoundingBox()

    def go_over_gcode_input(self, to_set_file_path_to_gcode):
        self.gcode_file_path = to_set_file_path_to_gcode
        self.sort_gcode_input(self.gcode_file_path)
        self.set_core_gcode_properties()
        """
            This is where the main action is RUN FROM

        Args:
            to_sort_file_path_to_gcode (str, optional): _description_. Defaults to "".
        """
    
    def sort_gcode_input(self, to_sort_file_path_to_gcode = ""):

        
        '''
        sort_gcode_input: get list of x,y gcode from gcode file
        blank string parameter defaults to path set inside this function:
        "test/gcode_test_files/paired_gCode/Circles_and_star_1.gcode"
        "test/gcode_test_files/paired_gCode/Square_1.gcode"
        "test/gcode_test_files/paired_gCode/Square 1 - maximum job dimensions.gcode"

        '''
        # default test gcode_file_path...
        #_MANUAL_DEFAULT_DISABLED_FOR_TESTING_>>>
        workable_gcode_file_path = "test/boundary_walk_test_files/paired_gCode/Square 1 - maximum job dimensions.gcode"
        if to_sort_file_path_to_gcode == "" and self.gcode_file_path == "":  
            # set path to file, if provided
            self.gcode_file_path = workable_gcode_file_path
        elif self.gcode_file_path != to_sort_file_path_to_gcode:
            # set if not already
            self.go_over_gcode_input(to_sort_file_path_to_gcode)
        
        # get job envelope, range etc
        self.job_env.set_job_envelope(self.gcode_file_path)

    def get_job_env(self):
        print('job_env.range_x: {}, job_env.range_y: {}'.format(
            self.job_env.range_x, self.job_env.range_y))
        return (self.job_env.range_x,
                          self.job_env.range_y) 

    def get_gcode_path(self):
        return self.gcode_file_path

    # THINK THESE ARE IRRELEVANT FOR NOW
    #    
    # def get_job_env_bound(self):
    #     return ((self.bound_range_x[0],
    #             self.bound_range_x[1]),
    #             (self.bound_range_y[0],
    #             self.bound_range_y[1]))

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
    
    def set_core_gcode_properties(self):
        if self.job_env.count_arc_gcodelines > 0: 
            print('Found arcs... {}'.format(self.job_env.count_arc_gcodelines))

        if self.job_env.count_linear_gcodelines > 0:
            print('Found linear lines: {}'.format(self.job_env.count_linear_gcodelines))
