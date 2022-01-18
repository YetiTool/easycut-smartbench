'''
Created on 13 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com
@author hugh.harford@poscoconsulting.com

Purpose: undertake geometry and return array of gcode coordinates that represent a boundary

TODO:         ########## 
    hard coded .nc path to be refactored

    # address this:
    # @@@@ HACK HACK HACK! a fix to close the polygon
           # see: in run_via_angle_checking_max_dist_n_range  




'''

import os.path
import math

# this is almost manual dependency injection:
import job_envelope_inc_circles as job_envelope 


class BCalculator():
    '''
    Purpose: undertake geometry and return array of gcode 
    coordinates that represent a boundary
    
    Considerable parts of this are superfluous given simplicity of 
    correctly datumed rectangle of job envelope
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
            # [2] = angle (from "north")
            # [3] = distance between x,y and datum
    
    boundary_calc_by_segment = [] # i.e. the boundary but in a 'nearest to a circle'
        # boundary_calc_by_segment will later be: 
            # [0] = x coord
            # [1] = y coord
            # [2] = distance between datum and x,y

    angle_sorted_boundary_xy = []

    datum_x = 0.0
    datum_y = 0.0
    
    bound_range_x = [0,0]
    bound_range_y = [0,0]
    
    temp_dist_to_boundary = 0.0
    temp_angle = 0.0
    

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
    segment_divisor = 10000000
    angle_max_check = math.pi/segment_divisor
    #
    ########### (see notes above on what this is for)
    
    def __init__(self):
        # re-set lists:
        self.boundary_xy = 0
        
        self.sort_gcode_input("")
        # instead of 
        # UnitTestsBoundaryWalk.test_boundary_datum_is_not_blank
        # use / see:
        #      self.b_setter.sort_gcode_input(self.gcode_file_path)

        # sort boundary by angle:
        self.sort_boundary_data_by_angle()
        # sort through, establishing boundary:
        self.run_via_angle_checking_max_dist_n_range()
    
    def sort_gcode_input(self, input_file_path_to_gcode = ""):
        # test gcode_file_path...
        self.gcode_file_path = "../../test/gcode_test_files/paired_gCode/Circles_and_star_1.gcode"
        # self.gcode_file_path = "../../test/gcode_test_files/jobCache_copy/Circle.nc"

        # this worked fine: "../../test/gcode_test_files/jobCache_copy/Circle.nc"
        # THE BELOW DOESN'T WORK - MUST PICK A FILE WITH .NC EXTENSION
        #    ../../test/gcode_test_files/jobCache_copy/Write Fineliner.gcode"
        # WORK FINE:
        #    ../../test/gcode_test_files/paired_gCode/Circles_and_star_1.gcode
        # set path to file, if provided
        if (input_file_path_to_gcode != ""): 
            self.gcode_file_path = input_file_path_to_gcode

        self.gcodefile = self.set_gcode_as_list(self.gcode_file_path)

        # get job range
        self.envelope_of_work = job_envelope.BoundingBox()
        self.envelope_of_work.set_job_envelope(self.gcode_file_path)

        ## this is a GETTER: so call from test: self.get_job_envelope_from_gcode()
        ## self.set_boundary_datum_point()
        

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
        ### see: run_via_angle_checking_max_dist_n_range
        # self.bound_range_x = [x_min, x_max]
        # self.bound_range_y = [y_min, y_max]
        
        found_envelope = ((self.bound_range_x[0],
                           self.bound_range_x[1]),
                           (self.bound_range_y[0],
                            self.bound_range_y[1]))
            


        return found_envelope

    def set_boundary_datum_point(self):
        # ### FOCUS POINT <<>>
        if len(self.envelope_of_work.range_x) < 3 and \
            len(self.envelope_of_work.range_y) < 3:
            
            print("HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP ")

        if self.datum_x == 0 and self.datum_y == 0:
            print("CHECKED AND WAS A A A A A BLANNNNNNNKKKKKKKEEEEEEEEEEEEEEEEEEEEEEEEEEEEEER")
        
            
        # set single x,y datum at job_envelop mid point
        self.datum_x = abs((self.envelope_of_work.range_x[0] 
                            - 
                            self.envelope_of_work.range_x[1])
                            /2)
        self.datum_y = abs((self.envelope_of_work.range_y[0] 
                            - 
                            self.envelope_of_work.range_y[1])
                            /2)
        
 
        if self.details_to_console == 1: 
            print("datum_x = " + str(self.datum_x))
            print("datum_y = " + str(self.datum_y))
            

    def check_point(self, in_x, in_y, datum):
        # use? math.angle_counterclockwise(a,b)
        
        temp_point = (in_x ,in_y)
        found_angle = self.b_setter.angle_from_datum(in_x, in_y, datum)
        dist_to_boundary = self.b_setter.distance_from_datum(in_x, in_y, datum)
            
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

        if self.details_to_console == 1: 
            print("dx, dy: " + str(dx) + "," + str(dy) + ", and " + str(dx**2 + dy**2))
            print("self.temp_dist_to_boundary = " + str(self.temp_dist_to_boundary))
    
    def add_coord_to_boundary(self, tp_x, tp_y):
        if self.boundary_xy == [[0.0, 0.0, 0.0, 0.0]]: # start, as has been reset
            self.boundary_xy = [[
                float(tp_x), 
                float(tp_y), 
                float(self.temp_angle), 
                float(self.temp_dist_to_boundary)
                ]]
        else: # append as needed
            self.boundary_xy.append([
                float(tp_x), 
                float(tp_y), 
                float(self.temp_angle), 
                float(self.temp_dist_to_boundary)
                ])

        if self.details_to_console == 1: 
            print(" add coord: \n" + str(tp_x) + " and " + str(tp_x))
            print(" add coord: \n" + str(self.boundary_xy))
    
    def set_gcode_as_list(self, incoming_gcode_file_path):
        self.datum = [self.datum_x, self.datum_y]
    # set first value to datum (required...?)
        temp_x = self.datum_x
        temp_y = self.datum_y
        self.temp_angle = 0.00001
        # temp values
        x_values = []
        y_values = []
        # reset boundary_xy 
        self.boundary_xy = [[0.0, 0.0, 0.0, 0.0]]
    # check file provided is there
        if os.path.isfile(incoming_gcode_file_path) == True:
            self.gcode_file_path = incoming_gcode_file_path
            if self.details_to_console == 1:
                print("gcode supplied: " + self.gcode_file_path)
        elif os.path.isfile(self.gcode_file_path) == False:
            print("gcode supplied path/file isn't working...  " + self.gcode_file_path)
            print("                      manually spec'd ERROR >>>>     " + str([99,88,77,"failed file"]))
            assert (1 == 0)
    # open GCODE file for use
        file_in_use = open(self.gcode_file_path,'r');
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
                        pass # z_values.append(float(part[1:])) # temp_z = float(part[1:])
                        
                # find angle from datum 
                ########## (just exactly what angle is calculated here...??)
                    self.angle_from_datum(temp_x, temp_y) 
                # find distance from datum:
                    self.distance_from_datum(temp_x, temp_y)
                # add data to boundary (datatype: self.boundary_xy): 
                    self.add_coord_to_boundary(temp_x, temp_y)
                except ZeroDivisionError:
                    pass
                    # print "Boundary calculator: skipped '" + part + "'"
                    
        file_in_use.close()
        
        if self.details_to_console == 1: 
            print("closed file, been through")
            print("boundary_xy: \n" + str(self.boundary_xy))
            print("boundary_xy length = " + str(len(self.boundary_xy)))
            # THIS
            print("boundary_xy length = " + str(len(self.boundary_xy)))

        return self.boundary_xy
        
    
    def sort_boundary_data_by_angle(self):
        # reset sorted b_xy:
        ### self.angle_sorted_boundary_xy = [[0.0, 0.0, 0.0, 0.0]]

        # sort the boundary_xy, creating a new sorted array
        # x[1] being 2nd column, angle:
            # x[0] = x coord
            # x[1] = y coord
            # x[2] = angle
            # x[3] = distance
        self.angle_sorted_boundary_xy = sorted(self.boundary_xy, key=lambda x: (x[2])) 
        # return self.angle_sorted_boundary_xy
    
    def run_via_angle_checking_max_dist_n_range(self):
        # go through the angle_sorted_boundary_xy and do 2 things:
        # a) find the max distance from the datum at that point
        # b) capture the boundary range while we are going through

        temp_max_dist_at_in_segment = 0
        start_segment = 99 # to indicate not-started
        # reset output list:
            # [0] = x coord
            # [1] = y coord
            # [2] = distance between datum and x,y
        self.boundary_calc_by_segment = [[0.0,0.0,0.0]]
        #####  loop logic (for boundary):
            # in each segment:
            #    start_segment = "recorded"
            #    if next_entry > start_segment + self.angle_max_check:
            #        record xy and angle into boundary_calc_by_segment
            #        IS THIS WHAT IS NEEDED LATER????
            #    else:
            #        check_if_latest_dist_is_greater
        
        ##### NOTE: also, as we go through, 
        #        capturing bound_range x & y
        #        ranges x,y, min max all set to 0
        ####     also setting object range values after loop end
        #    ranges x,y, min max all set to 0
        x_min = self.datum_x
        x_max = self.datum_x
        y_min = self.datum_y
        y_max = self.datum_y
        
        for x in range(len(self.angle_sorted_boundary_xy)-1):
            # get initial values
            x_value = self.angle_sorted_boundary_xy[x][0]
            y_value = self.angle_sorted_boundary_xy[x][1]
        #####
        ## @@@@@@@@@@@@@@ establishing x & y bound_range
        ## @@@ NOTE: this boundary range can be / will be APPROXIMATE
            # x values min and max
            if x_value > x_max: x_max = x_value
            if x_value < x_min: x_min = x_value
            # y values min and max
            if y_value > y_max: y_max = y_value
            if y_value < y_min: y_min = y_value
        #####
        ## @@@@@@@@@@@@@@ FIND DISTANCE FROM DATUM @ ANGLE
        #####   
            #### checking dist from datum
            #    as we go through via angle
            if start_segment == 99: # i.e. not populated yet (many times pi)
                start_segment = self.angle_sorted_boundary_xy[x][1]
            this_angle = self.angle_sorted_boundary_xy[x][1]
            if this_angle > start_segment + self.angle_max_check:    
                # record_max_dist_found into boundary_calc_by_segment
                if self.boundary_calc_by_segment == [[0.0,0.0,0.0]]:
                    self.boundary_calc_by_segment = [[
                        x_value,
                        y_value,
                        temp_max_dist_at_in_segment]]
                else:
                    self.boundary_calc_by_segment.append(
                        [x_value,
                         y_value, 
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
        # @@@@ HACK HACK HACK! a fix to close the polygon
        # @@@@ HACK HACK HACK! CLOSED OFF
        # self.boundary_calc_by_segment.append(self.boundary_calc_by_segment[0])
        
        ####### 
        # put the found range values into object.range_etc
        self.bound_range_x = [x_min, x_max]
        self.bound_range_y = [y_min, y_max]

        # debug print lines:        
        if self.details_to_console == 1:
            print("run_via_angle_checking_max_dist_n_range:") 
            print("  >> angle_max_check = " + str(self.angle_max_check) + 
                  " ___ i.e. PI / segment_divisor, where segment_divisor = " + 
                  str(self.segment_divisor))
            print("  >> datums: x(" + str(self.datum_x) + "), y(" + str(self.datum_y) + ")")
            print("  >> BOUND RANGE >>>>>>>>>>>>>> self.bound_range_x = " + 
                  str(self.bound_range_x))
            print("  >> BOUND RANGE >>>>>>>>>>>>>> self.bound_range_y = " + 
                  str(self.bound_range_y))
            print("  >> no. items in calc'd boundary = " + str(len(self.boundary_calc_by_segment)))
        
        return self.boundary_calc_by_segment
    
    def output_gcode_file(self, pathForOutput = ""):
        print("boundary_calculator.output_gcode:") 
        if pathForOutput != "":
            # actually run output
            
            pass
    