'''
Created 5 March 2020
@author: Letty
Module to store parameters and user choices for the Shape Cutter app
'''

import csv
import math

class ShapeCutterJobParameters(object):
    
    parameterCache_file_path = './asmcnc/shapeCutter_app/parameter_cache/'
    jobCache_file_path = './asmcnc/shapeCutter_app/shapeCutter_jobCache/'
    profile_filename = ""

    # internal settings:
    z_height_for_rapid_move = 3
    
    def __init__(self):
 
        # shape choices       
        self.shape_dict = {
            "shape": "",
            "cut_type": "",
            "dimensions": "",
            "units": "mm"
            }
        
        # shape dimensions
        self.circle_dimensions = {
            "D": "",
            "Z": ""
            }
        
        self.rectangle_dimensions = {
            "X": "",
            "Y": "",
            "Z": "",
            "R": ""
            }
        
        # parameters
        self.tabs = {
            "tabs?": "",
            "width": "",
            "height": "",
            "spacing": "",
            "units": "mm"
            }
        
        self.cutter_dimensions = {
            "diameter": "",
            "cutting length": "",
            "shoulder length": "",
            "units": "mm"
            }

        self.feed_rates = {
            "xy feed rate": "",
            "z feed rate": "",
            "spindle speed": "",
            "units": "mm"
            }
        
        self.strategy_parameters = {
            "stock bottom offset": "",
            "step down": "",
            "finishing passes": "",
            "units": "mm"
            }
        
        self.parameter_dict = {
            "tabs": self.tabs,
            "cutter dimensions": self.cutter_dimensions,
            "feed rates": self.feed_rates,
            "strategy parameters": self.strategy_parameters         
            }
    
    def validate_shape_dimensions(self):
        pass
    
    def validate_parameters(self):
        pass
 
    def load_parameters(self):
        
#        display_parameters = ''
        
        r = csv.reader(open(self.parameterCache_file_path + 'default' + '.csv', "r"), delimiter = '\t', lineterminator = '\n')
        for row in r:
