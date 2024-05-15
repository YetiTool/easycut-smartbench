'''
Created 5 March 2020
@author: Letty
Module to store parameters and user choices for the Shape Cutter app
'''

import csv
import math
import re

from asmcnc.comms.logging_system.logging_system import Logger


class ShapeCutterJobParameters(object):
    
    
    parameterCache_file_path = './asmcnc/apps/shapeCutter_app/parameter_cache/'
    jobCache_file_path = './jobCache/'

    # Internal settings
    z_height_for_rapid_move = 3
    
    def __init__(self, machine, shapecutter_sm):
 
        self.m = machine
        self.shapecutter_sm = shapecutter_sm
        
        self.refresh_parameters()

    def refresh_parameters(self):
        # Defaults are all in mm
        
        self.profile_filename = ""
        
        # parameters
        self.parameter_string = ''
        
        # gcode
        self.gcode_lines = []
        self.gcode_filename = ''
        self.gcode_job_name = ''
        
        # shape dimensions
        self.circle_dimensions = {
            "D": 100,
            "Z": 6
            }
        
        self.rectangle_dimensions = {
            "X": 100,
            "Y": 100,
            "Z": 6,
            "R": 10
            }
        
        # shape choices       
        self.shape_dict = {
            "shape": "",
            "cut_type": "",
            "dimensions": self.circle_dimensions,
            "units": "mm"
            }
        
        # parameters
        self.tabs = {
            "tabs?": True,
            "width": 12,
            "height": 3,
            "spacing": 60,
            "units": "mm"
            }
        
        self.cutter_dimensions = {
            "diameter": 6.35,
            "cutting length": 20,
            "shoulder length": 30,
            "units": "mm"
            }

        self.feed_rates = {
            "xy feed rate": 2000,
            "z feed rate": 300,
            "spindle speed": 25000,
            "units": "mm"
            }
        
        self.strategy_parameters = {
            "stock bottom offset": 1,
            "step down": 3,
            "finishing passes": 0,
            "units": "mm"
            }
        
        self.parameter_dict = {
            "tabs": self.tabs,
            "cutter dimensions": self.cutter_dimensions,
            "feed rates": self.feed_rates,
            "strategy parameters": self.strategy_parameters         
            }

        # Bounding box
        self.range_x = [0,0] 
        self.range_y = [0,0] 
        self.range_z = [0,0]
    
    def validate_shape_dimensions(self, dim, input):

        if self.shape_dict["units"] == "inches": 
            multiplier = 1/25.4
            self.tabs_in_inches()
        else: 
            multiplier = 1
            self.tabs_in_mm()
        
        max_X = self.m.s.setting_130*multiplier
        max_Y = self.m.s.setting_131*multiplier
        max_Z = self.m.s.setting_132*multiplier
        
        if dim == "X":
            
            if not input < max_X: return max_X
            if not input > 0: return max_X
            
            self.shape_dict["dimensions"]["X"] = input
            
        elif dim == "Y":
            
            if not input < max_Y: return max_Y
            if not input > 0: return max_Y
        
            self.shape_dict["dimensions"]["Y"] = input
        
        elif dim == "Z":
            
            if not input < max_Z: return max_Z
            if not input > 0: return max_Z
            
            self.shape_dict["dimensions"]["Z"] = input
            
        elif dim == "R":
            
            max_R = min(self.shape_dict["dimensions"]["X"], self.shape_dict["dimensions"]["Y"])

            if not input < max_R: return max_R
            if not input >= 0: return max_R
            
            self.shape_dict["dimensions"]["R"] = input
            
        elif dim == "D":

            if not input < max_X: return max_X
            if not input > 0: return max_X
            
            self.shape_dict["dimensions"]["D"] = input
        
        return True

    def tabs_in_inches(self):
        
        if self.parameter_dict["tabs"]["units"] == "mm":
            tab_unit_multiplier = 1/25.4
            self.parameter_dict["tabs"]["units"] = "inches"
            self.parameter_dict["tabs"]["height"] = float(self.parameter_dict["tabs"]["height"])*tab_unit_multiplier
            self.parameter_dict["tabs"]["width"] = float(self.parameter_dict["tabs"]["width"])*tab_unit_multiplier
            self.parameter_dict["tabs"]["spacing"] = float(self.parameter_dict["tabs"]["spacing"])*tab_unit_multiplier

    def tabs_in_mm(self):
        
        if self.parameter_dict["tabs"]["units"] == "inches":
            tab_unit_multiplier = 25.4
            self.parameter_dict["tabs"]["units"] = "mm"
            self.parameter_dict["tabs"]["height"] = float(self.parameter_dict["tabs"]["height"])*tab_unit_multiplier
            self.parameter_dict["tabs"]["width"] = float(self.parameter_dict["tabs"]["width"])*tab_unit_multiplier
            self.parameter_dict["tabs"]["spacing"] = float(self.parameter_dict["tabs"]["spacing"])*tab_unit_multiplier

    def validate_cutter_dimensions(self, param, input):
        
        if self.shape_dict["units"] == "inches" and self.parameter_dict["cutter dimensions"]["units"] == "mm": 
            multiplier = 25.4
        elif self.shape_dict["units"] == "mm" and self.parameter_dict["cutter dimensions"]["units"] == "inches":
            multiplier = 1/25.4
        else:
            multiplier = 1
            
        min_CZ = self.shape_dict["dimensions"]["Z"]*multiplier
        min_CB = self.parameter_dict["cutter dimensions"]["cutting length"]

        if param == "diameter":
            if not input > 0: return 26*multiplier
            if not input <= 26*multiplier: return 26*multiplier
            self.parameter_dict["cutter dimensions"]["diameter"] = input
            
        elif param == "cutting length":
            if not input > 0: return 0
            self.parameter_dict["cutter dimensions"]["cutting length"] = input
        
        elif param == "shoulder length":
            if not input > min_CZ: return min_CZ
            if not input > min_CB: return min_CB   
            self.parameter_dict["cutter dimensions"]["shoulder length"] = input
        
        return True

    def validate_tabs(self, param, input):
       
        if self.shape_dict["units"] == "inches" and self.parameter_dict["tabs"]["units"] == "mm": 
            multiplier = 25.4
        elif self.shape_dict["units"] == "mm" and self.parameter_dict["tabs"]["units"] == "inches":
            multiplier = 1/25.4
        else:
            multiplier = 1
            
        if param == "width":
            
            if self.parameter_dict["cutter dimensions"]["units"] == "inches" and self.shape_dict["units"] == "mm": 
                width_max_multiplier = 25.4
            elif self.parameter_dict["cutter dimensions"]["units"] == "mm" and self.shape_dict["units"] == "inches":
                width_max_multiplier = 1/25.4
            else:
                width_max_multiplier = 1
                
                
            if self.shape_dict["shape"] == "rectangle":          
                width_max = (min(self.shape_dict["dimensions"]["X"],self.shape_dict["dimensions"]["Y"]) \
                                - 2*self.shape_dict["dimensions"]["R"] \
                                - 2*self.parameter_dict["cutter dimensions"]["diameter"]*width_max_multiplier)*multiplier
            
            elif self.shape_dict["shape"] == "circle": 
                width_max = (math.pi*self.shape_dict["dimensions"]["D"] \
                - self.parameter_dict["cutter dimensions"]["diameter"]*width_max_multiplier)*multiplier
            
            if not input > 0: return width_max
            if not input < width_max: return width_max
            self.parameter_dict["tabs"]["width"] = input
            
        elif param == "height":
            max_height = self.shape_dict["dimensions"]["Z"]*multiplier
            if not input < max_height: return max_height
            self.parameter_dict["tabs"]["height"] = input
        
        elif param == "spacing":

            if self.parameter_dict["cutter dimensions"]["units"] == "inches" and self.parameter_dict["tabs"]["units"] == "mm": 
                spacing_multiplier = 25.4
            elif self.parameter_dict["cutter dimensions"]["units"] == "mm" and self.parameter_dict["tabs"]["units"] == "inches":
                spacing_multiplier = 1/25.4
            else:
                spacing_multiplier = 1
            
            min_spacing = self.parameter_dict["tabs"]["width"] + \
                        self.parameter_dict["cutter dimensions"]["diameter"]*spacing_multiplier
            
            if not input > min_spacing: return min_spacing
            self.parameter_dict["tabs"]["spacing"] = input

        return True
        
    def validate_feed_rates(self, param, input):

        if param == "xy feed rate":
            if not input > 0: return 0
            self.parameter_dict["feed rates"]["xy feed rate"] = input
            
        elif param == "z feed rate":
            if not input > 0: return 0
            self.parameter_dict["feed rates"]["z feed rate"] = input
        
        elif param == "spindle speed":
            if input < 6000 or input > 25000: return False
            self.parameter_dict["feed rates"]["spindle speed"] = input
        
        return True
    
    def validate_strategy_parameters(self, param, input):

        if self.parameter_dict["cutter dimensions"]["units"] == "inches" and self.parameter_dict["strategy parameters"]["units"] == "mm": 
            multiplier = 25.4
        elif self.parameter_dict["cutter dimensions"]["units"] == "mm" and self.parameter_dict["strategy parameters"]["units"] == "inches":
            multiplier = 1/25.4
        else:
            multiplier = 1

        if param == "stock bottom offset":
            if input < 0: return 0
            self.parameter_dict["strategy parameters"]["stock bottom offset"] = input
            
        elif param == "step down":
            
            warning_step_down = (float(self.parameter_dict["cutter dimensions"]["diameter"])*multiplier) / 2
            
            if input > (float(self.shape_dict["dimensions"]["Z"])): return (float(self.shape_dict["dimensions"]["Z"]))
            if not input > 0: return 0
            if input > warning_step_down: return False
            self.parameter_dict["strategy parameters"]["step down"] = input

        return True
 
    def load_parameters(self, filename):
        r = csv.reader(open(filename, "r"), delimiter = '\t', lineterminator = '\n')
        for row in r:
            if ('\t'.join(row)).split('\t')[0]in self.parameter_dict:
                current_group = ('\t'.join(row)).split('\t')[0]
            else:                
                if ('\t'.join(row)).split('\t')[1] in self.parameter_dict[current_group]:
                    self.parameter_dict[current_group][('\t'.join(row)).split('\t')[1]] = ('\t'.join(row)).split('\t')[2]     

        self.parameter_string = self.parameters_to_string()
   
        self.profile_filename = (filename.split('/')[-1]).split('.')[0]
    
    def save_parameters(self, filename):
        self.profile_filename = filename
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

        self.generate_gCode_filename()
        # adapted from Gcode file generator found at: 
        # https://github.com/YetiTool/GCodeFileGenerators/blob/master/shapes/shape_cut.py

        # internal settings:
        z_height_for_rapid_move = self.z_height_for_rapid_move

        # MODE
        shape = self.shape_dict["shape"]
        aperture_or_island = self.shape_dict["cut_type"]

        if self.shape_dict["units"] == "inches":
            dim_unit_multiplier = 25.4
        elif self.shape_dict["units"] == "mm":
            dim_unit_multiplier = 1
            
        if self.parameter_dict["cutter dimensions"]["units"] == "inches":
            cutter_unit_multiplier = 25.4
        elif self.parameter_dict["cutter dimensions"]["units"] == "mm":
            cutter_unit_multiplier = 1
 
        if self.parameter_dict["tabs"]["units"] == "inches":
            tab_unit_multiplier = 25.4
        elif self.parameter_dict["tabs"]["units"] == "mm":
            tab_unit_multiplier = 1

        if self.parameter_dict["feed rates"]["units"] == "inches":
            rates_unit_multiplier = 25.4
        elif self.parameter_dict["feed rates"]["units"] == "mm":
            rates_unit_multiplier = 1

        if self.parameter_dict["strategy parameters"]["units"] == "inches":
            strategy_unit_multiplier = 25.4
        elif self.parameter_dict["strategy parameters"]["units"] == "mm":
            strategy_unit_multiplier = 1
           
        material_thickness = float(self.shape_dict["dimensions"]["Z"])*dim_unit_multiplier #??
                
        Logger.info(material_thickness)
        
        # RECTANGLE PARAMETERS  
        if shape == "rectangle":
            rect_job_x = float(self.shape_dict["dimensions"]["X"])*dim_unit_multiplier
            rect_job_y = float(self.shape_dict["dimensions"]["Y"])*dim_unit_multiplier
            rect_job_rad = float(self.shape_dict["dimensions"]["R"])*dim_unit_multiplier
        
            Logger.info(rect_job_x)
            Logger.info(rect_job_y)
            Logger.info(rect_job_rad)
        
        
        # CIRCLE PARAMS
        elif shape == "circle":
            circ_input_diameter = float(self.shape_dict["dimensions"]["D"])*dim_unit_multiplier
       
            Logger.info(circ_input_diameter)
       
        # TOOL
        cutter_diameter = float(self.parameter_dict["cutter dimensions"]["diameter"])*cutter_unit_multiplier
        cutter_rad = cutter_diameter/2

        # TAB PARAMS
        tabs = self.parameter_dict["tabs"]["tabs?"]
        
        if tabs == True:
            tab_height = float(self.parameter_dict["tabs"]["height"])*tab_unit_multiplier
            tab_width = float(self.parameter_dict["tabs"]["width"])*tab_unit_multiplier
            tab_distance = float(self.parameter_dict["tabs"]["spacing"])*tab_unit_multiplier
            tab_absolute_height = -(material_thickness - tab_height)
            tab_effective_width = cutter_diameter + tab_width
        
        # FEEDS AND SPEEDS
        xy_feed_rate = float(self.parameter_dict["feed rates"]["xy feed rate"])*rates_unit_multiplier
        plunge_feed_rate = float(self.parameter_dict["feed rates"]["z feed rate"])*rates_unit_multiplier
        spindle_speed = float(self.parameter_dict["feed rates"]["spindle speed"])
        
        # STRATEGY
        stock_bottom_offset = float(self.parameter_dict["strategy parameters"]["stock bottom offset"])*strategy_unit_multiplier
        stepdown = float(self.parameter_dict["strategy parameters"]["step down"])*strategy_unit_multiplier
        finishing_pass = float(self.parameter_dict["strategy parameters"]["finishing passes"])

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
            
            if tabs == True:
                
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
            
                Logger.info("Number of tabs in X axis: " + str(len(x_out_tabs)))
                Logger.info("Number of tabs in Y axis: " + str(len(y_out_tabs)))
        
            else:
                Logger.info("No tabs")
        
        # CIRCLE PARAMS
        
        elif shape == "circle":
            
            if aperture_or_island == "aperture":
                circ_path_rad = (circ_input_diameter - cutter_diameter) / 2
                
            elif aperture_or_island == "island":
                circ_path_rad = (circ_input_diameter + cutter_diameter) / 2
        
            if tabs == True:
                
                # calculate an even distribution of tabs along the circumference, based on desired distance between each (round down the distance between tabs as needed to achieve even distribution)
                # working in rads here
                
                total_circumference = 2.0 * math.pi * circ_path_rad
                circ_tabs_qty = math.ceil(total_circumference / tab_distance) #rounddown
                circ_angle_between_tabs = (2.0 * math.pi) / circ_tabs_qty
                circ_angle_across_tab = (tab_effective_width / total_circumference) * (2.0 * math.pi)
        
        #         print total_circumference, circ_tabs_qty, circ_angle_between_tabs, circ_angle_across_tab, circ_path_rad, math.degrees(circ_angle_across_tab)
        
                circ_tab_start_pos = []
                circ_tab_end_pos = []
                
                circ_tab_start_angle = 0
        
                while circ_tab_start_angle < (round(2 * math.pi,6)):
                    
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
                    
                    circ_tab_next_start_pos = circ_tab_start_pos[1:] + circ_tab_start_pos[:1] # simple way to rotate a list
                
                    
        ################ GCODE GENERATOR ###############
        
        ######## GCODE HEADER
        
        job_name = self.gcode_filename
        
        lines = ['(' + job_name + ')',
                'G90', #Absolute
                'G94', #Feed units per mm
                'G17', #XY plane
                'G21', #In MM
                'M3 S' + str(spindle_speed), # Turn on spindle
                'G4 P1', # Allow time for inrush
                'G91.1' # relative rad centre definitions. IMPORTANT: "G90.1" (absolute rad centre definitions) DOESN'T WORK IN GRBL
                ]
        
        ###### GCODE SHAPE
        
        # Start pos
        
        lines.append("\n(Start of shape)")
        
        if shape == "rectangle":
            lines.append("G0 X" + str(x_flat_min) + " Y" + str(y_min))
        
        elif shape == "circle":
            lines.append("G0 X" + str(circ_path_rad) + " Y" + str(0))
        
        lines.append("G0 Z" + str(z_height_for_rapid_move))
        
        z = -stepdown
        
        while z >= z_max:
            
            if shape == "rectangle":
                
                
                # plunge and draw square, anti-clockwise
                lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                
                # x-out
                if tabs == True and z < tab_absolute_height:
                    for start_tab_coord in x_out_tabs:
                        lines.append("G1 X" + str(start_tab_coord) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G1 X" + str(start_tab_coord + tab_effective_width) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                lines.append("G1 X" + str(x_flat_max) + " Y" + str(y_min) + " F" + str(xy_feed_rate))
                
                # rad 1
                lines.append("G3 X" + str(x_max) + " Y" + str(y_flat_min) + " I" + str(0) +  " J" + str(rect_path_rad))
                
                # y-out
                if tabs == True and z < tab_absolute_height:
                    for start_tab_coord in y_out_tabs:
                        lines.append("G1 Y" + str(start_tab_coord) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G1 Y" + str(start_tab_coord + tab_effective_width) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                lines.append("G1 X" + str(x_max) + " Y" + str(y_flat_max) + " F" + str(xy_feed_rate))
                
                # rad 2
                lines.append("G3 X" + str(x_flat_max) + " Y" + str(y_max) + " I" + str(-rect_path_rad) +  " J" + str(0))
                
                # x-rtn
                if tabs == True and z < tab_absolute_height:
                    for start_tab_coord in x_rtn_tabs:
                        lines.append("G1 X" + str(start_tab_coord) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G1 X" + str(start_tab_coord - tab_effective_width) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                lines.append("G1 X" + str(x_flat_min) + " Y" + str(y_max) + " F" + str(xy_feed_rate))
                
                # rad 3
                lines.append("G3 X" + str(x_min) + " Y" + str(y_flat_max) + " I" + str(0) +  " J" + str(-rect_path_rad))
                
                # y-rtn
                if tabs == True and z < tab_absolute_height:
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
                if tabs == True and z < tab_absolute_height:
                    tab_count = 0
                    for (xy_start, xy_end, xy_next) in zip(circ_tab_start_pos, circ_tab_end_pos, circ_tab_next_start_pos):
                        tab_count += 1
                        lines.append("(Z" + str(z) + ": Tab " + str(tab_count) + ")")
        #                 if xy_start[0] != circ_path_rad: # hack to prevent repetition of co-ordinates from triggering a 360 degree revolution (makes sure that x co-ords aren't the same before appending - only works in this template with start point position etc)
        #                     lines.append("G3 X" + str(xy_start[0]) + " Y" + str(xy_start[1]) + " I" + str(-xy_start[0]) + " J" + str(-xy_start[1]) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(tab_absolute_height) + " F" + str(plunge_feed_rate))
                        lines.append("G3 X" + str(xy_end[0]) + " Y" + str(xy_end[1]) + " I" + str(-xy_start[0]) + "J" + str(-xy_start[1]) + " F" + str(xy_feed_rate))
                        lines.append("G1 Z" + str(z) + " F" + str(plunge_feed_rate))
                        lines.append("G3 X" + str(xy_next[0]) + " Y" + str(xy_next[1]) + " I" + str(-xy_end[0]) + " J" + str(-xy_end[1]) + " F" + str(xy_feed_rate))
                  
                else:
                    lines.append("G3 X" + str(circ_path_rad) + " Y0 I" + str(-circ_path_rad) + " J0 F" + str(xy_feed_rate))
        
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
#        lines.append("%") #Prog end (redundant?) # BREAKER OF THINGS GET IN YOUR GRAVE

        self.set_job_envelope(lines)

        # strip it to prevent weird gcode errors
        preloaded_job_gcode = []

        for line in lines:
            # Strip comments/spaces/new line and capitalize:
            l_block = re.sub('\s|\(.*?\)', '', (line.strip()).upper())
            
            if l_block.find('%') == -1 and l_block.find('M6') == -1 and l_block.find('M06') == -1 and l_block.find('G28') == -1:    # Drop undesirable lines
                preloaded_job_gcode.append(l_block)
                
        self.gcode_lines = preloaded_job_gcode
        
        return True     

    def generate_gCode_filename(self):
        self.gcode_job_name = self.shape_dict["shape"] + "_" + self.shape_dict["cut_type"] + "_" + self.profile_filename + ".nc"
        self.gcode_filename = self.jobCache_file_path + self.gcode_job_name
       
    def save_gCode(self):
        self.generate_gCode_filename()
        f = open(self.gcode_filename, "w")
        for line in self.gcode_lines:
            f.write(line + "\n")
        Logger.info("Done: " + self.gcode_filename)

    def set_job_envelope(self, lines):

        # there's a bug here - needs looking at! 
        if self.shape_dict["units"] == "inches":
            dim_unit_multiplier = 25.4
        elif self.shape_dict["units"] == "mm":
            dim_unit_multiplier = 1
             
        if self.shape_dict["shape"] == "rectangle":
 
            x_values = []
            y_values = []
            z_values = []
    
            for line in lines:
                Logger.info(line)
                blocks = str(line).strip().split(" ")
                Logger.info(blocks)
                for part in blocks:
                    try:
                        if part.startswith(('X')): x_values.append(float(part[1:]))
                        if part.startswith(('Y')): y_values.append(float(part[1:]))
                        if part.startswith(('Z')): z_values.append(float(part[1:]))
                    except:
                        Logger.info("Envelope calculator: skipped '" + part + "'")
            
            Logger.info(x_values)
            Logger.info(y_values)
            Logger.info(z_values)
            
            self.range_x[0], self.range_x[1] = min(x_values), max(x_values)
            self.range_y[0], self.range_y[1] = min(y_values), max(y_values)
            self.range_z[0], self.range_z[1] = min(z_values), max(z_values)
            
        elif self.shape_dict["shape"] == "circle":
            
            self.range_x[0] = -1* float(self.shape_dict["dimensions"]["D"])*dim_unit_multiplier/2
            self.range_x[1] = float(self.shape_dict["dimensions"]["D"])*dim_unit_multiplier/2
            self.range_y[0] = -1* float(self.shape_dict["dimensions"]["D"])*dim_unit_multiplier/2
            self.range_y[1] = float(self.shape_dict["dimensions"]["D"])*dim_unit_multiplier/2
            
            z_values = []
    
            for line in lines:
                blocks = str(line).strip().split(" ")
                for part in blocks:
                    try:
                        if part.startswith(('Z')): z_values.append(float(part[1:]))
                    except:
                        Logger.info("Envelope calculator: skipped '" + part + "'")
            
            self.range_z[0], self.range_z[1] = min(z_values), max(z_values)

    def is_job_within_bounds(self):

        errorfound = 0
        error_message = ''
        
        if self.shape_dict["shape"] == "rectangle":
            range_0_multiplier = -1
        elif self.shape_dict["shape"] == "circle":
            range_0_multiplier = -1
            
        # Mins
        
        if range_0_multiplier*(self.m.x_wco()+float(self.range_x[0])) >= (self.m.grbl_x_max_travel - self.m.limit_switch_safety_distance):
            error_message = error_message + "\n\nThe job target is too close to the X home position."
            errorfound += 1 
        if range_0_multiplier*(self.m.y_wco()+float(self.range_y[0])) >= (self.m.grbl_y_max_travel - self.m.limit_switch_safety_distance):
            error_message = error_message + "\n\nThe job target is too close to the Y home position."
            errorfound += 1 
        if -(self.m.z_wco()+float(self.range_z[0])) >= (self.m.grbl_z_max_travel - self.m.limit_switch_safety_distance):
            error_message = error_message + "\n\nThe job target is too far from the Z home position."
            errorfound += 1 
            
        # Maxs

        if self.m.x_wco()+float(self.range_x[1]) >= -self.m.limit_switch_safety_distance:
            error_message = error_message + "\n\nThe job target is too far from the X home position."
            errorfound += 1 
        if self.m.y_wco()+float(self.range_y[1]) >= -self.m.limit_switch_safety_distance:
            error_message = error_message + "\n\nThe job target is too far from the Y home position."
            errorfound += 1 
        if self.m.z_wco()+float(self.range_z[1]) >= -self.m.limit_switch_safety_distance:
            error_message = error_message + "\n\nThe job target is too close to the Z home position."
            errorfound += 1 

        if errorfound > 0: return error_message
        else: return True  
