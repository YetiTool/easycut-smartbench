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
import decimal
import os
import re

try:
    from asmcnc.apps.drywall_cutter_app.config import config_loader
except ImportError:
    print("unable to import config_loader")

class GCodeEngine():
    def __init__(self, dwt_config):
        self.config = dwt_config

        #Globals 
        self.x = 0  # Identifier for use in arrays
        self.y = 1  # Identifier for use in arrays

    #Produce corner coordinates for a rectangle of size x, y
    def rectangle_coordinates(self, x, y):
        if x <= 0 or y <= 0:
            return None  # Invalid dimensions, return None

        # Define the coordinates for the four corners
        top_left = (0, y)
        top_right = (x, y)
        bottom_left = (0, 0)
        bottom_right = (x, 0)

        # Return the coordinates in clockwise order
        return [bottom_left, top_left, top_right, bottom_right]

    #Find the shape centre coordinates
    def find_centre(self, coordinates, x_offset = 0, y_offset = 0):
        x_sum = 0
        y_sum = 0
        # Remove duplicates from the list
        coordinates = list(set(coordinates))
        for x, y in coordinates:
            x_sum += x + x_offset
            y_sum += y + y_offset
        centre_x = x_sum / len(coordinates)
        centre_y = y_sum / len(coordinates)

        return centre_x, centre_y

    #Check if a corner radius is present (and not tiny)
    def find_corner_rads(self, radius):
        return radius > 0.09

    # Determine shape point direction
    def is_clockwise(self, coordinates):
        total = 0
        for i in xrange(len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[(i + 1) % len(coordinates)]  # Handle the wraparound at the end
            total += (x2 - x1) * (y2 + y1)
        
        return total < 0

    # Reverse coordinates if need to be clockwise
    def correct_orientation(self, coordinates, clockwise):
        if not clockwise:
            return coordinates[::-1]
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
        if total_cut_depth <= 0 or pass_depth <= 0:
            raise ValueError("Total cut depth and pass depth must be positive values.")
        
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
        return climb and offset_type == u"outside" or not(climb) and offset_type == u"inside"

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
    def replace_mode_after_keyword(self, input_list, keyword, replacement_mode):
        for i in xrange(len(input_list) - 1):
            if keyword.lower() in input_list[i].lower():
                if i + 1 < len(input_list):
                    # Replace the first two letters of the line that follows the keyword
                    input_list[i + 1] = replacement_mode + input_list[i + 1][2:]
        return input_list

    #Produce gcode instructions to cut a rounded (or not) rectangle
    def cut_rectangle(self, coordinates, datum_x, datum_y, offset, tool_diameter, is_climb, corner_radius, pass_depth, feedrate, plungerate, total_cut_depth, z_safe_distance, roughing_pass):
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
        final_coordinates = self.correct_orientation(final_coordinates, clockwise_cutting)
        
        if clockwise_cutting:
            arc_instruction = u"G2"
        else:
            arc_instruction = u"G3"

        cutting_lines = []

        for depth in pass_depths:
            gcode_instruction = "(Offset: %s)\n(Roughing pass)\n" % offset if roughing_pass else "(Offset: %s)\n(Finishing pass)\n" % offset
            cutting_lines.append(gcode_instruction)
            cutting_lines.append("G1 Z-%s F%s\n" % (depth, plungerate))
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
                        gcode_instruction = "G1 X%s Y%s\n" % (coordinate[0] + datum_x, coordinate[1] + datum_y)
                    else:
                        gcode_instruction = "%s X%s Y%s R%s\n" % (arc_instruction, coordinate[0] + datum_x, coordinate[1] + datum_y, adjusted_corner_radius)
                    arc_flag = not arc_flag
                    cutting_lines.append(gcode_instruction)
            cutting_lines.append("G1 Z%d F%d\n\n" % (z_safe_distance, plungerate))

        # Correct gcode order
        cutting_lines = self.swap_lines_after_keyword(cutting_lines, u"Roughing pass")
        # Speed up first XY move
        cutting_lines = self.replace_mode_after_keyword(cutting_lines, u"Roughing pass", u"G0")

        return cutting_lines

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

    # Scrape through gcode and replace feedrate, plungerate and spindle speed
    def adjust_feeds_and_speeds(self, gcode_lines, feedrate, plungerate, spindle_speed):
        adjusted_lines = []
        feedrate_pattern = re.compile(r'G1.*?[XY].*?F([\d.]+)', re.IGNORECASE)
        plungerate_pattern = re.compile(r'G1.*?[Z].*?F([\d.]+)', re.IGNORECASE)
        spindle_speed_pattern = re.compile(r'S\d.+', re.IGNORECASE)

        for line in gcode_lines:
            line = line.upper()
            if 'F' in line and feedrate_pattern.search(line) and ('Z' not in line):
                # Replace the feedrate if 'G1', 'X' or 'Y' move is present
                match = feedrate_pattern.search(line)
                line = line.replace(match.group(1), str(feedrate))

            elif 'Z' in line and plungerate_pattern.search(line) and ('X' not in line and 'Y' not in line):
                # Replace the plungerate if 'G1' and 'Z' move is present
                match = plungerate_pattern.search(line)
                line = line.replace(match.group(1), str(plungerate))

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

    # Replace gcode z data with user-driven z data
    def replace_cut_depth_and_z_safe_distance(self, gcode_lines, gcode_cut_depth, gcode_z_safe_distance, new_cut_depth, new_z_safe_distance):
        output = []    

        for line in gcode_lines:
            if "z" + str(gcode_cut_depth) in line.strip().lower():
                # Replace Z cut depth
                line = re.sub(r'Z[-+]?\d*\.?\d+', 'Z{}'.format(new_cut_depth), line)
            elif "z" + str(gcode_z_safe_distance) in line.strip().lower(): # Only 1 Z value will be present per line, hence using elif
                # Replace Z safe distance
                line = re.sub(r'Z[-+]?\d*\.?\d+', 'Z{}'.format(new_z_safe_distance), line)

            output.append(line)

        return output

    #Add datum to each x and y move command
    def apply_datum_offset(self, gcode_lines, x_adjustment, y_adjustment):
        adjusted_lines = []
        for line in gcode_lines:
            if line.startswith("G1Z") or line.startswith("G1 Z"):
                adjusted_lines.append(line)
                continue

            parts = re.findall(r'[A-Z][0-9.-]+', line)
            adjusted_parts = []
            for part in parts:
                if part.startswith('X'):
                    x_value = float(part[1:])
                    adjusted_x = x_value + x_adjustment
                    adjusted_parts.append('X{}'.format(self.format_float(adjusted_x)))
                elif part.startswith('Y'):
                    y_value = float(part[1:])
                    adjusted_y = y_value + y_adjustment
                    adjusted_parts.append('Y{}'.format(self.format_float(adjusted_y)))
                else:
                    adjusted_parts.append(part)
            adjusted_lines.append(' '.join(adjusted_parts))
        return adjusted_lines

    # For use with apply_datum_offset
    def format_float(value):
        if value == int(value):
            return str(int(value))
        else:
            # return float without extra zeros
            return str(decimal.Decimal(str(value)).normalize())

    # Repeat gcode for each pass 
    def repeat_for_depths(self, gcode_lines, pass_depths, start_line_key, end_line_key):
        output = []

        for depth in pass_depths:
            cut_lines = []
            for line in gcode_lines[start_line_key:end_line_key]:
                # Replace "cut depth" with the depth value in the line
                cut_line = line.replace("[cut depth]", "-" + str(depth))
                cut_lines.append(cut_line)
            output.append(cut_lines)

        output.append(gcode_lines[end_line_key:])

        return output

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

    def read_in_custom_shape_dimentions(self, gcode_lines):
        x_dim_pattern = r"Final part x dim: (-?\d+\.\d+)"
        y_dim_pattern = r"Final part y dim: (\d+\.\d+)"

        x_dim = None
        y_dim = None

        for string in gcode_lines[:20]: #Data should be found within the first 20 lines
            if x_dim is None:
                x_dim_match = re.search(x_dim_pattern, string, re.IGNORECASE)
                if x_dim_match:
                    x_dim = x_dim_match.group(1)  # Store the matched value as a string

            if y_dim is None:
                y_dim_match = re.search(y_dim_pattern, string, re.IGNORECASE)
                if y_dim_match:
                    y_dim = y_dim_match.group(1)  # Store the matched value as a string

            if x_dim and y_dim:
                break  # Exit the loop once both values have been found

        return x_dim, y_dim

    #Main
    def engine_run(self):
        output_file = "jobCache/" + self.config.active_config.shape_type + u".nc"
        safe_start_position = u"X0 Y0 Z10"
        z_safe_distance = 5
        cutting_lines = []
        pass_depths = []
        stepovers = [0]

        is_climb = self.config.active_cutter.cutting_direction.lower() == "climb"

        # Calculated parameters
        total_cut_depth = self.config.active_config.cutting_depths.material_thickness - self.config.active_config.cutting_depths.bottom_offset

        if self.config.active_config.shape_type.lower() == u"rectangle" or self.config.active_config.shape_type.lower() == u"square":
            rect_coordinates = self.rectangle_coordinates(self.config.active_config.canvas_shape_dims.x, self.config.active_config.canvas_shape_dims.y)
            if len(rect_coordinates) != 4:
                raise Exception(u"Sir, rectangles have 4 sides, not %d" % len(rect_coordinates))

            # Add first point to end of coordinate list to complete the contour
            coordinates = rect_coordinates
            coordinates.append(coordinates[0])

            # Create a list of stepovers to add finishing passes
            finish_passes = 1
            finish_stepover = 0.5
            finish_stepdown = self.config.active_config.cutting_depths.material_thickness
            if finish_passes > 0:
                stepovers = [finish_stepover * (finish_passes - i) for i in range(finish_passes)]
                stepovers.append(0)

            # Produce instructions for each complete rectangle
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
                                        roughing_pass)

                roughing_pass = False
                cutting_lines += rectangle

        elif self.config.active_config.shape_type.lower() == u"geberit":
            source_folder_name = u"gcode" 
            source_folder_path = u"asmcnc/apps/drywall_cutter_app/" + source_folder_name #os.path.join(source_folder_name) 

            # Read in data
            gcode_lines = self.find_and_read_gcode_file(source_folder_path, self.config.active_config.shape_type, self.config.active_cutter.diameter)
            gcode_cut_depth, gcode_z_safe_distance = self.extract_cut_depth_and_z_safe_distance(gcode_lines)
            x_size, y_size = self.read_in_custom_shape_dimentions(gcode_lines)
            
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
            circle_coordinates = self.rectangle_coordinates(self.config.active_config.canvas_shape_dims.d, self.config.active_config.canvas_shape_dims.d) #Circles are secretly rounded rectangles            

            # Add first point to end of coordinate list to complete the contour
            coordinates = circle_coordinates
            coordinates.append(coordinates[0])

            # Create a list of stepovers to add finishing passes
            finish_passes = 1
            finish_stepover = 0.5
            finish_stepdown = self.config.active_config.cutting_depths.material_thickness
            if finish_passes > 0:
                stepovers = [finish_stepover * (finish_passes - i) for i in range(finish_passes)]
                stepovers.append(0)

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
                                        roughing_pass)

                roughing_pass = False
                cutting_lines += circle 

        else:
            raise Exception("Shape type: '%s' not supported" % self.config.active_config.shape_type)

        # GCODE FILE STRUCTURE
        file_structure_1_shapes = ["rectangle", "square", "circle"]
        if self.config.active_config.shape_type in file_structure_1_shapes:
            output = "(%s)\nG90\nM3 S%d\nG0 %s\n\n%s\n(End)\nG0 Z%d\nM5\n" % (
                output_file[output_file.find("/")+1:], self.config.active_cutter.cutting_spindle_speed, safe_start_position, ''.join(cutting_lines), z_safe_distance)
        else:
            output = ''.join(cutting_lines)  # Use ''.join() to concatenate lines without spaces

        with open(output_file, 'w+') as out_file:
            out_file.write(output.decode('utf-8'))  # Use write() to write the entire output as a single string
            print("%s written" % output_file)