#            display_parameters = display_parameters + '\t\t\t\t\t\t'.join(row) + '\n\r'
            if ('\t'.join(row)).split('\t')[0]in self.parameter_dict:
                current_group = ('\t'.join(row)).split('\t')[0]
            else:
                if ('\t'.join(row)).split('\t')[0] in self.parameter_dict[current_group]:
                    self.parameter_dict[current_group]('\t'.join(row)).split('\t')[0] = ('\t'.join(row)).split('\t')[1]        

        output = self.parameters_to_string()
        return output
    
    def save_parameters(self, filename):
        w = csv.writer(open(self.parameterCache_file_path + filename + '.csv', "w"), delimiter = '\t', lineterminator = '\n')
        for param_group, group_dict in self.parameter_dict.items():
            w.writerow([param_group])
            for param, value in group_dict.items():
                w.writerow(['', param, value])
    
    def parameters_to_string(self):       
        string_parameters = ''
        
        for param_group, group_dict in self.parameter_dict.items():
            string_parameters = string_parameters + str(param_group) + '\n\r'
            
            for param, value in group_dict.items():
                string_parameters = string_parameters + '\t' + str(param) + ':\t' + str(value) + '\n\r'

        return string_parameters

    def generate_gCode(self): # Generate GCode

        # adapted from Gcode file generator found at: 
        # https://github.com/YetiTool/GCodeFileGenerators/blob/master/shapes/shape_cut.py

        # MODE
        # shape = "rectangle"
        shape = self.shape_dict["shape"]
        aperture_or_island = self.shape_dict["cut_type"]
    
        
        # TAB PARAMS
        tabs = self.parameter_dict["tabs"]["tabs?"]
        tab_height = self.parameter_dict["tabs"]["height"]
        tab_width = self.parameter_dict["tabs"]["width"]
        tab_distance = self.parameter_dict["tabs"]["spacing"]
        
        # RECTANGLE PARAMETERS
        rect_job_x = self.shape_dict["dimensions"]["X"]
        rect_job_y = self.shape_dict["dimensions"]["Y"]
        rect_job_rad = self.shape_dict["dimensions"]["R"]
        
        # CIRCLE PARAMS
        circ_input_diameter = self.shape_dict["dimensions"]["D"]
        
        # TOOL
        cutter_diameter = self.parameter_dict["cutter dimensions"]["diameter"]
        cutter_rad = cutter_diameter/2
        
        # FEEDS AND SPEEDS
        xy_feed_rate = self.parameter_dict["feed rates"]["xy feed rate"]
        plunge_feed_rate = self.parameter_dict["feed rates"]["z feed rate"]
        spindle_speed = self.parameter_dict["feed rates"]["spindle speed"]
        
        # STRATEGY
        material_thickness = 10 # ?? 
        stock_bottom_offset = self.parameter_dict["strategy parameters"]["stock bottom offset"]
        stepdown = self.parameter_dict["strategy parameters"]["step down"]
        finishing_pass = self.parameter_dict["strategy parameters"]["finishing passes"]


        job_name = self.jobCache_file_path + shape + " " + aperture_or_island + self.profile_filename + ".nc"
        tab_absolute_height = -(material_thickness - tab_height)
        tab_effective_width = cutter_diameter + tab_width
        z_max = - material_thickness - stock_bottom_offset

        # RECTANGLE PARAMS
        
        if shape == "rectangle":
        
            if aperture_or_island == "aperture":
                # rectangle hack to save a bunch of logic to exclude rads for r0 case: 
                # rad will still be included but so small they won't be noticed visually.
                if rect_job_rad <= cutter_rad: rect_job_rad = cutter_rad + 0.01
                rect_path_rad = rect_job_rad - cutter_rad
                x_min = 0 + cutter_rad
                y_min = 0 + cutter_rad
                x_max = rect_job_x - cutter_rad
                y_max = rect_job_y - cutter_rad
                
            elif aperture_or_island == "island":
                if rect_job_rad == 0: rect_job_rad =  0.01
                rect_path_rad = rect_job_rad + cutter_rad
                x_min = 0 - cutter_rad
                y_min = 0 - cutter_rad
                x_max = rect_job_x + cutter_rad
                y_max = rect_job_y + cutter_rad
        
            # flat endpoints
            x_flat_min = rect_job_rad
            x_flat_max = rect_job_x - rect_job_rad
            y_flat_min = rect_job_rad
            y_flat_max = rect_job_y - rect_job_rad
            
            # tabs
            
            if tabs:
                
                rect_tab_offset_from_origin = cutter_rad # so tab doesn't start near the flat end point (potential errors with r0 hack
                
                # tab start point containers
                x_out_tabs = []
                x_rtn_tabs = []
                y_out_tabs = []
                y_rtn_tabs = []    
                
                # x-out
                x = x_flat_min + cutter_rad
                while x < (x_flat_max - cutter_rad - tab_effective_width):
                    x_out_tabs.append(x) 
                    x += tab_distance
            
                # x-rtn
                x = x_flat_max - cutter_rad
                while x > (x_flat_min + cutter_rad + tab_effective_width):
                    x_rtn_tabs.append(x) 
                    x -= tab_distance
            
                # y-out
                y = y_flat_min + cutter_rad
                while y < (y_flat_max - cutter_rad - tab_effective_width):
                    y_out_tabs.append(y) 
                    y += tab_distance
            
                # y-rtn
                y = y_flat_max - cutter_rad
                while y > (y_flat_min + cutter_rad + tab_effective_width):
                    y_rtn_tabs.append(y) 
                    y -= tab_distance
            
                print "Number of tabs in X axis: " + str(len(x_out_tabs))
                print "Number of tabs in Y axis: " + str(len(y_out_tabs))
        
            else:
                print "No tabs"
        
        # CIRCLE PARAMS
        
        elif shape == "circle":
            
            if aperture_or_island == "aperture":
                circ_path_rad = (circ_input_diameter - cutter_diameter) / 2
                
            elif aperture_or_island == "island":
                circ_path_rad = (circ_input_diameter + cutter_diameter) / 2
        
            if tabs:
                
                # calculate an even distribution of tabs along the circumference, based on desired distance between each (round down the distance between tabs as needed to achieve even distribution)
                # working in rads here
                
                total_circumference = 2.0 * math.pi * circ_path_rad
                circ_tabs_qty = math.ceil(total_circumference / tab_distance)
                circ_angle_between_tabs = (2.0 * math.pi) / circ_tabs_qty
                circ_angle_across_tab = (tab_effective_width / total_circumference) * (2.0 * math.pi)
        
        #         print total_circumference, circ_tabs_qty, circ_angle_between_tabs, circ_angle_across_tab, circ_path_rad, math.degrees(circ_angle_across_tab)
        
                circ_tab_start_pos = []
                circ_tab_end_pos = []
                
                circ_tab_start_angle = 0
        
                while circ_tab_start_angle < (2 * math.pi):
                    
                    # start co-ords
                    x = circ_path_rad * math.cos(circ_tab_start_angle)
                    y = circ_path_rad * math.sin(circ_tab_start_angle)
                    circ_tab_start_pos.append([round(x,6),round(y,6)])
                    
                    # end co-ords
                    circ_tab_end_angle = circ_tab_start_angle + circ_angle_across_tab
                    x = circ_path_rad * math.cos(circ_tab_end_angle)
                    y = circ_path_rad * math.sin(circ_tab_end_angle)
                    circ_tab_end_pos.append([round(x,6),round(y,6)])
                                
                    circ_tab_start_angle += circ_angle_between_tabs
                    
        
                
                    
        ################ GCODE GENERATOR ###############
        
        ######## GCODE HEADER
        
        lines = ['(' + job_name + ')',
                'G90', #Absolute
                'G94', #Feed units per mm
                'G17', #XY plane
                'G21', #In MM
                'M3 S25000', # Turn on spindle
                'G4 P1' # Allow time for inrush
                ]
        
        
        ###### GCODE SHAPE
        
        # Start pos
        
        lines.append("\n(Start of shape)")
        
        if shape == "rectangle":
            lines.append("G91.1") # relative rad centre definitions
            lines.append("G0 X" + str(x_flat_min) + " Y" + str(y_min))
        
        elif shape == "circle":
            lines.append("G90.1") # absolute rad centre definitions
            lines.append("G0 X" + str(circ_path_rad) + " Y" + str(0))
        
        lines.append("G0 Z" + str(z_height_for_rapid_move))
        
        
        z = -stepdown
        
        while z >= z_max:
            
            if shape == "rectangle":
                
                
                # plunge and draw square, anti-clockwise
                lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                
                # x-out
                if tabs and z < tab_absolute_height:
                    for start_tab_coord in x_out_tabs:
                        lines.append("G1 X" + str(start_tab_coord) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G1 X" + str(start_tab_coord + tab_effective_width) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                lines.append("G1 X" + str(x_flat_max) + " Y" + str(y_min) + " F" + str(xy_feed_rate))
                
                # rad 1
                lines.append("G3 X" + str(x_max) + " Y" + str(y_flat_min) + " I" + str(0) +  " J" + str(rect_path_rad))
                
                # y-out
                if tabs and z < tab_absolute_height:
                    for start_tab_coord in y_out_tabs:
                        lines.append("G1 Y" + str(start_tab_coord) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G1 Y" + str(start_tab_coord + tab_effective_width) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                lines.append("G1 X" + str(x_max) + " Y" + str(y_flat_max) + " F" + str(xy_feed_rate))
                
                # rad 2
                lines.append("G3 X" + str(x_flat_max) + " Y" + str(y_max) + " I" + str(-rect_path_rad) +  " J" + str(0))
                
                # x-rtn
                if tabs and z < tab_absolute_height:
                    for start_tab_coord in x_rtn_tabs:
                        lines.append("G1 X" + str(start_tab_coord) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G1 X" + str(start_tab_coord - tab_effective_width) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                lines.append("G1 X" + str(x_flat_min) + " Y" + str(y_max) + " F" + str(xy_feed_rate))
                
                # rad 3
                lines.append("G3 X" + str(x_min) + " Y" + str(y_flat_max) + " I" + str(0) +  " J" + str(-rect_path_rad))
                
                # y-rtn
                if tabs and z < tab_absolute_height:
                    for start_tab_coord in y_rtn_tabs:
                        lines.append("G1 Y" + str(start_tab_coord) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G1 Y" + str(start_tab_coord - tab_effective_width) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                lines.append("G1 X" + str(x_min) + " Y" + str(y_flat_min) + " F" + str(xy_feed_rate))
                
                # rad 4
                lines.append("G3 X" + str(x_flat_min) + " Y" + str(y_min) + " I" + str(rect_path_rad) +  " J" + str(0))
        
                
        
            elif shape == "circle":
                
        
                # plunge and draw circle, anti-clockwise
                lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                if tabs and z < tab_absolute_height:
                    for (xy_start, xy_end) in zip(circ_tab_start_pos, circ_tab_end_pos):
                        
                        lines.append("(Tab)")
                        if xy_start[0] != circ_path_rad: # hack to prevent repetition of co-ordinates from triggering a 360 degree revolution (makes sure that x co-ords aren't the same before appending - only works in this template with start point position etc)
                            lines.append("G3 X" + str(xy_start[0]) + " Y" + str(xy_start[1]) + " I0 J0 F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G3 X" + str(xy_end[0]) + " Y" + str(xy_end[1]) + " I0 J0 F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                  
                lines.append("G3 X" + str(circ_path_rad) + " Y0 I0 J0 F" + str(xy_feed_rate))
        
            # assess if final_pass
            if z == z_max and finishing_pass <= 0: break
            if z == z_max and finishing_pass > 0: finishing_pass -= 1
        
            # increment z down for next pass
            z -= stepdown
            if z < z_max: z = z_max
            
        
        ######## GCODE FOOTER
        
        lines.append("\n(Shutdown)")
        lines.append("G0 Z" + str(z_height_for_rapid_move))
        lines.append("M5") #Kill spindle
        lines.append("G4 P2") #Pause for vac overrun
        lines.append("M30") #Prog end
        lines.append("%") #Prog end (redundant?)
          
        f = open(job_name, "w")
        for line in lines:
            f.write(line + "\n")   
        
        print "Done: " + job_name

        