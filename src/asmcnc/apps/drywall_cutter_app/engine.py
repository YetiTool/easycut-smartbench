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

config = config_loader.DWTConfig()

active_config = config.active_config
active_cutter = config.active_cutter

#Produce corner coordinates for a rectangle of size x, y
def rectangle_coordinates(x, y):
    if x <= 0 or y <= 0:
        return []  # Invalid dimensions, return an empty list

    # Define the coordinates for the four corners
    top_left = (0, y)
    top_right = (x, y)
    bottom_right = (x, 0)
    bottom_left = (0, 0)

    # Return the coordinates in clockwise order
    return [bottom_left, top_left, top_right, bottom_right]

#Adjust corner radius depending on the offset type (in, on, outside of line)
def offset_corner_radius(corner_radius, offset_type, tool_diameter):
    if offset_type == u"inside":
        return corner_radius - tool_diameter
    elif offset_type == u"outside":
        return corner_radius + tool_diameter
    elif offset_type == None:
        return corner_radius
    else: 
        raise  Exception(u"Unknown offset type. Please specify 'inside', 'outside' or 'none'.")

#Find the shape centre coordinates
def find_centre(coordinates, x_offset, y_offset):
    x_sum = 0
    y_sum = 0
    for x, y in coordinates:
        x_sum += x + x_offset
        y_sum += y + y_offset
    centre_x = x_sum / len(coordinates)
    centre_y = y_sum / len(coordinates)

    return centre_x, centre_y

#Check if a corner radius is present (and not tiny)
def find_corner_rads(radius):
    if radius > 0.09:
        return True
    else:
        return False

#Determine shape point direction
def is_clockwise(coordinates):
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
def correct_orientation(coordinates, clockwise):
    if clockwise:
        return coordinates[::-1]
    else:
        return coordinates

#Take in corner coordinates and return coordinates for arcs
def add_corner_coordinates(coordinates, shape_centre, corner_radius):
    new_coordinates = []
    for coordinate in coordinates:
        #Bottom left
        if coordinate[x] < shape_centre[x] and coordinate[y] < shape_centre[y]: 
            rad_point_1 = coordinate[x] + corner_radius, coordinate[y]
            rad_point_2 = coordinate[x], coordinate[y] + corner_radius
        #Top left
        elif coordinate[x] < shape_centre[x] and coordinate[y] > shape_centre[y]:
            rad_point_1 = coordinate[x], coordinate[y] - corner_radius
            rad_point_2 = coordinate[x] + corner_radius, coordinate[y]
        #Top right
        elif coordinate[x] > shape_centre[x] and coordinate[y] > shape_centre[y]:
            rad_point_1 = coordinate[x] - corner_radius, coordinate[y]
            rad_point_2 = coordinate[x], coordinate[y] - corner_radius
        #Bottom right
        elif coordinate[x] > shape_centre[x] and coordinate[y] < shape_centre[y]:
            rad_point_1 = coordinate[x], coordinate[y] + corner_radius
            rad_point_2 = coordinate[x] - corner_radius, coordinate[y]
        new_coordinates.append(rad_point_1)
        new_coordinates.append(rad_point_2)
    return new_coordinates 

#Calculate the difference in corner radius depending on offset type
def calculate_corner_radius_offset(offset_type, tool_diamter):
    tool_radius = tool_diamter / 2
    if offset_type == u"inside":
        offset_for_rads = -1 * tool_radius
    elif offset_type == u"outside":
        offset_for_rads = tool_radius
    else:
        offset_for_rads = 0
    return offset_for_rads

#Apply transformation for inside and outside line cutting
def apply_offset(coordinates, offset_type, tool_diameter, shape_centre):
    adjusted_coordinates = []
    if offset_type != None:
        tool_radius = tool_diameter / 2
        #x_offset = tool_radius 
        #y_offset = tool_radius 
        for coordinate in coordinates:

            if offset_type == u"inside":

                if coordinate[x] > shape_centre[x]: #RHS
                    x_offset = -1 * tool_radius #Move to the left
                else: #LHS
                    x_offset = tool_radius #Move to the right
                    
                if coordinate[y] > shape_centre[y]: #Top
                    y_offset = -1 * tool_radius #Move down
                else: #Bottom
                    y_offset = tool_radius #Move up

            elif offset_type == u"outside":

                if coordinate[x] < shape_centre[x]: #LHS
                    x_offset = -1 * tool_radius #Move to the left
                else:#RHS
                    x_offset = tool_radius #Move to the right

                if coordinate[y] < shape_centre[y]: #Bottom
                    y_offset = -1 * tool_radius #Move down
                else: #Top
                    y_offset = tool_radius #Move up
            new_coordinate = coordinate[x] + x_offset, coordinate[y] + y_offset 
            adjusted_coordinates.append(new_coordinate)
    else:
        adjusted_coordinates = coordinates

    return  adjusted_coordinates

    pass

