'''
Working theory:

read in data
for simple shapes:
    is it clockwise? 
        correct direction
    find shape centre
    apply inside/outside offset
    are there corner rads?
        offset corner radius
        add corner coordinates
calculate pass depths
produce gcode
tidy gcode
write to output file
'''
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from io import open
import os
import re

from asmcnc.apps.drywall_cutter_app.config import config_loader

class GCodeEngine():
    def __init__(self, dwt_config, **kwargs):
        self.m = kwargs['machine']
        self.config = dwt_config

        #Globals 
        self.x = 0  # Identifier for use in arrays
        self.y = 1  # Identifier for use in arrays

        self.custom_gcode_shapes = ["geberit"]

        self.source_folder_name = u"gcode" 
        self.source_folder_path = u"asmcnc/apps/drywall_cutter_app/" + self.source_folder_name 

    #Produce corner coordinates for a rectangle of size x, y
    def rectangle_coordinates(self, x, y, xmin, ymin):
        if x <= 0 or y <= 0:
            return []  # Invalid dimensions, return an empty list

        # Define the coordinates for the four corners
        top_left = (xmin, y)
        top_right = (x, y)
        bottom_right = (x, ymin)
        bottom_left = (xmin, ymin)

        # Return the coordinates in clockwise order
        return [bottom_left, top_left, top_right, bottom_right]

    #Adjust corner radius depending on the offset type (in, on, outside of line)
    def offset_corner_radius(self, corner_radius, offset_type, tool_diameter):
        if offset_type == u"inside":
            return corner_radius - tool_diameter
        elif offset_type == u"outside":
            return corner_radius + tool_diameter
        elif offset_type == None:
            return corner_radius
        else: 
            raise  Exception(u"Unknown offset type. Please specify 'inside', 'outside' or 'none'.")

    #Find the shape centre coordinates
    def find_centre(self, coordinates, x_offset, y_offset):
        x_sum = 0
        y_sum = 0
        for x, y in coordinates:
            x_sum += x + x_offset
            y_sum += y + y_offset
        centre_x = x_sum / len(coordinates)
        centre_y = y_sum / len(coordinates)

        return centre_x, centre_y

    #Check if a corner radius is present (and not tiny)
    def find_corner_rads(self, radius):
        if radius > 0.09:
            return True
        else:
            return False

    #Determine shape point direction
    def is_clockwise(self, coordinates):
        total = 0
        for i in xrange(len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[(i + 1) % len(coordinates)]  # Handle the wraparound at the end
            total += (x2 - x1) * (y2 + y1)
        
        if total > 0:
            return False
        elif total < 0:
            return True

    #Reverse coordinates if need to be clockwise
    def correct_orientation(self, coordinates, clockwise):
        if clockwise:
            return coordinates[::-1]
        else:
            return coordinates

    #Take in corner coordinates and return coordinates for arcs
    def add_corner_coordinates(self, coordinates, shape_centre, corner_radius):
        new_coordinates = []
        for coordinate in coordinates:
            #Bottom left
            if coordinate[self.x] < shape_centre[self.x] and coordinate[self.y] < shape_centre[self.y]: 
                rad_point_1 = coordinate[self.x] + corner_radius, coordinate[self.y]
                rad_point_2 = coordinate[self.x], coordinate[self.y] + corner_radius
            #Top left
            elif coordinate[self.x] < shape_centre[self.x] and coordinate[self.y] > shape_centre[self.y]:
                rad_point_1 = coordinate[self.x], coordinate[self.y] - corner_radius
                rad_point_2 = coordinate[self.x] + corner_radius, coordinate[self.y]
            #Top right
            elif coordinate[self.x] > shape_centre[self.x] and coordinate[self.y] > shape_centre[self.y]:
                rad_point_1 = coordinate[self.x] - corner_radius, coordinate[self.y]
                rad_point_2 = coordinate[self.x], coordinate[self.y] - corner_radius
            #Bottom right
            elif coordinate[self.x] > shape_centre[self.x] and coordinate[self.y] < shape_centre[self.y]:
                rad_point_1 = coordinate[self.x], coordinate[self.y] + corner_radius
                rad_point_2 = coordinate[self.x] - corner_radius, coordinate[self.y]
            new_coordinates.append(rad_point_1)
            new_coordinates.append(rad_point_2)
        return new_coordinates 

    #Calculate the difference in corner radius depending on offset type
    def calculate_corner_radius_offset(self, offset_type, tool_diamter):
        tool_radius = tool_diamter / 2
        if offset_type == u"inside":
            offset_for_rads = -1 * tool_radius
        elif offset_type == u"outside":
            offset_for_rads = tool_radius
        else:
            offset_for_rads = 0
        return offset_for_rads

    #Apply transformation for inside and outside line cutting
    def apply_offset(self, coordinates, offset_type, tool_diameter, shape_centre):
        x_offset = 0
        y_offset = 0
        adjusted_coordinates = []
        if offset_type != None:
            tool_radius = tool_diameter / 2
            for coordinate in coordinates:
                if offset_type == u"inside":
                    if coordinate[self.x] > shape_centre[self.x]:  # RHS
                        x_offset = -1 * tool_radius  # Move to the left
                    else:  # LHS
                        x_offset = tool_radius  # Move to the right
                    if coordinate[self.y] > shape_centre[self.y]:  # Top
                        y_offset = -1 * tool_radius  # Move down
                    else:  # Bottom
                        y_offset = tool_radius  # Move up
                elif offset_type == u"outside":
                    if coordinate[self.x] < shape_centre[self.x]:  # LHS
                        x_offset = -1 * tool_radius  # Move to the left
                    else:  # RHS
                        x_offset = tool_radius  # Move to the right
                    if coordinate[self.y] < shape_centre[self.y]:  # Bottom
                        y_offset = -1 * tool_radius  # Move down
                    else:  # Top
                        y_offset = tool_radius  # Move up
                new_coordinate = coordinate[self.x] + x_offset, coordinate[self.y] + y_offset
                adjusted_coordinates.append(new_coordinate)
        else:
            adjusted_coordinates = coordinates
        return adjusted_coordinates

    #Produce a list of cut depths based on total depth and pass depth
    def calculate_pass_depths(self, total_cut_depth, pass_depth):
        pass_depths = []
        current_depth = pass_depth
        while current_depth < total_cut_depth:
            pass_depths.append(current_depth)
            current_depth += pass_depth
        try:
            if max(pass_depths) < total_cut_depth:
                pass_depths.append(total_cut_depth)
        except:
            pass_depths = [total_cut_depth]
        return pass_depths

    #Determine if the cut direction should be clockwise or not
    def determine_cut_direction_clockwise(self, offset_type, climb):
        if climb and offset_type == u"outside" or not(climb) and offset_type == u"inside":
            return True
        else:
            return False

    #For use when reordering gcode instructions
    def swap_lines_after_keyword(self, input_list, keyword):
        i = 0
        while i < len(input_list):
            if keyword.lower() in input_list[i].lower():
                # Check if there are at least two lines after the keyword
                if i + 2 < len(input_list):
                    # Swap the lines
                    input_list[i + 1], input_list[i + 2] = input_list[i + 2], input_list[i + 1]
                i += 3  # Move to the next keyword (assuming each occurrence is separated by 2 lines)
            else:
                i += 1
        return input_list

    #For use when reordering gcode instructions
    def replace_after_keyword(self, input_list, keyword, replacement):
        for i in xrange(len(input_list) - 1):
            if keyword.lower() in input_list[i].lower():
                if i + 1 < len(input_list):
                    # Replace the first two letters of the line that follows the keyword
                    input_list[i + 1] = replacement + input_list[i + 1][2:]
        return input_list

    #Produce gcode instructions to cut a rounded (or not) rectangle
    def cut_rectangle(self, coordinates, datum_x, datum_y, offset, tool_diameter, is_climb, corner_radius, pass_depth, feedrate, plungerate, total_cut_depth, z_safe_distance, roughing_pass, simulate):
        # Ensure coordinates are all in clockwise order
        coordinates = self.correct_orientation(coordinates, self.is_clockwise(coordinates))  

        # Find shape centre for further calcs
        shape_centre = self.find_centre(coordinates[:-1], 0, 0)  

        # Apply offset for toolpath (inside, on, outside the line cutting)
        offset_coordinates = self.apply_offset(coordinates, offset, tool_diameter, shape_centre)  

        clockwise_cutting = self.determine_cut_direction_clockwise(offset, is_climb)  

        # Add corner coordinates if necessary
        radii_present = self.find_corner_rads(corner_radius)  
        final_coordinates = offset_coordinates
        if radii_present:
            adjusted_corner_radius = corner_radius + self.calculate_corner_radius_offset(offset, tool_diameter)  
            if adjusted_corner_radius > 0:
                final_coordinates = self.add_corner_coordinates(offset_coordinates, shape_centre, adjusted_corner_radius)  
            else:
                radii_present = False

        pass_depths = self.calculate_pass_depths(total_cut_depth, pass_depth)  

        # Time to make some gcode :)
        if clockwise_cutting:
            arc_instruction = "G2"
        else:
            final_coordinates = self.correct_orientation(final_coordinates, True)
            arc_instruction = "G3"

        cutting_lines = []

        for depth in pass_depths:
            if not simulate:
                gcode_instruction = "(Offset: %s)\n(Roughing pass)\n" % offset if roughing_pass else "(Offset: %s)\n(Finishing pass)\n" % offset
                cutting_lines.append(gcode_instruction)
                cutting_lines.append("G1 Z-%s F%s\n" % (depth, plungerate))
            else:
                gcode_instruction = "(Simulation pass)\n"
                cutting_lines.append(gcode_instruction)
                cutting_lines.append("G1 Z%s F%s\n" % (depth, plungerate))
            # Cut the shape
            if not radii_present:
                # Logic for straight lines only
                for coordinate in final_coordinates:
                    second_line = 1 == final_coordinates.index(coordinate)
                    gcode_instruction = "G1 X%s Y%s %s\n" % (coordinate[0] + datum_x, coordinate[1] + datum_y, 'F%s' % feedrate if second_line else '')
                    cutting_lines.append(gcode_instruction)
            else:
                # Logic for when corner rads are present
                arc_flag = True
                for coordinate in final_coordinates[:-1]:
                    second_line = 1 == final_coordinates.index(coordinate)              
                    gcode_instruction = "G1 X%s Y%s %s\n" % (coordinate[0] + datum_x, coordinate[1] + datum_y, 'F%s' % feedrate if second_line else '')
                    if arc_flag:                        
                        gcode_instruction = "G1 X%s Y%s %s\n" % (coordinate[0] + datum_x, coordinate[1] + datum_y, 'F%s' % feedrate if second_line else '')
                    else:
                        gcode_instruction = "%s X%s Y%s R%s %s\n" % (arc_instruction, coordinate[0] + datum_x, coordinate[1] + datum_y, adjusted_corner_radius, 'F%s' % feedrate if second_line else '')
                    arc_flag = not arc_flag
                    cutting_lines.append(gcode_instruction)
            cutting_lines.append("G1 Z%d F%d\n\n" % (z_safe_distance, plungerate))

        # Correct gcode order
        cutting_lines = self.swap_lines_after_keyword(cutting_lines, u"pass")
        # Speed up first XY move
        cutting_lines = self.replace_after_keyword(cutting_lines, u"pass", "G0")

        return cutting_lines
    
    #Produce gcode instructions to cut a straight line
    def cut_line(self, datum_x, datum_y, length, tool_diameter, orientation, pass_depth, feedrate, plungerate, total_cut_depth, z_safe_distance, simulate):
        pass_depths = self.calculate_pass_depths(total_cut_depth, pass_depth)
        tool_radius = tool_diameter / 2
        x = 0
        y = 1 
        direction_flag = True

        gcode_lines = ["G0 Z{}\n".format(z_safe_distance)]

        if orientation == "vertical":
            start_coordinate = [datum_x + tool_radius, datum_y]
            end_coordinate = [datum_x + length - tool_radius, datum_y]
        else: #horizontal
            start_coordinate = [datum_x, datum_y + tool_radius]
            end_coordinate = [datum_x, datum_y + length - tool_radius]
        gcode_lines.append("G0 X{} Y{}\n".format(start_coordinate[x], start_coordinate[y]))
        for depth in pass_depths:
            if simulate:
                    gcode_lines.append("G1 Z{} F{}\n".format(depth, plungerate))
            else:                    
                    gcode_lines.append("G1 Z-{} F{}\n".format(depth, plungerate))
            if direction_flag:                
                gcode_lines.append("G1 X{} Y{} F{}\n".format(end_coordinate[x], end_coordinate[y], feedrate))
            else:
                gcode_lines.append("G1 X{} Y{} F{}\n".format(start_coordinate[x], start_coordinate[y], feedrate))
            direction_flag = not(direction_flag)

        gcode_lines.append("G1 Z{} F{}\n".format(z_safe_distance, plungerate))

        return gcode_lines

    #Return lines in appropriate gcode file
    def find_and_read_gcode_file(self, directory, shape_type, tool_diameter):
        for file in os.listdir(directory):
            filename = file.lower().strip()
            if shape_type in filename and str(tool_diameter)[:-2] + "mm" in filename:
                file_path = os.path.join(directory, filename)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as file:
                            return file.readlines()
                    except IOError:
                        print("An error occurred while reading the Gcode file")
                else:
                    raise IOError("Gcode file not found")

    #Scrape through gcode and replace feedrate, plungerate and spindle speed
    def adjust_feeds_and_speeds(self, gcode_lines, feedrate, plungerate, spindle_speed):
        adjusted_lines = []
        feedrate_pattern = re.compile(r'G1.*?[XY].*?F([\d.]+)', re.IGNORECASE)
        plungerate_pattern = re.compile(r'G1.*?Z(-?\d+\.\d+).*?F([\d.]+)', re.IGNORECASE)
        spindle_speed_pattern = re.compile(r'S\d+', re.IGNORECASE)

        for line in gcode_lines:
            if 'F' in line and feedrate_pattern.search(line):
                # Replace the feedrate if 'G1', 'X' or 'Y' move is present
                match = feedrate_pattern.search(line)
                line = line.replace(match.group(1), str(feedrate))

            if 'G1' in line and 'Z' in line and 'F' in line and plungerate_pattern.search(line):
                # Replace the plungerate
                match = plungerate_pattern.search(line)
                line = line.replace(match.group(2), str(plungerate))

            # Replace the spindle speed
            line = spindle_speed_pattern.sub('S' + str(spindle_speed), line)

            adjusted_lines.append(line)

        return adjusted_lines

    #Extract Z data from gcode header (manually inserted)
    def extract_cut_depth_and_z_safe_distance(self, gcode_lines):
        cut_depth_pattern = r"Cut depth: (-?\d+\.\d+)"
        z_safe_distance_pattern = r"Z safe distance: (\d+\.\d+)"

        cut_depth_value = None
        z_safe_distance_value = None

        for string in gcode_lines:
            if cut_depth_value is None:
                cut_depth_match = re.search(cut_depth_pattern, string, re.IGNORECASE)
                if cut_depth_match:
                    cut_depth_value = cut_depth_match.group(1)  # Store the matched value as a string

            if z_safe_distance_value is None:
                z_safe_distance_match = re.search(z_safe_distance_pattern, string, re.IGNORECASE)
                if z_safe_distance_match:
                    z_safe_distance_value = z_safe_distance_match.group(1)  # Store the matched value as a string

            if cut_depth_value and z_safe_distance_value:
                break  # Exit the loop once both values have been found

        return cut_depth_value, z_safe_distance_value

    #Replace gcode z data with user-driven z data
    def replace_cut_depth_and_z_safe_distance(self, gcode_lines, gcode_cut_depth, gcode_z_safe_distance, new_cut_depth, new_z_safe_distance):
        output = []    
        for line in gcode_lines:
            original_line = line
            line = line.replace(str(gcode_cut_depth), str(new_cut_depth))
            line = line.replace(str(gcode_z_safe_distance), str(new_z_safe_distance))
            output.append(line)

        return output

    #Add datum to each x and y move command
    def apply_datum_offset(self, gcode_lines, x_adjustment, y_adjustment):
        adjusted_lines = []
        for line in gcode_lines:
            if line.startswith("G1Z"):
                adjusted_lines.append(line)
                continue

            parts = re.findall(r'[A-Z][0-9.-]+', line)
            adjusted_parts = []
            for part in parts:
                if part.startswith('X'):
                    x_value = float(part[1:])
                    adjusted_x = x_value + x_adjustment
                    adjusted_parts.append('X{:.3f}'.format(adjusted_x))
                elif part.startswith('Y'):
                    y_value = float(part[1:])
                    adjusted_y = y_value + y_adjustment
                    adjusted_parts.append('Y{:.3f}'.format(adjusted_y))
                else:
                    adjusted_parts.append(part)
            adjusted_lines.append(' '.join(adjusted_parts) + "\n")
        return adjusted_lines

    # Repeat gcode for each pass 
    def repeat_for_depths(self, gcode_lines, pass_depths, start_line_key, end_line_key):
        output = []

        for depth in pass_depths:
            cut_lines = []
            for line in gcode_lines[start_line_key:end_line_key]:
                # Replace "cut depth" with the depth value in the line
                cut_line = line.replace("[cut depth]", "-" + str(depth))
                cut_lines.append(cut_line)
            output.append(''.join(cut_lines))

        output.append('\n'.join(gcode_lines[end_line_key:]))

        return '\n'.join(output)

    #Add partoff cut for geberit shape
    def add_partoff(self, gcode_lines, insertion_key, start_coordinate, end_coordinate, pass_depths, feedrate, plungerate, z_safe_distance):
        x = 0
        y = 1
        insert_index = None
        partoff_gcode = ["(Partoff)"]
        direction_flag = True

        #Find index to insert partoff line
        for i in range(len(gcode_lines)):
            if insertion_key.lower() == gcode_lines[i].lower() + gcode_lines[i+1].lower():
                insert_index = i
                break
            if i == len(gcode_lines):
                break
        if insert_index is None:
            raise Exception ("Unable to find " + insertion_key + " in gcode")
        
        #Generate partoff line gcode
        partoff_gcode.append("G1 Z" + str(z_safe_distance)) #Lift to Z safe distance
        partoff_gcode.append("G0 X" + str(start_coordinate[x]) + " Y" + str(start_coordinate[y]) + "F" + str(feedrate)) #Go to start position
        for depth in pass_depths:          
            if direction_flag: #x min -> x max pass   
                partoff_gcode.append("G1 Z-" + str(depth) + " F" + str(plungerate)) #Plunge to depth
                partoff_gcode.append("G1 X" + str(end_coordinate[x]) + " Y" + str(end_coordinate[y])+ "F" + str(feedrate)) #Go to end position
            else: #x max -> x min pass
                partoff_gcode.append("G1 Z-" + str(depth) + " F" + str(plungerate)) #Plunge to depth
                partoff_gcode.append("G1 X" + str(start_coordinate[x]) + " Y" + str(start_coordinate[y])+ "F" + str(feedrate)) #Go to start position
            direction_flag = not(direction_flag)
        partoff_gcode.append("G1 Z" + str(z_safe_distance)) #Lift to Z safe distance

        output = ""
        for line in partoff_gcode:
            output += line + "\n"
        partoff_gcode = "".join(output)

        #Insert partoff gcode
        gcode_part_1 = gcode_lines[:insert_index]
        gcode_part_2 = gcode_lines[insert_index:]

        return gcode_part_1 +partoff_gcode + gcode_part_2      

    #Extract dimention data from gcode header (manually inserted)
    def read_in_custom_shape_dimentions(self, gcode_lines):
        x_dim_pattern = r"Final part x dim: (-?\d+\.\d+)"
        y_dim_pattern = r"Final part y dim: (\d+\.\d+)"
        x_min_pattern = r"x min: (-?\d+\.\d+)"
        y_min_pattern = r"y min: (-?\d+\.\d+)"

        x_dim = None
        y_dim = None
        x_min = None
        y_min = None

        for string in gcode_lines:
            if x_dim is None:
                x_dim_match = re.search(x_dim_pattern, string, re.IGNORECASE)
                if x_dim_match:
                    x_dim = x_dim_match.group(1)  # Store the matched value as a string

            if y_dim is None:
                y_dim_match = re.search(y_dim_pattern, string, re.IGNORECASE)
                if y_dim_match:
                    y_dim = y_dim_match.group(1)  # Store the matched value as a string

            if x_min is None:
                x_min_match = re.search(x_min_pattern, string, re.IGNORECASE)
                if x_min_match:
                    x_min = x_min_match.group(1)  # Store the matched value as a string

            if y_min is None:
                y_min_match = re.search(y_min_pattern, string, re.IGNORECASE)
                if y_min_match:
                    y_min = y_min_match.group(1)  # Store the matched value as a string

            if x_dim and y_dim and x_min and y_min:
                break  # Exit the loop once both values have been found

        missing_values = [dim for dim, value in zip(['x_dim', 'y_dim', 'x_min', 'y_min'], [x_dim, y_dim, x_min, y_min]) if value is None]
        if missing_values:
            raise Exception("Unable to gather shape dimension data. Missing values: {}".format(', '.join(missing_values)))

        return x_dim, y_dim, x_min, y_min

    #For use in UI not engine
    def get_custom_shape_extents(self):
        if self.config.active_config.shape_type.lower() in self.custom_gcode_shapes:
            # Read in data
            gcode_lines = self.find_and_read_gcode_file(self.source_folder_path, self.config.active_config.shape_type, self.config.active_cutter.diameter)
            
            # Get dimensions as strings
            x_dim_str, y_dim_str, x_min_str, y_min_str = self.read_in_custom_shape_dimensions(gcode_lines)
            
            # Convert strings to floats
            x_dim = float(x_dim_str)
            y_dim = float(y_dim_str)
            x_min = float(x_min_str)
            y_min = float(y_min_str)

            return x_dim, y_dim, x_min, y_min
        else:
            raise Exception ("Shape type: {} is not defined as a custom shape.".format(self.config.active_config.shape_type))

    #Main
    def engine_run(self, simulate=True):
        output_file = "jobCache/" + self.config.active_config.shape_type + u".nc"
        safe_start_position = u"X0 Y0 Z10"
        z_safe_distance = 5
        cutting_lines = []
        pass_depths = []
        stepovers = [0]
        simulation_z_height = 5 #mm
        simualtion_plunge_rate = 750 #mm/s
        simulation_feedrate = 2000 #mm/s

        if self.config.active_cutter.cutting_direction.lower() == "climb":
            is_climb = True
        else:
            is_climb = False

        # Calculated parameters
        total_cut_depth = self.config.active_config.cutting_depths.material_thickness - self.config.active_config.cutting_depths.bottom_offset

        if self.config.active_config.shape_type.lower() == u"rectangle" or self.config.active_config.shape_type.lower() == u"square":
            rect_coordinates = self.rectangle_coordinates(self.config.active_config.canvas_shape_dims.x, self.config.active_config.canvas_shape_dims.y, 0, 0)
            if len(rect_coordinates) != 4:
                raise Exception(u"Sir, rectangles have 4 sides, not %d" % len(rect_coordinates))

            # Add first point to end of coordinate list to complete the contour
            coordinates = rect_coordinates
            coordinates.append(coordinates[0])

            # Create a list of stepovers to add finishing passes
            finish_passes = 0
            finish_stepover = 0.5
            finish_stepdown = self.config.active_config.cutting_depths.material_thickness
            if finish_passes > 0:
                stepovers = [finish_stepover * (finish_passes - i) for i in range(finish_passes)]
                stepovers.append(0)

            if simulate:              
                rectangle = self.cut_rectangle(coordinates,
                                               self.config.active_config.datum_position.x,
                                                self.config.active_config.datum_position.y,
                                                self.config.active_config.toolpath_offset,
                                                self.config.active_cutter.diameter,
                                                is_climb,
                                                self.config.active_config.canvas_shape_dims.r,
                                                simulation_z_height,
                                                simulation_feedrate,
                                                simualtion_plunge_rate,
                                                simulation_z_height,
                                                z_safe_distance,
                                                True,
                                                True)
            else:
                roughing_pass = True
                for stepover in stepovers:
                    effective_tool_diameter = self.config.active_cutter.diameter + (stepover * 2)
                    pass_depth = finish_stepdown if stepover != max(stepovers) else self.config.active_config.cutting_depths.depth_per_pass
                    rectangle = self.cut_rectangle(coordinates,
                                            self.config.active_config.datum_position.x,
                                            self.config.active_config.datum_position.y,
                                            self.config.active_config.toolpath_offset,
                                            effective_tool_diameter,
                                            is_climb,
                                            self.config.active_config.canvas_shape_dims.r,
                                            pass_depth,
                                            self.config.active_cutter.cutting_feedrate,
                                            self.config.active_cutter.plunge_rate,
                                            total_cut_depth,
                                            z_safe_distance,
                                            roughing_pass,
                                            False)
                    roughing_pass = False

            cutting_lines += rectangle

        elif self.config.active_config.shape_type.lower() == u"geberit":
            # Read in data
            gcode_lines = self.find_and_read_gcode_file(self.source_folder_path, self.config.active_config.shape_type, self.config.active_cutter.diameter)
            gcode_cut_depth, gcode_z_safe_distance = self.extract_cut_depth_and_z_safe_distance(gcode_lines)
            x_size, y_size, x_minus, y_minus  = self.read_in_custom_shape_dimentions(gcode_lines)

            if simulate:
                coordinates = self.rectangle_coordinates(float(x_size), float(y_size), float(x_minus), float(y_minus))
                coordinates.append(coordinates[0])
                gcode_lines = self.cut_rectangle(coordinates,
                                               self.config.active_config.datum_position.x,
                                                self.config.active_config.datum_position.y,
                                                "on",
                                                0,
                                                is_climb,
                                                0,
                                                simulation_z_height,
                                                simulation_feedrate,
                                                simualtion_plunge_rate,
                                                simulation_z_height,
                                                z_safe_distance,
                                                True,
                                                True)

            else:
                # Remove header info
                gcode_lines = gcode_lines[next((i for i, s in enumerate(gcode_lines) if re.search(r"T[1-9]", s)), None):]

                # Adjust feeds, speeds, and Z values
                gcode_lines = self.adjust_feeds_and_speeds(gcode_lines, self.config.active_cutter.cutting_feedrate, self.config.active_cutter.plunge_rate, self.config.active_cutter.cutting_spindle_speed)
                gcode_lines = self.replace_cut_depth_and_z_safe_distance(gcode_lines, gcode_cut_depth, gcode_z_safe_distance, "[cut depth] ", z_safe_distance)

                # Apply datum offset
                gcode_lines = self.apply_datum_offset(gcode_lines, self.config.active_config.datum_position.x, self.config.active_config.datum_position.y)

                # Apply pass depths
                pass_depths = self.calculate_pass_depths(total_cut_depth, self.config.active_config.cutting_depths.depth_per_pass)
                start_condition = next((i for i, s in enumerate(gcode_lines) if re.search(r"T[1-9]", s)), None)
                end_condition = next((i for i, s in enumerate(gcode_lines) if re.search(r"M5", s)), None)
                gcode_lines = self.repeat_for_depths(gcode_lines, pass_depths, start_condition, end_condition)

                tool_radius = self.config.active_cutter.diameter / 2
                
                partoff_start_coordinate = [(-1 * tool_radius) + self.config.active_config.datum_position.x,
                                            float(y_size) + tool_radius + self.config.active_config.datum_position.y]
                partoff_end_coordinate = [tool_radius + float(x_size) + self.config.active_config.datum_position.x,
                                        tool_radius + float(y_size) + self.config.active_config.datum_position.y]
                gcode_lines = self.add_partoff(gcode_lines, "M5", partoff_start_coordinate, partoff_end_coordinate, pass_depths, self.config.active_cutter.cutting_feedrate, self.config.active_cutter.plunge_rate, z_safe_distance)
                
            cutting_lines = gcode_lines

        elif self.config.active_config.shape_type.lower() == u"circle":
            circle_coordinates = self.rectangle_coordinates(self.config.active_config.canvas_shape_dims.d, self.config.active_config.canvas_shape_dims.d, 0, 0) #Circles are secretly rounded rectangles            

            # Add first point to end of coordinate list to complete the contour
            coordinates = circle_coordinates
            coordinates.append(coordinates[0])

            # Create a list of stepovers to add finishing passes
            finish_passes = 0
            finish_stepover = 0.5
            finish_stepdown = self.config.active_config.cutting_depths.material_thickness
            if finish_passes > 0:
                stepovers = [finish_stepover * (finish_passes - i) for i in range(finish_passes)]
                stepovers.append(0)

            if simulate:
                circle = self.cut_rectangle(coordinates,
                                               self.config.active_config.datum_position.x,
                                                self.config.active_config.datum_position.y,
                                                self.config.active_config.toolpath_offset,
                                                self.config.active_cutter.diameter,
                                                is_climb,
                                                self.config.active_config.canvas_shape_dims.d/2,
                                                simulation_z_height,
                                                simulation_feedrate,
                                                simualtion_plunge_rate,
                                                simulation_z_height,
                                                z_safe_distance,
                                                True,
                                                True)
            else:
                roughing_pass = True
                for stepover in stepovers:
                    effective_tool_diameter = self.config.active_cutter.diameter + (stepover * 2)
                    pass_depth = finish_stepdown if stepover != max(stepovers) else self.config.active_config.cutting_depths.depth_per_pass
                    circle = self.cut_rectangle(coordinates,
                                            self.config.active_config.datum_position.x,
                                            self.config.active_config.datum_position.y,
                                            self.config.active_config.toolpath_offset,
                                            effective_tool_diameter,
                                            is_climb,
                                            self.config.active_config.canvas_shape_dims.d/2,
                                            pass_depth,
                                            self.config.active_cutter.cutting_feedrate,
                                            self.config.active_cutter.plunge_rate,
                                            total_cut_depth,
                                            z_safe_distance,
                                            roughing_pass,
                                            False)

                    roughing_pass = False
            cutting_lines += circle 

        elif self.config.active_config.shape_type.lower() == u"line":
            if simulate:
                cutting_lines = self.cut_line(self.config.active_config.datum_position.x,
                                            self.config.active_config.datum_position.y,
                                            self.config.active_config.canvas_shape_dims.l,
                                            self.config.active_cutter.diameter,
                                            "vertical",
                                            simulation_z_height,
                                            simulation_feedrate,
                                            simualtion_plunge_rate,
                                            simulation_z_height,
                                            z_safe_distance,
                                            simulate
                                            )
            else:
                cutting_lines = self.cut_line(self.config.active_config.datum_position.x,
                                            self.config.active_config.datum_position.y,
                                            self.config.active_config.canvas_shape_dims.l,
                                            self.config.active_cutter.diameter,
                                            "vertical",
                                            self.config.active_config.cutting_depths.depth_per_pass,
                                            self.config.active_cutter.cutting_feedrate,
                                            self.config.active_cutter.plunge_rate,
                                            total_cut_depth,
                                            z_safe_distance,
                                            simulate
                                            )

        else:
            raise Exception("Shape type: '%s' not supported" % self.config.active_config.shape_type)
        
        if simulate:
            cutting_lines = cutting_lines.insert(0, "G90")
            self.m.s.run_skeleton_buffer_stuffer(cutting_lines)
        else:
            file_structure_1_shapes = ["rectangle", "square", "circle", "line"]
           
            if self.config.active_config.shape_type in file_structure_1_shapes:
                output = "(%s)\nG90\nM3 S%d\nG0 %s\n\n%s\n(End)\nG0 Z%d\nM5\n" % (
                    output_file[output_file.find("/")+1:], self.config.active_cutter.cutting_spindle_speed, safe_start_position, ''.join(cutting_lines), z_safe_distance)
            else:
                output = ''.join(cutting_lines)

            with open(output_file, 'w+') as out_file:
                out_file.write(output.decode('utf-8'))
                print("%s written" % output_file)