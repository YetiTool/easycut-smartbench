import math
from collections import OrderedDict


class Tabs(object):
    def __init__(self, config):
        self.config = config

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
        xy_feed = self.config.active_profile.cutting_parameters.max_feedrate
        z_feed = self.config.active_profile.cutting_parameters.plungerate
        last_x = 0
        last_y = 0
        g1_last_x = 0
        g1_last_y = 0
        x_delta = 0
        y_delta = 0
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
                    modified_gcode.extend(
                        self.add_straight_tabs(xy_feed, z_feed, linear_distance_moved, tab_spacing, tab_width,
                                               tab_height,
                                               previous_x_pos, previous_y_pos, g1_last_x, g1_last_y, x_delta, y_delta,
                                               current_z, tab_top_z, line, three_d_tabs))

                if line.startswith('G2') or line.startswith('G3'):
                    tabs_added = True
                    modified_gcode.extend(
                        self.add_arc_tabs(xy_feed, z_feed, parts, line, last_x, last_y, current_x, current_y,
                                          tab_spacing,
                                          tab_width, current_z, tab_top_z, three_d_tabs))

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

    @staticmethod
    def add_straight_tabs(xy_feed, z_feed, linear_distance_moved, tab_spacing, tab_width, tab_height, previous_x_pos,
                          previous_y_pos, last_x, last_y, x_delta, y_delta, current_z, tab_top_z, line, three_d_tabs):
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

    def add_arc_tabs(self, xy_feed, z_feed, parts, line, last_x, last_y, current_x, current_y, tab_spacing, tab_width,
                     current_z, tab_top_z, three_d_tabs):
        modified_gcode = []
        r_value = None
        arc_command = None
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
                    tab_end_distance = arc_length - (
                            (tab_spacing * i) + (tab_width * i) + tab_width + tab_inset_distance)
                    tab_start_x, tab_start_y = self.calculate_arc_point(self, last_x, last_y, current_x, current_y, radius,
                                                                        tab_start_distance,
                                                                        clockwise=arc_command == 'G3')
                    tab_end_x, tab_end_y = self.calculate_arc_point(self, last_x, last_y, current_x, current_y, radius,
                                                                    tab_end_distance, clockwise=arc_command == 'G3')
                    tab_centre_x, tab_centre_y = self.calculate_arc_point(self, last_x, last_y, current_x, current_y, radius,
                                                                          tab_start_distance - tab_width / 2,
                                                                          clockwise=arc_command == 'G3')

                    tab_cut_height = current_z if current_z > tab_top_z else tab_top_z

                    if three_d_tabs:
                        modified_gcode.append(
                            '{} X{} Y{} R{} F{}\n'.format(arc_command, round(tab_start_x, 2), round(tab_start_y, 2),
                                                          radius,
                                                          xy_feed))
                        modified_gcode.append(
                            '{} X{} Y{} Z{} R{}\n'.format(arc_command, round(tab_centre_x, 2), round(tab_centre_y, 2),
                                                          tab_cut_height, radius))
                        modified_gcode.append(
                            '{} X{} Y{} Z{} R{}\n'.format(arc_command, round(tab_end_x, 2), round(tab_end_y, 2),
                                                          current_z,
                                                          radius))
                    else:
                        modified_gcode.append(
                            '{} X{} Y{} R{} F{}\n'.format(arc_command, round(tab_start_x, 2), round(tab_start_y, 2),
                                                          radius,
                                                          xy_feed))
                        modified_gcode.append('G1 Z{} F{}\n'.format(tab_cut_height, z_feed))
                        modified_gcode.append(
                            '{} X{} Y{} R{} F{}\n'.format(arc_command, round(tab_end_x, 2), round(tab_end_y, 2), radius,
                                                          xy_feed))
                        modified_gcode.append('G1 Z{} F{}\n'.format(current_z, z_feed))

        return modified_gcode

    @staticmethod
    def calculate_arc_point(self, x1, y1, x2, y2, r, d, clockwise):
        # Calculate the center of the circle (midpoint of start and end)

        cx, cy = self.find_arc_center(x1, y1, x2, y2, clockwise)

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

        return round(new_x, 2), round(new_y, 2)

    @staticmethod
    def find_arc_center(x1, y1, x2, y2, clockwise):
        """
        Find the center of the circle that the arc is part of.
        Works only for 90 degree arcs.
        """

        x_delta_positive = x2 - x1 > 0
        y_delta_positive = y2 - y1 > 0

        same_polarity = x_delta_positive == y_delta_positive

        x_use_start = not same_polarity
        y_use_start = same_polarity

        if not clockwise:
            x_use_start = not x_use_start
            y_use_start = not y_use_start

        x = x1 if x_use_start else x2
        y = y1 if y_use_start else y2

        return x, y
