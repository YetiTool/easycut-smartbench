'''
Author: BP
Description: This module contains the GCodeEngine class, which is responsible for producing gcode instructions for cutting shapes. The class contains methods for producing gcode instructions for cutting rectangles, circles, and custom shapes. The class also contains methods for reading in gcode files, adjusting feeds and speeds, and replacing Z values. The class is used by the DrywallCutterApp class to produce gcode instructions for cutting shapes.

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
import decimal, os, re, math
from collections import OrderedDict

from asmcnc import paths
from asmcnc.apps.drywall_cutter_app.config.config_options import CuttingDirectionOptions, ShapeOptions
from asmcnc.comms.logging_system.logging_system import Logger

class GCodeEngine(object):
    def __init__(self, router_machine, dwt_config, coordinate_system):
        self.config = dwt_config
        self.m = router_machine
        self.cs = coordinate_system

        self.finishing_passes = 1
        self.finishing_stepover = 0.5
        self.finishing_stepdown = 12

        # Globals
        self.x = 0  # Identifier for use in arrays
        self.y = 1  # Identifier for use in arrays
        self.custom_gcode_shapes = ["geberit"]  # List of custom shapes that require gcode files
        self.source_folder_path = os.path.join(paths.DWT_APP_PATH, "gcode")

        # Constants
        self.CORNER_RADIUS_THRESHOLD = 0.09  # Minimum corner radius to be considered a corner radius

    # Produce corner coordinates for a rectangle of size x, y
    def rectangle_coordinates(self, x, y, x_min=0, y_min=0):
        if x <= 0 or y <= 0 and self.config.active_config.shape_type.lower() not in ["circle", "geberit", "line"]:
            return None  # Invalid dimensions, return None

        # Define the coordinates for the four corners
        top_left = (x_min, y)
        top_right = (x, y)
        bottom_left = (x_min, y_min)
        bottom_right = (x, y_min)

        # Return the coordinates in clockwise order
        return [bottom_left, top_left, top_right, bottom_right]

    # Find the shape centre coordinates
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

    # Check if a corner radius is present (and not tiny)
    def find_corner_rads(self, radius):
        return radius > self.CORNER_RADIUS_THRESHOLD

    # Determine shape point direction
    def is_clockwise(self, coordinates):
        total = 0
        for i in xrange(len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[(i + 1) % len(coordinates)]  # Handle the wraparound at the end
            total += (x2 - x1) * (y2 + y1)

        return total > 0

    # Reverse coordinates if need to be clockwise
    def correct_orientation(self, coordinates, clockwise):
        if not clockwise:
            return coordinates[::-1]
        return coordinates

    # Take in corner coordinates and return coordinates for arcs
    def add_corner_coordinates(self, coordinates, shape_centre, corner_radius):
        new_coordinates = []
        for coordinate in coordinates:
            # Bottom left
            if coordinate[self.x] < shape_centre[self.x] and coordinate[self.y] < shape_centre[self.y]:
                rad_point_1 = coordinate[self.x], coordinate[self.y] + corner_radius
                rad_point_2 = coordinate[self.x] + corner_radius, coordinate[self.y]
            # Top left
            elif coordinate[self.x] < shape_centre[self.x] and coordinate[self.y] > shape_centre[self.y]:
                rad_point_1 = coordinate[self.x] + corner_radius, coordinate[self.y]
                rad_point_2 = coordinate[self.x], coordinate[self.y] - corner_radius
            # Top right
            elif coordinate[self.x] > shape_centre[self.x] and coordinate[self.y] > shape_centre[self.y]:
                rad_point_1 = coordinate[self.x], coordinate[self.y] - corner_radius
                rad_point_2 = coordinate[self.x] - corner_radius, coordinate[self.y]
            # Bottom right
            elif coordinate[self.x] > shape_centre[self.x] and coordinate[self.y] < shape_centre[self.y]:
                rad_point_1 = coordinate[self.x] - corner_radius, coordinate[self.y]
                rad_point_2 = coordinate[self.x], coordinate[self.y] + corner_radius
            new_coordinates.append(rad_point_1)
            new_coordinates.append(rad_point_2)
        return new_coordinates

    # Calculate the difference in corner radius depending on offset type
    def calculate_corner_radius_offset(self, offset_type, tool_diamter):
        tool_radius = tool_diamter / 2
        if offset_type == "inside":
            offset_for_rads = -1 * tool_radius
        elif offset_type == "outside":
            offset_for_rads = tool_radius
        else:
            offset_for_rads = 0
        return offset_for_rads

    # Apply transformation for inside and outside line cutting
    def apply_offset(self, coordinates, offset_type, tool_diameter, shape_centre):
        x_offset = 0
        y_offset = 0
        adjusted_coordinates = []
        if offset_type != None:
            tool_radius = tool_diameter / 2
            for coordinate in coordinates:
                if offset_type == "inside":
                    if coordinate[self.x] > shape_centre[self.x]:  # RHS
                        x_offset = -1 * tool_radius  # Move to the left
                    else:  # LHS
                        x_offset = tool_radius  # Move to the right
                    if coordinate[self.y] > shape_centre[self.y]:  # Top
                        y_offset = -1 * tool_radius  # Move down
                    else:  # Bottom
                        y_offset = tool_radius  # Move up
                elif offset_type == "outside":
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

    # Produce a list of cut depths based on total depth and pass depth
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

    # Determine if the cut direction should be clockwise or not
    def determine_cut_direction_clockwise(self, offset_type, climb):
        if offset_type in ["inside", "on"]:
            return climb
        elif offset_type == "outside":
            return not climb
        else:
            raise ValueError("Offset type must be 'on, 'inside' or 'outside'. Got '{}'.".format(offset_type))

    # For use when reordering gcode instructions
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

    # For use when reordering gcode instructions
    def replace_mode_after_keyword(self, input_list, keyword, replacement_mode):
        for i in xrange(len(input_list) - 1):
            if keyword.lower() in input_list[i].lower():
                if i + 1 < len(input_list):
                    # Replace the first two letters of the line that follows the keyword
                    input_list[i + 1] = replacement_mode + input_list[i + 1][2:]
        return input_list

    # Produce gcode instructions to cut a rounded (or not) rectangle
    def cut_rectangle(self, coordinates, datum_x, datum_y, offset, tool_diameter, is_climb, corner_radius, pass_depth, feedrate, plungerate, total_cut_depth, z_safe_distance, pass_type, simulate, first_plunge=True):
        if offset == "pocket":
            offset = "inside"  # Pocketing operations exist inside the shape perimeter - the additional passes are handled by loops in engine_run

        # Ensure coordinates are all in clockwise order
        coordinates = self.correct_orientation(coordinates, self.is_clockwise(coordinates))

        # Find shape centre for further calcs
        shape_centre = self.find_centre(coordinates[:-1], 0, 0)

        # Apply offset for toolpath (inside, on, outside the line cutting)
        offset_coordinates = self.apply_offset(coordinates, offset, tool_diameter, shape_centre)

        # Add corner coordinates if necessary
        radii_present = self.find_corner_rads(corner_radius)
        final_coordinates = offset_coordinates
        if radii_present:
            adjusted_corner_radius = corner_radius + self.calculate_corner_radius_offset(offset, tool_diameter)
            if adjusted_corner_radius > 0:
                final_coordinates = self.add_corner_coordinates(reversed(offset_coordinates), shape_centre, adjusted_corner_radius)
            else:
                radii_present = False

        pass_depths = self.calculate_pass_depths(total_cut_depth, pass_depth)

        # Correct orientation for climb or conventional cutting
        clockwise_cutting = self.determine_cut_direction_clockwise(offset, is_climb)

        # Determine if the tool is going to be lifted out of the material (no if pocketing)
        tool_lifting = z_safe_distance > 0 or first_plunge

        if clockwise_cutting:
            final_coordinates = final_coordinates[::-1]

        if clockwise_cutting:
            arc_instruction = "G2"
        else:
            arc_instruction = "G3"

        # Time to make some gcode :)
        cutting_lines = []

        for depth in pass_depths:
            if not simulate:
                gcode_instruction = "(Offset: %s)\n(%s)\n" % (offset, pass_type)
                cutting_lines.append(gcode_instruction)
                cutting_lines.append("G1 Z-%s F%s\n" % (depth, plungerate))
            else:
                gcode_instruction = "(Simulation pass)\n"
                cutting_lines.append(gcode_instruction)
                cutting_lines.append("G1 Z%s F%s\n" % (depth, plungerate))
            # Cut the shape
            if not radii_present:
                # Logic for straight lines only
                for coordinate in final_coordinates[::-1]:
                    if tool_lifting:
                        add_feedrate_to_line = 1 == final_coordinates.index(coordinate)  # Second line
                    else:
                        add_feedrate_to_line = 0 == final_coordinates.index(coordinate)  # First line
                    if first_plunge:
                        add_feedrate_to_line = 3 == final_coordinates.index(coordinate)  # Fourth line

                    gcode_instruction = "G1 X%s Y%s %s\n" % (coordinate[0] + datum_x, coordinate[1] + datum_y, 'F%s' % feedrate if add_feedrate_to_line else '')
                    cutting_lines.append(gcode_instruction)
            else:
                # Logic for when corner rads are present
                arc_flag = True
                for coordinate in final_coordinates[:-1]:
                    if tool_lifting:
                        add_feedrate_to_line = 1 == final_coordinates.index(coordinate)  # Second line
                    else:
                        add_feedrate_to_line = 0 == final_coordinates.index(coordinate)  # First line
                    if first_plunge:
                        add_feedrate_to_line = 1 == final_coordinates.index(coordinate)  # Second line

                    if arc_flag:
                        gcode_instruction = "G1 X%s Y%s %s\n" % (coordinate[0] + datum_x, coordinate[1] + datum_y, 'F%s' % feedrate if add_feedrate_to_line else '')
                    else:
                        gcode_instruction = "%s X%s Y%s R%s %s\n" % (arc_instruction, coordinate[0] + datum_x, coordinate[1] + datum_y, adjusted_corner_radius, 'F%s' % feedrate if add_feedrate_to_line else '')
                    arc_flag = not arc_flag
                    cutting_lines.append(gcode_instruction)
            cutting_lines.append("G1 Z%s F%d\n\n" % (z_safe_distance, plungerate))

        gcode_pass_headers = ["New pass", "Roughing pass", "Finishing pass", "Simulation pass"]
        if tool_lifting:  # Only perform these modifications if the tool is being lifted out of the material
            for header in gcode_pass_headers:
                # Correct gcode order
                cutting_lines = self.swap_lines_after_keyword(cutting_lines, header)

                # Speed up first XY move
                cutting_lines = self.replace_mode_after_keyword(cutting_lines, header, "G0")

        return cutting_lines

    # Produce gcode instructions to cut a line
    def cut_line(self, datum_x, datum_y, length, tool_diameter, orientation, pass_depth, feedrate, plungerate, total_cut_depth, z_safe_distance, simulate=False):
        pass_depths = self.calculate_pass_depths(total_cut_depth, pass_depth)
        tool_radius = tool_diameter / 2
        x = 0
        y = 1
        direction_flag = True

        # Start at z safe distance
        gcode_lines = ["G0 Z{}".format(z_safe_distance)]

        # Define line start and end coordinates
        if orientation == "vertical":
            start_coordinate = [datum_x + tool_radius, datum_y]
            end_coordinate = [datum_x + length - tool_radius, datum_y]
        elif orientation == "horizontal":
            start_coordinate = [datum_x, datum_y + tool_radius]
            end_coordinate = [datum_x, datum_y + length - tool_radius]
        else:
            raise ValueError("Orientation must be 'vertical' or 'horizontal'. Got '{}'".format(orientation))

        # Add line cutting gcode
        gcode_lines.append("G0 X{} Y{}".format(start_coordinate[x], start_coordinate[y])) # Move to start position

        for depth in pass_depths:

            if simulate:
                gcode_lines.append("G1 Z{} F{}".format(depth, plungerate)) # Raise to height {depth}
            else:
                gcode_lines.append("G1 Z-{} F{}".format(depth, plungerate)) # Plunge to depth


            if not(direction_flag):
                gcode_lines.append("G1 X{} Y{} F{}".format(start_coordinate[x], start_coordinate[y], feedrate)) # Move to start position
            else:
                gcode_lines.append("G1 X{} Y{} F{}".format(end_coordinate[x], end_coordinate[y], feedrate)) # Move to end position
            direction_flag = not(direction_flag)

        gcode_lines.append("G1 Z{} F{}".format(z_safe_distance, plungerate)) # Lift to Z safe distance

        for i in range(len(gcode_lines)):
            gcode_lines[i] = gcode_lines[i] + "\n"

        return gcode_lines

    @staticmethod
    def calculate_arc_point(x1, y1, x2, y2, r, d, clockwise):
        # Calculate the center of the circle (midpoint of start and end)
        def find_arc_center(x1, y1, x2, y2, clockwise):
            """
            Find the center of the circle that the arc is part of.
            Works only for 90 degree arcs.
            """

            x_delta_positive = x2 - x1 > 0
            y_delta_positive = y2 - y1 > 0

            bool = x_delta_positive == y_delta_positive

            x_use_start = not (bool)
            y_use_start = bool

            if not clockwise:
                x_use_start = not x_use_start
                y_use_start = not y_use_start

            x = x1 if x_use_start else x2
            y = y1 if y_use_start else y2

            return x, y

        cx, cy = find_arc_center(x1, y1, x2, y2, clockwise)

        # Calculate the starting angle
        start_angle = math.atan2(y1 - cy, x1 - cx)

        # Calculate the angle traversed
        traversed_angle = -d / r

        # Determine the direction
        if clockwise:
            final_angle = start_angle + traversed_angle
        else:
            final_angle = start_angle - traversed_angle

        # Calculate the new point coordinates
        new_x = cx + r * math.cos(final_angle)
        new_y = cy + r * math.sin(final_angle)

        x = 0

        return round(new_x, 2), round(new_y, 2)

    def add_straight_tabs(self, xy_feed, z_feed, linear_distance_moved, tab_spacing, tab_width, tab_height, previous_x_pos, previous_y_pos, last_x, last_y, x_delta, y_delta, current_z, tab_top_z, line, three_d_tabs):
        number_of_tabs = int(linear_distance_moved / (tab_spacing + tab_width))
        tab_inset_distance = linear_distance_moved - ((tab_width * number_of_tabs) + tab_spacing * (number_of_tabs - 1))
        tab_inset_distance /= 2

        tabs_dict = {}

        if x_delta:
            for i in range(number_of_tabs):
                polariser = 1 if x_delta > 0 else -1
                tab_x = previous_x_pos + polariser * ((tab_spacing * i) + (tab_width * i) + tab_inset_distance)
                tab_y = last_y

                tab_x = round(tab_x, 2)

                tabs_dict['tab_{}'.format(i + 1)] = {
                    'start_x': tab_x,
                    'start_y': tab_y,
                    'end_x': tab_x + polariser * tab_width,
                    'end_y': tab_y,
                    'height': tab_height
                }

        elif y_delta:
            for i in range(number_of_tabs):
                polariser = 1 if y_delta > 0 else -1
                tab_x = last_x
                tab_y = previous_y_pos + polariser * (
                        (tab_spacing * i) + (tab_width * i) + tab_inset_distance)

                tab_y = round(tab_y, 2)

                tabs_dict['tab_{}'.format(i + 1)] = {
                    'start_x': tab_x,
                    'start_y': tab_y,
                    'end_x': tab_x,
                    'end_y': tab_y + polariser * tab_width,
                    'height': tab_height
                }

        tabs_dict = OrderedDict(sorted(tabs_dict.items()))

        modified_gcode = []

        for tab in tabs_dict.values():
            tab_cut_height = current_z if current_z > tab_top_z else tab_top_z
            if current_z < tab_top_z and ('X' in line or 'Y' in line):
                if line.startswith('G1'):
                    if three_d_tabs:
                        tab_centre_x = (tab['start_x'] + tab['end_x']) / 2
                        tab_centre_y = (tab['start_y'] + tab['end_y']) / 2
                        modified_gcode.append('G1 X{} Y{} F{}\n'.format(tab['start_x'], tab['start_y'], xy_feed))
                        modified_gcode.append('G1 X{} Y{} Z{}\n'.format(tab_centre_x, tab_centre_y, tab_cut_height))
                        modified_gcode.append('G1 X{} Y{} Z{}\n'.format(tab['end_x'], tab['end_y'], current_z))
                    else:
                        modified_gcode.append('G1 X{} Y{} F{}\n'.format(tab['start_x'], tab['start_y'], xy_feed))
                        modified_gcode.append('G1 Z{} F{}\n'.format(tab_cut_height, z_feed))
                        modified_gcode.append('G1 X{} Y{} F{}\n'.format(tab['end_x'], tab['end_y'], xy_feed))
                        modified_gcode.append('G1 Z{} F{}\n'.format(current_z, z_feed))

        return modified_gcode

    def add_arc_tabs(self, xy_feed, z_feed, parts, line, last_x, last_y, current_x, current_y, tab_spacing, tab_width, current_z, tab_top_z, three_d_tabs):
        modified_gcode = []
        r_value = None
        for part in parts:
            if part.startswith('G'):
                arc_command = part
            if part.startswith('R'):
                r_value = float(part[1:])

        if r_value is not None:
            cx = (last_x + current_x) / 2
            cy = (last_y + current_y) / 2
            radius = r_value

            start_angle = math.atan2(last_y - cy, last_x - cx)
            end_angle = math.atan2(current_y - cy, current_x - cx)

            if line.startswith('G2'):
                if end_angle > start_angle:
                    end_angle -= 2 * math.pi
            else:
                if start_angle > end_angle:
                    start_angle -= 2 * math.pi

            arc_length = abs(end_angle - start_angle) * radius
            arc_length /= 2

            if arc_length >= tab_spacing:
                number_of_tabs = int(arc_length / (tab_spacing + tab_width))
                tab_inset_distance = arc_length - ((tab_width * number_of_tabs) + tab_spacing * (number_of_tabs - 1))
                tab_inset_distance /= 2

                last_x, last_y, current_x, current_y = current_x, current_y, last_x, last_y

                for i in range(number_of_tabs):
                    tab_start_distance = arc_length - ((tab_spacing * i) + (tab_width * i) + tab_inset_distance)
                    tab_end_distance = arc_length - ((tab_spacing * i) + (tab_width * i) + tab_width + tab_inset_distance)
                    tab_start_x, tab_start_y = self.calculate_arc_point(last_x, last_y, current_x, current_y, radius, tab_start_distance, clockwise=arc_command == 'G3')
                    tab_end_x, tab_end_y = self.calculate_arc_point(last_x, last_y, current_x, current_y, radius, tab_end_distance, clockwise=arc_command == 'G3')

                    tab_cut_height = current_z if current_z > tab_top_z else tab_top_z

                    if three_d_tabs:
                        tab_centre_x = (tab_start_x + tab_end_x) / 2
                        tab_centre_y = (tab_start_y + tab_end_y) / 2
                        modified_gcode.append('{} X{} Y{} R{} F{}\n'.format(arc_command, round(tab_start_x, 2), round(tab_start_y, 2), radius, xy_feed))
                        modified_gcode.append('{} X{} Y{} Z{} R{}\n'.format(arc_command, round(tab_centre_x, 2), round(tab_centre_y, 2), tab_cut_height, radius))
                        modified_gcode.append('{} X{} Y{} Z{} R{}\n'.format(arc_command, round(tab_end_x, 2), round(tab_end_y, 2), current_z, radius))
                    else:
                        modified_gcode.append('{} X{} Y{} R{} F{}\n'.format(arc_command, round(tab_start_x, 2), round(tab_start_y, 2), radius, xy_feed))
                        modified_gcode.append('G1 Z{} F{}\n'.format(tab_cut_height, z_feed))
                        modified_gcode.append('{} X{} Y{} R{} F{}\n'.format(arc_command, round(tab_end_x, 2), round(tab_end_y, 2), radius, xy_feed))
                        modified_gcode.append('G1 Z{} F{}\n'.format(current_z, z_feed))

        return modified_gcode

    def add_tabs_to_gcode(self, gcode_lines, total_cut_depth, tab_height, tab_width, tab_spacing, three_d_tabs=False):
        """
        Adds tabs of specified height, width, and spacing to the given G-code lines.

        Parameters:
        - gcode_lines (list of str): The list of G-code lines to modify.
        - tab_height (float): The height of the tabs.
        - tab_width (float): The width of the tabs.
        - tab_spacing (float): The distance between the start of each tab.

        Returns:
        - list of str: The modified list of G-code lines with tabs.
        """
        modified_gcode = []
        current_z = None
        current_x = None
        current_y = None
        xy_feed = self.config.active_cutter.parameters.cutting_feed_rate
        z_feed = self.config.active_cutter.parameters.plunge_feed_rate
        last_x = 0
        last_y = 0
        previous_x_pos = 0
        previous_y_pos = 0
        linear_distance_moved = 0

        tab_top_z = - (total_cut_depth - tab_height)
        if tab_top_z > 0:
            tab_top_z = 0

        for line in gcode_lines:
            tabs_added = False
            parts = line.split()

            if line.startswith('G0') or line.startswith('G1') or line.startswith('G2') or line.startswith('G3'):
                for part in parts:
                    if part.startswith('Z'):
                        current_z = float(part[1:])
                    elif part.startswith('X'):
                        current_x = float(part[1:])
                    elif part.startswith('Y'):
                        current_y = float(part[1:])
                    elif part.startswith('F'):
                        if 'X' in line or 'Y' in line:
                            xy_feed = float(part[1:])
                        elif 'Z' in line:
                            z_feed = float(part[1:])

            # Add tabs if moving in the XY plane at cutting depth
            if current_z is not None and current_z <= tab_top_z and current_x is not None and current_y is not None:
                if line.startswith(('G0', 'G1', 'G2', 'G3')):
                    if last_x is not None and last_y is not None:
                        linear_distance_moved = ((current_x - last_x) ** 2 + (current_y - last_y) ** 2) ** 0.5
                        x_delta = current_x - last_x
                        y_delta = current_y - last_y

                    g1_last_x = current_x
                    g1_last_y = current_y

                if linear_distance_moved >= tab_spacing and line.startswith(('G0', 'G1')):
                    tabs_added = True
                    modified_gcode.extend(self.add_straight_tabs(xy_feed, z_feed, linear_distance_moved, tab_spacing, tab_width, tab_height, previous_x_pos, previous_y_pos, g1_last_x, g1_last_y, x_delta, y_delta, current_z, tab_top_z, line, three_d_tabs))

                if line.startswith('G2') or line.startswith('G3'):
                    tabs_added = True
                    modified_gcode.extend(self.add_arc_tabs(xy_feed, z_feed, parts, line, last_x, last_y, current_x, current_y, tab_spacing, tab_width, current_z, tab_top_z, three_d_tabs))

                last_x = current_x
                last_y = current_y

                g1_last_x = current_x
                g1_last_y = current_y

            previous_x_pos = last_x
            previous_y_pos = last_y

            if tabs_added:
                if ('X' in line or 'Y' in line) and ('F' not in line):
                    line = line[:-1] + 'F{}\n'.format(xy_feed)
                if ('Z' in line) and ('F' not in line):
                    line = line[:-1] + 'F{}\n'.format(z_feed)

            modified_gcode.append(line)

        return modified_gcode

    # Return lines in appropriate gcode file
    def find_and_read_gcode_file(self, directory, shape_type, tool_diameter, orientation=None):
        for file in os.listdir(directory):
            filename = file.lower().strip()
            if shape_type in filename and str(tool_diameter)[:-2] + "mm" in filename and (orientation is None or orientation in filename):
                file_path = os.path.join(directory, file)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as file:
                            Logger.debug("Reading {} gcode file: {}".format(shape_type, file_path))
                            return file.readlines()
                    except IOError:
                        Logger.Warning("An error occurred while reading the Gcode file")
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

    # Extract Z data from gcode header (manually inserted)
    def extract_cut_depth_and_z_safe_distance(self, gcode_lines):
        cut_depth_pattern = r"Cut depth: (-?\d+\.\d+)"
        z_safe_distance_pattern = r"Z safe distance: (\d+\.\d+)"

        cut_depth_value = None
        z_safe_distance_value = None

        if not gcode_lines:
            raise Exception("Gcode file is empty.")

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

        if cut_depth_value is None or z_safe_distance_value is None:
            raise Exception("Unable to gather cut depth and Z safe distance data.")

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

    # Add datum to each x and y move command
    def apply_datum_offset(self, gcode_lines, x_adjustment, y_adjustment):
        if x_adjustment == 0 and y_adjustment == 0:
            return gcode_lines
        adjusted_lines = []
        for line in gcode_lines:
            if line.startswith("G1Z") or line.startswith("G1 Z"):
                adjusted_lines.append(line)
                continue

            parts = re.findall(r'[A-Z][0-9.-]+', line)
            adjusted_parts = ""
            for part in parts:
                if part.startswith('X'):
                    x_value = float(part[1:])
                    adjusted_x = x_value + x_adjustment
                    adjusted_parts += (' X{}'.format(self.format_float(adjusted_x)))
                elif part.startswith('Y'):
                    y_value = float(part[1:])
                    adjusted_y = y_value + y_adjustment
                    adjusted_parts +=(' Y{}'.format(self.format_float(adjusted_y)))
                else:
                    adjusted_parts += part
            adjusted_lines.append(adjusted_parts)
        return adjusted_lines

    # For use with apply_datum_offset
    def format_float(*args):
        value = args[1]
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
            output.extend(cut_lines)

        if end_line_key < len(gcode_lines):
            output.extend(gcode_lines[end_line_key:])

        return output

    # Add partoff cut for geberit shape
    def add_partoff(self, gcode_lines, insertion_key, start_coordinate, end_coordinate, pass_depths, feedrate, plungerate, z_safe_distance):
        x = 0
        y = 1
        insert_index = None
        partoff_gcode = ["(Partoff)"] # First line of partoff section
        direction_flag = True

        # Find index to insert partoff line
        insertion_key = insertion_key.lower()
        for i in range(len(gcode_lines)):
            if insertion_key in gcode_lines[i].lower():
                insert_index = i
                break
        if insert_index is None:
            raise Exception ("Unable to find " + insertion_key + " in gcode")

        # Generate partoff line gcode
        partoff_gcode.append("G1 Z" + str(z_safe_distance)) # Lift to Z safe distance
        partoff_gcode.append("G0 X" + str(start_coordinate[x]) + " Y" + str(start_coordinate[y]) + "F" + str(feedrate)) # Go to start position
        for depth in pass_depths:
            if direction_flag: # x min -> x max pass
                partoff_gcode.append("G1 Z-" + str(depth) + " F" + str(plungerate)) # Plunge to depth
                partoff_gcode.append("G1 X" + str(end_coordinate[x]) + " Y" + str(end_coordinate[y])+ "F" + str(feedrate)) # Go to end position
            else: # x max -> x min pass
                partoff_gcode.append("G1 Z-" + str(depth) + " F" + str(plungerate)) # Plunge to depth
                partoff_gcode.append("G1 X" + str(start_coordinate[x]) + " Y" + str(start_coordinate[y])+ "F" + str(feedrate)) # Go to start position
            direction_flag = not(direction_flag)
        partoff_gcode.append("G1 Z" + str(z_safe_distance)) # Lift to Z safe distance

        # Insert partoff gcode
        gcode_part_1 = gcode_lines[:insert_index]
        gcode_part_2 = gcode_lines[insert_index:]

        return gcode_part_1 + partoff_gcode + gcode_part_2

    # Extract dimension data from gcode header (manually inserted)
    def read_in_custom_shape_dimensions(self, gcode_lines):
        x_dim_pattern = r"Final part x dim: (-?\d+\.?\d*)"
        y_dim_pattern = r"Final part y dim: (-?\d+\.?\d*)"
        x_min_pattern = r"x min: (-?\d+\.?\d*)"
        y_min_pattern = r"y min: (-?\d+\.?\d*)"

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
                break  # Exit the loop once all values have been found

        missing_values = [dim for dim, value in zip(['x_dim', 'y_dim', 'x_min', 'y_min'], [x_dim, y_dim, x_min, y_min]) if value is None]
        if missing_values:
            raise Exception("Unable to gather shape dimension data. Missing values: {}".format(', '.join(missing_values)))

        return x_dim, y_dim, x_min, y_min

    # For use in UI not engine
    def get_custom_shape_extents(self):
        if self.config.active_config.shape_type.lower() in self.custom_gcode_shapes:
            # Read in data
            gcode_lines = self.find_and_read_gcode_file(self.source_folder_path, self.config.active_config.shape_type, self.config.active_cutter.dimensions.diameter, orientation=self.config.active_config.rotation)

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

    def remove_redudant_lines(self, gcode_lines):
        """
        Remove moves that result in no machine movement
        """
        x_pos = 0
        y_pos = 0
        z_pos = 0

        last_x = 0
        last_y = 0
        last_z = 0

        output = []

        for line in gcode_lines:
            if line.startswith('G0') or line.startswith('G1') or line.startswith('G2') or line.startswith('G3'):
                parts = line.split()
                for part in parts:
                    if part.startswith('X'):
                        x_pos = float(part[1:])
                    elif part.startswith('Y'):
                        y_pos = float(part[1:])
                    elif part.startswith('Z'):
                        z_pos = float(part[1:])

                if x_pos != last_x or y_pos != last_y or z_pos != last_z:
                    output.append(line)
                    last_x = x_pos
                    last_y = y_pos
                    last_z = z_pos
            else:
                output.append(line)

        output.append("\n")

        return output

    # Main
    def engine_run(self, simulate=False):
        filename = self.config.active_config.shape_type + ".nc"
        output_path = os.path.join(paths.DWT_TEMP_GCODE_PATH, filename)
        safe_start_position = "X0 Y0 Z10"
        z_safe_distance = 5

        stepover_z_hop_distance = 0
        cutting_pass_depth = self.config.active_cutter.parameters.recommended_depth_per_pass if self.config.active_config.cutting_depths.auto_pass else self.config.active_config.cutting_depths.depth_per_pass
        cutting_lines = []
        simulation_z_height = 5 # mm
        simulation_plunge_rate = 750 # mm/s
        simulation_feedrate = 6000 # mm/s
        geberit_partoff = False

        tab_spacing = 20  # mm
        tab_width = 10  # mm
        tab_height = self.config.active_config.cutting_depths.material_thickness * 0.6
        if tab_height > 5:
            tab_height = 5
        three_d_tabs = True

        # Compensate for tool diameter
        tab_width = tab_width + self.config.active_cutter.dimensions.diameter

        is_climb = (self.config.active_cutter.parameters.cutting_direction == CuttingDirectionOptions.CLIMB.value
                    or self.config.active_cutter.parameters.cutting_direction == CuttingDirectionOptions.BOTH.value)

        # Calculated parameters
        total_cut_depth = self.config.active_config.cutting_depths.material_thickness + self.config.active_config.cutting_depths.bottom_offset

        def calculate_stepovers(start, stop, step):
            return [round(start - i * step, 3) for i in range(int((start - stop) / step) + 1)]

        # Assign defaults
        def rectangle_default_parameters(simulate=False):
            parameters = {
                'coordinates': coordinates,
                'datum_x': 0,
                'datum_y': 0,
                'offset': self.config.active_config.toolpath_offset,
                'tool_diameter': 0 if self.config.active_cutter.dimensions.diameter is None else self.config.active_cutter.dimensions.diameter,
                'is_climb': is_climb,
                'corner_radius': self.config.active_config.canvas_shape_dims.r,
                'pass_depth': cutting_pass_depth,
                'feedrate': self.config.active_cutter.parameters.cutting_feed_rate,
                'plungerate': self.config.active_cutter.parameters.plunge_feed_rate,
                'total_cut_depth': total_cut_depth,
                'z_safe_distance': z_safe_distance,
                'pass_type': "Roughing pass",
                'simulate': simulate,
                'first_plunge': True
                }
            if simulate:
                parameters['pass_depth'] = simulation_z_height
                parameters['feedrate'] = simulation_feedrate
                parameters['plungerate'] = simulation_plunge_rate
                parameters['total_cut_depth'] = simulation_z_height
            return parameters

        def circle_default_parameters(simulate=False):
            parameters = rectangle_default_parameters(simulate=simulate)
            parameters['corner_radius'] = self.config.active_config.canvas_shape_dims.d/2
            return parameters

        def line_default_parameters(simulate=False):
            parameters = {
                'datum_x': self.config.active_config.datum_position.x,
                'datum_y': self.config.active_config.datum_position.y,
                'length': self.config.active_config.canvas_shape_dims.l,
                'tool_diameter': 0 if self.config.active_cutter.dimensions.diameter is None else self.config.active_cutter.dimensions.diameter,
                'orientation': self.config.active_config.rotation,
                'pass_depth': self.config.active_config.cutting_depths.depth_per_pass,
                'feedrate': self.config.active_cutter.parameters.cutting_feed_rate,
                'plungerate': self.config.active_cutter.parameters.plunge_feed_rate,
                'total_cut_depth': total_cut_depth,
                'z_safe_distance': z_safe_distance,
                'simulate': simulate
                }
            if simulate:
                parameters['pass_depth'] = simulation_z_height
                parameters['feedrate'] = simulation_feedrate
                parameters['plungerate'] = simulation_plunge_rate
                parameters['total_cut_depth'] = simulation_z_height
            return parameters

        shape_type = self.config.active_config.shape_type.lower()
        pocketing = self.config.active_config.toolpath_offset == "pocket"

        if shape_type in ["rectangle", "square"]:
            # Produce coordinate list
            y_rect = self.config.active_config.canvas_shape_dims.y
            x_rect = self.config.active_config.canvas_shape_dims.x \
                if self.config.active_config.shape_type.lower() == ShapeOptions.RECTANGLE.value \
                else self.config.active_config.canvas_shape_dims.y
            rect_coordinates = self.rectangle_coordinates(x_rect, y_rect)

            if len(rect_coordinates) != 4:
                raise Exception("Sir, rectangles have 4 sides, not %d" % len(rect_coordinates))

            # Add first point to end of coordinate list to complete the contour
            coordinates = rect_coordinates
            coordinates.append(coordinates[0])

            # Create a dictionary of operations
            length_to_cover_with_passes = 0  # Generate a single pass for roughing
            if pocketing:
                length_to_cover_with_passes = min(x_rect, y_rect) / 2  # Half the shortest edge length
            length_covered_by_finishing = self.finishing_stepover * self.finishing_passes  # Amount of length covered by finishing passes
            length_to_cover_with_roughing = length_to_cover_with_passes - length_covered_by_finishing  # Remaining length to be covered by roughing passes

            finishing_stepovers = calculate_stepovers(length_covered_by_finishing, 0, self.finishing_stepover)[1:]
            roughing_stepovers = calculate_stepovers(length_to_cover_with_roughing, finishing_stepovers[0], self.config.active_cutter.dimensions.diameter / 2)[1:]
            finishing_depths = self.calculate_pass_depths(total_cut_depth, self.finishing_stepdown)
            roughing_depths = self.calculate_pass_depths(total_cut_depth, cutting_pass_depth)

            operations = {
                "Roughing": {
                    "stepovers": roughing_stepovers,
                    "cutting_depths": roughing_depths
                },
                "Finishing": {
                    "stepovers": finishing_stepovers,
                    "cutting_depths": finishing_depths
                }
            }

            if operations["Roughing"]["stepovers"] == [] and operations["Finishing"]["stepovers"] == [0]:
                operations["Roughing"]["stepovers"] = [0]
                operations["Finishing"]["stepovers"] = []


            if simulate:
                rectangle = self.cut_rectangle(**rectangle_default_parameters(simulate=True))
                cutting_lines += rectangle
            else:
                rectangle_parameters = rectangle_default_parameters()
                # Produce instructions for each complete rectangle
                for operation_name, operation_data in operations.items():
                    # for each operation
                    for pass_depth in operation_data["cutting_depths"]:
                        # for each stepdown
                        for stepover in operation_data["stepovers"]:
                            # for each stepover
                            first_plunge = stepover == operation_data["stepovers"][0]  # First stepover
                            rectangle_parameters["z_safe_distance"] = -1 * pass_depth + stepover_z_hop_distance  # Raise tool by the stepover distance for optimisation if not the last stepover

                            if self.config.active_cutter.dimensions.diameter:
                                rectangle_parameters["tool_diameter"] = self.config.active_cutter.dimensions.diameter + (stepover * 2)
                            else:
                                rectangle_parameters["tool_diameter"] = 0
                            rectangle_parameters["total_cut_depth"] = pass_depth
                            rectangle_parameters["pass_depth"] = pass_depth
                            rectangle_parameters["pass_type"] = operation_name + " pass"
                            rectangle_parameters["first_plunge"] = first_plunge

                            rectangle = self.cut_rectangle(**rectangle_parameters)
                            rectangle = self.remove_redudant_lines(rectangle)
                            if not pocketing:
                                pass
                                rectangle = self.add_tabs_to_gcode(rectangle, total_cut_depth, tab_height, tab_width, tab_spacing, three_d_tabs=three_d_tabs)
                            cutting_lines += rectangle

        elif shape_type in ["geberit"]:

            # Read in data
            gcode_lines = self.find_and_read_gcode_file(self.source_folder_path, self.config.active_config.shape_type, self.config.active_cutter.dimensions.diameter, orientation=self.config.active_config.rotation)
            gcode_cut_depth, gcode_z_safe_distance = self.extract_cut_depth_and_z_safe_distance(gcode_lines)
            x_size, y_size, x_minus, y_minus  = self.read_in_custom_shape_dimensions(gcode_lines)

            if simulate:
                coordinates = self.rectangle_coordinates(float(x_size), float(y_size) + self.config.active_cutter.dimensions.diameter/2, float(x_minus), float(y_minus))
                coordinates.append(coordinates[0])

                # Draw a rectangle around the geberit shape
                rectangle_parameters = rectangle_default_parameters(simulate=True)
                rectangle_parameters["offset"] = "inside"
                # rectangle_parameters["tool_diameter"] = 0
                rectangle_parameters["corner_radius"] = 0

                gcode_lines = self.cut_rectangle(**rectangle_parameters)

            else:
                # Remove header info
                gcode_lines = gcode_lines[next((i for i, s in enumerate(gcode_lines) if re.search(r"T[1-9]", s)), None):]

                # Adjust feeds, speeds, and Z values
                gcode_lines = self.adjust_feeds_and_speeds(gcode_lines, self.config.active_cutter.parameters.cutting_feed_rate, self.config.active_cutter.parameters.plunge_feed_rate, self.config.active_cutter.parameters.cutting_spindle_speed)
                gcode_lines = self.replace_cut_depth_and_z_safe_distance(gcode_lines, gcode_cut_depth, gcode_z_safe_distance, "[cut depth] ", z_safe_distance)

                # Apply datum offset
                gcode_lines = self.apply_datum_offset(gcode_lines, self.config.active_config.datum_position.x, self.config.active_config.datum_position.y)

                # Apply pass depths
                pass_depths = self.calculate_pass_depths(total_cut_depth, self.config.active_config.cutting_depths.depth_per_pass)
                start_condition = next((i for i, s in enumerate(gcode_lines) if re.search(r"M3", s)), None)
                end_condition = next((i for i, s in enumerate(gcode_lines) if re.search(r"M5", s)), None)
                gcode_lines = self.repeat_for_depths(gcode_lines, pass_depths, start_condition, end_condition)

                tool_radius = self.config.active_cutter.dimensions.diameter / 2

                if geberit_partoff:
                    # Add partoff cut
                    partoff_start_coordinate = [(-1 * tool_radius) + self.config.active_config.datum_position.x,
                                                float(y_size) + tool_radius + self.config.active_config.datum_position.y]
                    partoff_end_coordinate = [tool_radius + float(x_size) + self.config.active_config.datum_position.x,
                                            tool_radius + float(y_size) + self.config.active_config.datum_position.y]
                    gcode_lines = self.add_partoff(gcode_lines, "M5", partoff_start_coordinate, partoff_end_coordinate, pass_depths, self.config.active_cutter.parameters.cutting_feed_rate, self.config.active_cutter.parameters.plunge_feed_rate, z_safe_distance)

            cutting_lines = gcode_lines

        elif shape_type in ["circle"]:
            circle_coordinates = self.rectangle_coordinates(self.config.active_config.canvas_shape_dims.d, self.config.active_config.canvas_shape_dims.d) # Circles are secretly rounded rectangles

            # Add first point to end of coordinate list to complete the contour
            coordinates = circle_coordinates
            coordinates.append(coordinates[0])

            circle_radius = self.config.active_config.canvas_shape_dims.d / 2

            # Create a dictionary of operations
            length_to_cover_with_passes = 0  # Generate a single pass for roughing
            if pocketing:
                length_to_cover_with_passes = circle_radius
            length_covered_by_finishing = self.finishing_stepover * self.finishing_passes  # Amount of length covered by finishing passes
            length_to_cover_with_roughing = length_to_cover_with_passes - length_covered_by_finishing  # Remaining length to be covered by roughing passes

            finishing_stepovers = calculate_stepovers(length_covered_by_finishing, 0, self.finishing_stepover)
            roughing_stepovers = calculate_stepovers(length_to_cover_with_roughing, finishing_stepovers[0], self.config.active_cutter.dimensions.diameter / 2)[1:]
            finishing_depths = self.calculate_pass_depths(total_cut_depth, self.finishing_stepdown)
            roughing_depths = self.calculate_pass_depths(total_cut_depth, cutting_pass_depth)

            if finishing_stepovers:
                roughing_stepovers.append(finishing_stepovers[0])
                finishing_stepovers = finishing_stepovers[1:]

            operations = {
                "Roughing": {
                    "stepovers": roughing_stepovers,
                    "cutting_depths": roughing_depths
                },
                "Finishing": {
                    "stepovers": finishing_stepovers,
                    "cutting_depths": finishing_depths
                }
            }

            circle_parameters = circle_default_parameters(simulate=simulate)

            circle_parameters['datum_x'] = -1 * circle_radius
            circle_parameters['datum_y'] = -1 * circle_radius

            if simulate:
                circle_parameters["pass_depth"] = simulation_z_height
                circle_parameters["total_cut_depth"] = simulation_z_height
                circle_parameters["feedrate"] = simulation_feedrate
                circle_parameters["plungerate"] = simulation_plunge_rate
                circle = self.cut_rectangle(**circle_parameters)
                cutting_lines += circle

            else:
                for operation_name, operation_data in operations.items():
                    # for each operation
                    for pass_depth in operation_data["cutting_depths"]:
                        # for each stepdown
                        for stepover in operation_data["stepovers"]:
                            # for each stepover
                            first_plunge = stepover == operation_data["stepovers"][0]  # First stepover
                            circle_parameters["z_safe_distance"] = -1 * pass_depth + stepover_z_hop_distance  # Raise tool by the stepover distance for optimisation if not the last stepover

                            if self.config.active_cutter.dimensions.diameter:
                                circle_parameters["tool_diameter"] = self.config.active_cutter.dimensions.diameter + (stepover * 2)
                            else:
                                circle_parameters["tool_diameter"] = 0

                            circle_parameters["total_cut_depth"] = pass_depth
                            circle_parameters["pass_depth"] = pass_depth
                            circle_parameters["pass_type"] = operation_name + " pass"
                            circle_parameters["first_plunge"] = first_plunge

                            circle = self.cut_rectangle(**circle_parameters)
                            if not pocketing:
                                circle = self.remove_redudant_lines(circle)
                                circle = self.add_tabs_to_gcode(circle, total_cut_depth, tab_height, tab_width, tab_spacing, three_d_tabs=three_d_tabs)
                            cutting_lines += circle

        elif shape_type in ["line"]:
            cutting_lines = self.cut_line(**line_default_parameters(simulate=simulate))

        else:
            raise Exception("Shape type: '%s' not supported" % self.config.active_config.shape_type)

        # GCODE FILE STRUCTURE
        file_structure_1_shapes = ["rectangle", "square", "circle", "line"]

        if simulate:
            cutting_lines.insert(0, "G0 X0 Y0")
            cutting_lines.insert(0, "G90")
            cutting_lines.append("G0 X{} Y{}".format(-self.m.laser_offset_x_value, -self.m.laser_offset_y_value))
            self.m.s.run_skeleton_buffer_stuffer(cutting_lines)

        else:
            if self.config.active_config.shape_type in file_structure_1_shapes:
                output = "(%s)\nG90\nG17\nM3 S%d\nG0 %s\n\n%s(End)\nG0 Z%d\nM5\n" % (
                    filename, self.config.active_cutter.parameters.cutting_spindle_speed, safe_start_position, ''.join(cutting_lines), z_safe_distance)
            else:
                output = "(%s)\nG90\nG17\nM3 S%d\nG0 %s\n" % (filename, self.config.active_cutter.parameters.cutting_spindle_speed, safe_start_position)
                output += "\n".join(cutting_lines)

            with open(output_path, 'w+') as out_file:
                out_file.write(output)  # Use write() to write the entire output as a single string since we use \n in the string

                Logger.info("%s written" % filename)
                return output_path  # return path to the file