#Produce a list of cut depths based on total depth and pass depth
def calculate_pass_depths(total_cut_depth, pass_depth):
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
def determine_cut_direction_clockwise(offset_type, climb):
    if climb and offset_type == u"outside" or not(climb) and offset_type == u"inside":
        return True
    else:
        return False

#For use when reordering gcode instructions
def swap_lines_after_keyword(input_list, keyword):
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
def replace_after_keyword(input_list, keyword, replacement):
    for i in xrange(len(input_list) - 1):
        if keyword.lower() in input_list[i].lower():
            if i + 1 < len(input_list):
                # Replace the first two letters of the line that follows the keyword
                input_list[i + 1] = replacement + input_list[i + 1][2:]
    return input_list

#Produce gcode instructions to cut a rounded (or not) rectangle
def cut_rectangle(coordinates, datum_x, datum_y, offset, tool_diameter, is_climb, corner_radius, pass_depth, feedrate, plungerate, total_cut_depth, z_safe_distance):
        # Ensure coordinates are all in clockwise order
        coordinates = correct_orientation(coordinates, is_clockwise(coordinates))

        # Find shape centre for further calcs
        shape_centre = find_centre(coordinates[:-1], 0,0) #datum_x, datum_y)

        # Apply offset for toolpath (inside, on, outside the line cutting)
        offset_coordinates = apply_offset(coordinates, offset, tool_diameter, shape_centre)

        clockwise_cutting = determine_cut_direction_clockwise(offset, is_climb)

        # Add corner coordinates if necessary
        radii_present = find_corner_rads(corner_radius)
        final_coordinates = offset_coordinates
        if radii_present:
            adjusted_corner_radius = corner_radius + calculate_corner_radius_offset(offset, tool_diameter)
            if adjusted_corner_radius > 0:
                final_coordinates = add_corner_coordinates(offset_coordinates, shape_centre, adjusted_corner_radius)
            else:
                radii_present = False
            

        pass_depths = calculate_pass_depths(total_cut_depth, pass_depth)

        # Time to make some gcode :)
        if clockwise_cutting:
            arc_instruction = u"G2"
        else:
            final_coordinates = correct_orientation(final_coordinates, True)
            arc_instruction = u"G3"

        cutting_lines = []

        for depth in pass_depths:
            gcode_instruction = "(Offset: %s)\n(New pass)\n" % offset
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
        cutting_lines = swap_lines_after_keyword(cutting_lines, u"New pass")
        # Speed up first XY move
        cutting_lines = replace_after_keyword(cutting_lines, u"New pass", u"G0")

        return cutting_lines

#Return lines in appropriate gcode file
def find_and_read_gcode_file(directory, shape_type, tool_diameter):
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
def adjust_feeds_and_speeds(gcode_lines, feedrate, plungerate, spindle_speed):
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
def extract_cut_depth_and_z_safe_distance(gcode_lines):
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
def replace_cut_depth_and_z_safe_distance(gcode_lines, gcode_cut_depth, gcode_z_safe_distance, new_cut_depth, new_z_safe_distance):
    output = []    
    for line in gcode_lines:
        original_line = line
        line = line.replace(str(gcode_cut_depth), str(new_cut_depth))
        line = line.replace(str(gcode_z_safe_distance), str(new_z_safe_distance))
        output.append(line)

    return output

#Add datum to each x and y move command
def apply_datum_offset(gcode_lines, x_adjustment, y_adjustment):
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
def repeat_for_depths(gcode_lines, pass_depths, start_line_key, end_line_key):
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

