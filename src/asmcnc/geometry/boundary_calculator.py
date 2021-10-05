'''
Created on 13 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com

TODO:         ########## 
    hard coded .nc path to be refactored


Purpose: undertake geometry and return array of gcode coordinates that represent a boundary


'''

import os.path

import numpy

import job_envelope

# import screen_test
# from apps.shapeCutter_app import screen_manager_shapecutter

# from kivy.app import App


class BoundaryCalculator():
    '''
    Purpose: undertake geometry and return array of gcode coordinates that represent a boundary
    
    '''
    detailsToConsole = 0
    
    gcode_file_path = ""
    datum_x = 0.0
    datum_y = 0.0
    boundarySetter = object
    boundary_xy = []
    boundary_details = []

    

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


    def set_boundary_datum_point(self):
        
        # set single x,y datum at job_envelop mid point
        self.datum_x = abs((self.boundarySetter.range_x[0] - self.boundarySetter.range_x[1])/2)
        self.datum_y = abs((self.boundarySetter.range_y[0] - self.boundarySetter.range_y[1])/2)
 
        if self.detailsToConsole == 1: 
            print("datum_x = " + str(self.datum_x))
            print("datum_y = " + str(self.datum_y))
    
   
    def get_boundary_as_gcode_list(self):
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
    
    def angle_from_datum(self, in_x, in_y, datum):
        found_angle = 25.2
        return found_angle
    
    def distance_from_datum(self, in_x, in_y, datum):
        dist_to_boundary = 7
        return dist_to_boundary
    
    def add_coord_to_boundary(self, tp_x, tp_y, angle, dist):
        
        global boundary_xy, boundary_details
        
        
        boundary_xy.append((float(tp_x), float(tp_y)))
        
        # boundary_details.append((tp_x, tp_y, angle, dist))
        print(" add coord: \n" + str(tp_x) + " and " + str(tp_x))

        print(" add coord: \n" + str(boundary_xy))
    
    def set_gcode_as_list(self, gcode_file_path):
        global boundary_xy, boundary_details
        # get datum for use later in this function
        datum = (self.datum_x, self.datum_y)
        # set first value to datum (required...?)
        temp_x = datum[0]
        temp_y = datum[1]
        
        # initially copied from job_envelope.set_job_envelope
        x_values = []
        y_values = []

        if os.path.isfile(gcode_file_path) != True:
            print("gcode supplied path/file isn't working...  " + gcode_file_path)
        else: print("gcode supplied: " + gcode_file_path)
        
        file_in_use = open(gcode_file_path,'r');
        
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

                    # angle = self.boundarySetter.angle_from_datum(temp_x, temp_y, datum)
                    # dist = self.boundarySetter.distance_from_datum(temp_x, temp_y, datum)
                    self.add_coord_to_boundary(18, 89, 23, 34)
                    
                except:
                    pass
                    # print "Boundary calculator: skipped '" + part + "'"
                    
        file_in_use.close()
        print("closed file, been through")
        
        
        print("boundary_xy: \n" + str(self.boundary_xy))
        
        return self.boundary_xy
        
    def get_gcode_path(self):
        ## print("gcode_file_path = " + gcode_file_path)
        return gcode_file_path

