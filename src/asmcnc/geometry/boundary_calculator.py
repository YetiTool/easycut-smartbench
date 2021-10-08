'''
Created on 13 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com

TODO:         ########## 
    hard coded .nc path to be refactored


Purpose: undertake geometry and return array of gcode coordinates that represent a boundary


'''

import os.path
import math
import numpy
import job_envelope
# import screen_test # from apps.shapeCutter_app import screen_manager_shapecutter
# from kivy.app import App


class BoundaryCalculator():
    '''
    Purpose: undertake geometry and return array of gcode coordinates that represent a boundary
    '''
    detailsToConsole = 0
    
    gcode_file_path = ""
    boundarySetter = object

    datum_x = 0.0
    datum_y = 0.0
    
    bound_range_x = [0,0]
    bound_range_y = [0,0]
    
    temp_dist_to_boundary = 0.0
    temp_angle = 0.0
    
    boundary_xy = []
    angle_sorted_boundary_xy = []
    boundary_calc_by_segment = [] # i.e. the boundary but in a 'nearest to a circle'
    
    # approximations (to speed up processing etc)
    # ANGLE to check for max distance from datum against
    # N.B. in radians (proportions of PI, so 2*pi for a full circle)
    ## i.e. see run_via_angle_checking_max_dist_n_range()
    ## which checks for a max_dist at a segement
    ## e.g. 
    ##    if the angle_max_check was PI
    ##    then there would only be 2 measurements:
    ##    1: for -pi to 0 
    ##    2: for 0 to pi
    ##    there will, of course be lots more than 2!
    ###########
    #
    segment_divisor = 10000
    angle_max_check = math.pi/segment_divisor
    #
    ########### (see notes above on what this is for)

    # ????????????????///
    # st = screen_test
    # stm = screen_manager_shapecutter
    
    def __init__(self, file_path_to_gcode = ""):
        '''
        Constructor (really, I understood that __new__ was the constructor?)
        '''
        global gcode_file_path
        
        # expected path
        gcode_file_path = "../../test/gcode_test_files/jobCache_copy/Circle.nc"

        # set path to file, if provided
        if (file_path_to_gcode != ""):
            gcode_file_path = file_path_to_gcode

        # THE BELOW DOESN'T WORK - MUST PICK A FILE WITH .NC EXTENSION
        #    ../../test/gcode_test_files/jobCache_copy/Write Fineliner.gcode"
        self.boundarySetter = job_envelope.BoundingBox()
        
        # get job range
        self.boundarySetter.set_job_envelope(gcode_file_path)


        ## TRYING TO SET UP A SCREEN
        # self.st = screen_test.ScreenTest(App)
        # self.stm = self.st.build()

    def get_job_envelope_from_gcode(self):
        new_gcode_boundary_setter = job_envelope.BoundingBox()
        new_gcode_boundary_setter.set_job_envelope(gcode_file_path)
        found_envelope = (new_gcode_boundary_setter.range_x, 
                          new_gcode_boundary_setter.range_y) 
        return found_envelope
    
    def get_job_envelope_xy_list(self):

        found_boundary_range_x = [0,0]
        found_boundary_range_y = [88.0,88.1]

        # MAKE SURE TO DO BOTH ENDS OF RANGE:
        # ### , found_boundary_range_x[1] = max(self.boundary_calc_by_segment[:][1][1])
        found_boundary_range_x[0] = min(1,2,3,4,5,6,78,-99)
            # self.boundary_calc_by_segment[1][1])
        z = 0
        print(" ***** self.boundary_calc_by_segment[z]: " 
              + str(self.boundary_calc_by_segment[:][z][0]))
        print(" ***** _______ min found = " + 
              str(min(self.boundary_calc_by_segment[:][z][0])))
        
        # found_boundary_range_x[0], found_boundary_range_x[1] = 0.009
        
        # self.range_x[0], self.range_x[1] = min(x_values), max(x_values)
        # self.range_y[0], self.range_y[1] = min(y_values), max(y_values)
        found_envelope = ((found_boundary_range_x[0]
                           ,found_boundary_range_x[1]),(found_boundary_range_y[0],found_boundary_range_y[1]))
            
            # new_xylist_boundary_setter.range_x, 
            #              new_xylist_boundary_setter.range_y)
        
        print("found_envelope: " + str(found_envelope))
        
        return found_envelope

    def set_boundary_datum_point(self):
        
        # set single x,y datum at job_envelop mid point
        self.datum_x = abs((self.boundarySetter.range_x[0] - self.boundarySetter.range_x[1])/2)
        self.datum_y = abs((self.boundarySetter.range_y[0] - self.boundarySetter.range_y[1])/2)
 
        if self.detailsToConsole == 1: 
            print("datum_x = " + str(self.datum_x))
            print("datum_y = " + str(self.datum_y))
    
   
    def get_sample_boundary_as_gcode_list(self):
        sampleArray = [5,10,15,5] # providing a double fails the unit test, e.g. 5.5 
        return sampleArray
    

    
    def check_point(self, in_x, in_y, datum):
        
        # math.angle_counterclockwise(a,b)
        
        # temp_point = (0, 0)
        temp_point = (in_x ,in_y)
        
        # found_angle = 0.001
        # dist_to_boundary = 0.001
        
        found_angle = self.boundarySetter.angle_from_datum(in_x, in_y, datum)
        dist_to_boundary = self.boundarySetter.distance_from_datum(in_x, in_y, datum)
            
        print("found angle and distance: " + str(found_angle) + 
              ", dist: " + str(dist_to_boundary) + 
              ", for point: " + str(temp_point))
        
        temp_point_angle_dist = (temp_point, found_angle, dist_to_boundary)

        return temp_point_angle_dist
    
    def angle_from_datum(self, in_x, in_y):
        # set dy, dx
        dx = in_x - self.datum_x
        dy = in_y - self.datum_y   
        # calculate angle 
        found_angle = math.atan2(dy, dx)  
        self.temp_angle = float(found_angle)
        # print("self.temp_angle = " + str(self.temp_angle))

    def distance_from_datum(self, in_x, in_y):
        # set dx and dy
        dx = in_x - self.datum_x
        dy = in_y - self.datum_y
        # calculate absolute distance:
        self.temp_dist_to_boundary = math.sqrt(abs(dx**2 + dy**2))

        if self.detailsToConsole == 1: 
            print("dx, dy: " + str(dx) + "," + str(dy) + ", and " + str(dx**2 + dy**2))
            print("self.temp_dist_to_boundary = " + str(self.temp_dist_to_boundary))
    
    def add_coord_to_boundary(self, tp_x, tp_y):
        global boundary_xy, boundary_xy_string, boundary_details
        # actual values: 
        self.boundary_xy.append([
             (
                 float(tp_x), 
                 float(tp_y)
                 ), 
             float(self.temp_angle), 
             float(self.temp_dist_to_boundary)
             ])
        # single string:
        # temp_string = str(tp_x) + ", " + str(tp_y) + ", " + str(angle) + ", " + str(dist)
        # self.boundary_xy_string.append(temp_string)
        if self.detailsToConsole == 1: 
            print(" add coord: \n" + str(tp_x) + " and " + str(tp_x))
            print(" add coord: \n" + str(boundary_xy))
    
    def set_gcode_as_list(self, gcode_file_path):
        global boundary_xy, boundary_details
        global boundarySetter
        datum = [self.datum_x, self.datum_y]
    # set first value to datum (required...?)
        temp_x = self.datum_x
        temp_y = self.datum_y
        self.temp_angle = 0.00001
    # initially copied from job_envelope.set_job_envelope
        x_values = []
        y_values = []
    # check file provided is there
        if os.path.isfile(gcode_file_path) == True:
            print("gcode supplied: " + gcode_file_path)
        elif os.path.isfile(gcode_file_path) == False:
            print("gcode supplied path/file isn't working...  " + gcode_file_path)
            print("                      manually spec'd ERROR >>>>     " + str([99,88,77,"failed file"]))
            assert (1 == 0)
    # open GCODE file 
        file_in_use = open(gcode_file_path,'r');
    # go through line(s) and get out the x,y   
        for line in file_in_use:
            blocks = line.strip().split(" ")
            for part in blocks:
                try:
                    # grab the coordinates, as they change
                    if part.startswith(('X')): 
                        x_values.append(float(part[1:]))
                        temp_x = float(part[1:])
                    if part.startswith(('Y')): 
                        y_values.append(float(part[1:]))
                        temp_y = float(part[1:])
                    if part.startswith(('Z')): 
                        # z_values.append(float(part[1:]))
                        # temp_z = float(part[1:])
                        pass
                # find angle from datum 
                ########## (just exactly what angle is calculated here...??)
                    self.angle_from_datum(temp_x, temp_y) 
                # find distance from datum:
                    self.distance_from_datum(temp_x, temp_y)
                # add data to boundary (datatype: self.boundary_xy): 
                    self.add_coord_to_boundary(temp_x, temp_y)
                except:
                    pass
                    # print "Boundary calculator: skipped '" + part + "'"
                    
        file_in_use.close()
        print("closed file, been through")
        
        if self.detailsToConsole == 1: 
            print("boundary_xy: \n" + str(self.boundary_xy))
            print("boundary_xy length = " + str(len(self.boundary_xy)))
        print("boundary_xy length = " + str(len(self.boundary_xy)))

        return self.boundary_xy
        
    def get_gcode_path(self):
        ## print("gcode_file_path = " + gcode_file_path)
        return gcode_file_path
    
    def sort_boundary_data_by_angle(self):
        # global boundary_xy, boundary_details
        # global boundarySetter
        
        # sort the boundary_xy, creating a new sorted array
        # x[1] being 2nd column, angle:
            # x[0] = (x,y)
            # x[1] = angle
            # x[2] = distance
         
        self.angle_sorted_boundary_xy = sorted(self.boundary_xy, key=lambda x: (x[1])) 
        
        return self.angle_sorted_boundary_xy
    
    def run_via_angle_checking_max_dist_n_range(self):
        print("angle_max_check = " + str(self.angle_max_check) + 
              " ___ i.e. PI / segment_divisor, where segment_divisor = " + str(self.segment_divisor))
        temp_max_dist_at_in_segment = 0
        start_segment = 99 # to indicate no-started
        
        #####  loop logic:
            # in each segment:
            #    start_segment = "recorded"
            #    if next_entry > start_segment + self.angle_max_check:
            #        record xy and angle into boundary_calc_by_segment
            #        IS THIS WHAT IS NEEDED LATER????
            #    else:
            #        check_if_latest_dist_is_greater
        
        ##### NOTE: also, as we go through, 
        #           capturing bound_range x & y
        
        for x in range(len(self.angle_sorted_boundary_xy)-1):
            
            #### establishing x & y bound_range
            #
            
            
            #### checking dist from datum
            #    as we go through via angle
            if start_segment == 99: # i.e. not populated yet
                start_segment = self.angle_sorted_boundary_xy[x][1]
            this_angle = self.angle_sorted_boundary_xy[x][1]
            if this_angle > start_segment + self.angle_max_check:    
                # record_max_dist_found into boundary_calc_by_segment
                self.boundary_calc_by_segment.append(
                    [self.angle_sorted_boundary_xy[x][0][0],
                     self.angle_sorted_boundary_xy[x][0][1], 
                     temp_max_dist_at_in_segment]
                    )
                # RESET
                # set temp_max_dist_at_in_segment to 0
                temp_max_dist_at_in_segment = 0
                # reset segment too
                start_segment = self.angle_sorted_boundary_xy[x][1]

            else: 
                # check_if_latest_dist_is_greater
                if self.angle_sorted_boundary_xy[x][2] > temp_max_dist_at_in_segment:
                    # if so, replace temp_max with greater distance
                    temp_max_dist_at_in_segment = self.angle_sorted_boundary_xy[x][2]
        
        # artificially close the polygon of the boundary
        # HACK HACK HACK!
        self.boundary_calc_by_segment.append(
                    self.boundary_calc_by_segment[0]
                    )
        
        
        print("no items in calc'd boundary = " + str(len(self.boundary_calc_by_segment)))
        
        return self.boundary_calc_by_segment
    
    
    