#Main
def engine_run():

    x = 0  # Identifier for use in arrays
    y = 1  # Identifier for use in arrays

    output_file = config.active_config.shape_type + u".nc"
    safe_start_position = u"X0 Y0 Z10"
    z_safe_distance = 5
    cutting_lines = []
    pass_depths = []
    stepovers = [0]
    radii_present = None

    if active_cutter.cutting_direction.lower() == "climb":
        is_climb = True
    else:
        is_climb = False

    # Calculated parameters
    total_cut_depth = active_config.cutting_depths.material_thickness - active_config.cutting_depths.bottom_offset

    if config.active_config.shape_type == u"rectangle":
        rect_coordinates = rectangle_coordinates(active_config.canvas_shape_dims.x,active_config.canvas_shape_dims.x)
        if len(rect_coordinates) != 4:
            raise Exception(u"Sir, rectangles have 4 sides, not %d" % len(rect_coordinates))

        # Add first point to end of coordinate list to complete the contour
        coordinates = rect_coordinates
        coordinates.append(coordinates[0])

        # Create a list of stepovers to add finishing passes
        finish_passes = 1
        finish_stepover = 0.5
        finish_stepdown = active_config.cutting_depths.material_thickness
        if finish_passes > 0:
            stepovers = [finish_stepover * (finish_passes - i) for i in range(finish_passes)]
            stepovers.append(0)

        # Produce instructions for each complete rectangle
        for stepover in stepovers:
            effective_tool_diameter = active_cutter.diameter + (stepover * 2)
            pass_depth = finish_stepdown if stepover != max(stepovers) else active_config.cutting_depths.depth_per_pass
            rectangle = cut_rectangle(coordinates,
                                    active_config.datum_position.x,
                                    active_config.datum_position.y,
                                    config.active_config.toolpath_offset,
                                    effective_tool_diameter,
                                    is_climb,
                                    active_config.canvas_shape_dims.r,
                                    pass_depth,
                                    active_cutter.cutting_feedrate,
                                    active_cutter.plunge_rate,
                                    total_cut_depth,
                                    z_safe_distance)

            cutting_lines += rectangle

    elif config.active_config.shape_type == u"geberit":
        source_folder_name = "gcode" 
        source_folder_path = os.path.join(source_folder_name)   

        #Read in data
        gcode_lines = find_and_read_gcode_file(source_folder_path, config.active_config.shape_type, active_cutter.diameter)
        gcode_cut_depth, gcode_z_safe_distance = extract_cut_depth_and_z_safe_distance(gcode_lines)
        
        #Remove header info
        gcode_lines = gcode_lines[next((i for i, s in enumerate(gcode_lines) if re.search(r"T[1-9]", s)), None):]

        #Adjust feeds, speeds and Z values
        gcode_lines = adjust_feeds_and_speeds(gcode_lines, active_cutter.cutting_feedrate, active_cutter.plunge_rate, active_cutter.cutting_spindle_speed)
        gcode_lines = replace_cut_depth_and_z_safe_distance(gcode_lines, gcode_cut_depth, gcode_z_safe_distance, "[cut depth] ", z_safe_distance)

        #Apply datum offset
        gcode_lines = apply_datum_offset(gcode_lines, DatumPosition.x, DatumPosition.y)

        #Apply pass depths
        pass_depths = calculate_pass_depths(total_cut_depth, active_config.cutting_depths.depth_per_pass)
        start_condition = next((i for i, s in enumerate(gcode_lines) if re.search(r"T[1-9]", s)), None)
        end_condition = next((i for i, s in enumerate(gcode_lines) if re.search(r"M5", s)), None)
        gcode_lines = repeat_for_depths(gcode_lines, pass_depths, start_condition, end_condition)

        
        cutting_lines = gcode_lines

    else:
        raise Exception("Shape type: '%s' not supported" % config.active_config.shape_type)

    # GCODE FILE STRUCTURE
    if config.active_config.shape_type == "rectangle":
        output = "(%s)\nM3 S%d\nG0 %s\n\n%s\n(End)\nG0 Z%d\nM5\n" % (
            output_file, active_cutter.cutting_spindle_speed, safe_start_position, ''.join(cutting_lines), z_safe_distance)
    else:
        output = ''.join(cutting_lines)  # Use ''.join() to concatenate lines without spaces

    with open(output_file, 'w+') as out_file:
        out_file.write(output)  # Use write() to write the entire output as a single string
        print("%s written" % output_file)


