'''
Created 5 March 2020
@author: Letty
Module to store parameters and user choices for the Shape Cutter app
'''

import csv
import math
import re

class ShapeCutterJobParameters(object):
    
    parameterCache_file_path = './asmcnc/apps/shapeCutter_app/parameter_cache/'
    jobCache_file_path = './jobCache/'
    profile_filename = ""
    
    # gcode
    gcode_lines = []
    gcode_filename = ''
    
    # Internal settings
    z_height_for_rapid_move = 3
    
    def __init__(self):
 
        # shape dimensions
        self.circle_dimensions = {
            "D": "0",
            "Z": "0"
            }
        
        self.rectangle_dimensions = {
            "X": "0",
            "Y": "0",
            "Z": "0",
            "R": "0"
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
            "tabs?": "",
            "width": "0",
            "height": "0",
            "spacing": "0",
            "units": "mm"
            }
        
        self.cutter_dimensions = {
            "diameter": "0",
            "cutting length": "0",
            "shoulder length": "0",
            "units": "mm"
            }

        self.feed_rates = {
            "xy feed rate": "0",
            "z feed rate": "0",
            "spindle speed": "0",
            "units": "mm"
            }
        
        self.strategy_parameters = {
            "stock bottom offset": "0",
            "step down": "0",
            "finishing passes": "0",
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
    
    def validate_shape_dimensions(self):
        pass
    
    def validate_parameters(self):
        pass
 
    def load_parameters(self):

        r = csv.reader(open(self.parameterCache_file_path + 'default' + '.csv', "r"), delimiter = '\t', lineterminator = '\n')
        for row in r:
            if ('\t'.join(row)).split('\t')[0]in self.parameter_dict:
                current_group = ('\t'.join(row)).split('\t')[0]
            else:                
                if ('\t'.join(row)).split('\t')[1] in self.parameter_dict[current_group]:
                    self.parameter_dict[current_group][('\t'.join(row)).split('\t')[1]] = ('\t'.join(row)).split('\t')[2]     

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

        self.generate_gCode_filename()
        # adapted from Gcode file generator found at: 
        # https://github.com/YetiTool/GCodeFileGenerators/blob/master/shapes/shape_cut.py

        # internal settings:
        z_height_for_rapid_move = self.z_height_for_rapid_move

        # MODE
        shape = self.shape_dict["shape"]
        aperture_or_island = self.shape_dict["cut_type"]

    
        material_thickness = float(self.shape_dict["dimensions"]["Z"]) #??
                
        # RECTANGLE PARAMETERS  
        if shape == "rectangle":
            rect_job_x = float(self.shape_dict["dimensions"]["X"])
            rect_job_y = float(self.shape_dict["dimensions"]["Y"])
            rect_job_rad = float(self.shape_dict["dimensions"]["R"])
        
        # CIRCLE PARAMS
        elif shape == "circle":
            circ_input_diameter = float(self.shape_dict["dimensions"]["D"])
       
        # TOOL
        cutter_diameter = float(self.parameter_dict["cutter dimensions"]["diameter"])
        cutter_rad = cutter_diameter/2

        # TAB PARAMS
        tabs = self.parameter_dict["tabs"]["tabs?"]
        
        if tabs == True:
            tab_height = float(self.parameter_dict["tabs"]["height"])
            tab_width = float(self.parameter_dict["tabs"]["width"])
            tab_distance = float(self.parameter_dict["tabs"]["spacing"])
            tab_absolute_height = -(material_thickness - tab_height)
            tab_effective_width = cutter_diameter + tab_width
        
        # FEEDS AND SPEEDS
        xy_feed_rate = float(self.parameter_dict["feed rates"]["xy feed rate"])
        plunge_feed_rate = float(self.parameter_dict["feed rates"]["z feed rate"])
        spindle_speed = float(self.parameter_dict["feed rates"]["spindle speed"])
        
        # STRATEGY
        stock_bottom_offset = float(self.parameter_dict["strategy parameters"]["stock bottom offset"])
        stepdown = float(self.parameter_dict["strategy parameters"]["step down"])
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
        
            if tabs == True:
                
                # calculate an even distribution of tabs along the circumference, based on desired distance between each (round down the distance between tabs as needed to achieve even distribution)
                # working in rads here
                
                total_circumference = 2.0 * math.pi * circ_path_rad
                circ_tabs_qty = math.floor(total_circumference / tab_distance) #rounddown
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
                    
                    circ_tab_next_start_pos = circ_tab_start_pos[1:] + circ_tab_start_pos[:1] # simple way to rotate a list
                
                    
        ################ GCODE GENERATOR ###############
        
        ######## GCODE HEADER
        
        job_name = self.gcode_filename
        
        lines = ['(' + job_name + ')',
                'G90', #Absolute
                'G94', #Feed units per mm
                'G17', #XY plane
                'G21', #In MM
                'M3 S25000', # Turn on spindle
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
                    for (xy_start, xy_end, xy_next) in zip(circ_tab_start_pos, circ_tab_end_pos, circ_tab_next_start_pos):
                        
                        lines.append("(Tab)")
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

        # strip it and see if that gets rid of errors. 
        
        preloaded_job_gcode = []

        for line in lines:
            # Strip comments/spaces/new line and capitalize:
            l_block = re.sub('\s|\(.*?\)', '', (line.strip()).upper())  
            
            if l_block.find('%') == -1 and l_block.find('M6') == -1 and l_block.find('G28') == -1:    # Drop undesirable lines
                preloaded_job_gcode.append(l_block)
                
        self.gcode_lines = preloaded_job_gcode  

        print self.gcode_lines

    def generate_gCode_filename(self):
        self.gcode_filename = self.jobCache_file_path + self.shape_dict["shape"] \
         + "_" + self.shape_dict["cut_type"] + self.profile_filename + ".nc"
       
    def save_gCode(self):    
        f = open(self.gcode_filename, "w")
        for line in self.gcode_lines:
            f.write(line + "\n")
            print line + "\n"
        print "Done: " + self.gcode_filename

    def set_job_envelope(self):

        # there's a bug here - needs looking at! 
 
        x_values = []
        y_values = []
        z_values = []

        for line in self.gcode_lines:
            blocks = str(line).strip().split(" ")
            for part in blocks:
                try:
                    if part.startswith(('X')): x_values.append(float(part[1:]))
                    if part.startswith(('Y')): y_values.append(float(part[1:]))
                    if part.startswith(('Z')): z_values.append(float(part[1:]))
                except:
                    print "Envelope calculator: skipped '" + part + "'"
        self.range_x[0], self.range_x[1] = min(x_values), max(x_values)
        self.range_y[0], self.range_y[1] = min(y_values), max(y_values)
        self.range_z[0], self.range_z[1] = min(z_values), max(z_values)