import math
from collections import OrderedDict


class TabUtilities:
    def __init__(self, config):
        """
        Initialize TabUtilities with a configuration object.

        config: Configuration object containing profiles and cutting parameters.
        """
        self.config = config
        self.arc_args = {}

    def add_tabs_to_gcode(self, gcode_lines, total_cut_depth, tab_height, tab_width, base_tab_spacing, tool_diameter, three_d_tabs=False):
        """
        Add tabs to a list of gcode lines.

        gcode_lines: List[str]. The list of gcode lines to modify.
        total_cut_depth: float. The total depth of the cut.
        tab_height: float. The height of the tabs.
        tab_width: float. The width of the tabs.
        base_tab_spacing: float. The spacing between the tabs.
        tool_diameter: float. The diameter of the tool.
        three_d_tabs: bool. Whether to cut the tabs in 3D.

        Returns the modified gcode as a list of strings.
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

                if linear_distance_moved >= base_tab_spacing and line.startswith(('G0', 'G1')):
                    tabs_added = True
                    modified_gcode.extend(
                        self.add_straight_tabs(self, tool_diameter, xy_feed, linear_distance_moved, base_tab_spacing, tab_width,
                                               tab_height,
                                               previous_x_pos, previous_y_pos, g1_last_x, g1_last_y, x_delta, y_delta,
                                               current_z, tab_top_z, line, three_d_tabs))

                if line.startswith('G2') or line.startswith('G3'):
                    tabs_added = True
                    modified_gcode.extend(
                        self.add_arc_tabs(xy_feed, parts, line, last_x, last_y, current_x, current_y,
                                          base_tab_spacing,
                                          tab_width, current_z, tab_top_z, tool_diameter, three_d_tabs))

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
    def add_straight_tabs(self, tool_diameter, xy_feed, linear_distance_moved, base_tab_spacing, tab_width, tab_height, previous_x_pos,
                          previous_y_pos, last_x, last_y, x_delta, y_delta, current_z, tab_top_z, line, three_d_tabs):
        tab_spacing = self.adjust_tab_spacing(base_tab_spacing, linear_distance_moved)
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
                    tab_gcode = self.add_tab(self, "G1", ((tab['start_x'], tab['start_y']), (tab['end_x'], tab['end_y'])), current_z, tab_cut_height, xy_feed, tool_diameter, three_d_tabs)
                    modified_gcode.extend(tab_gcode)

        return modified_gcode

    def add_arc_tabs(self, xy_feed, parts, line, last_x, last_y, current_x, current_y, base_tab_spacing, tab_width,
                     current_z, tab_top_z, tool_diameter, three_d_tabs):
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

            tab_spacing = self.adjust_tab_spacing(base_tab_spacing, arc_length)

            if arc_length >= tab_spacing:
                number_of_tabs = int(arc_length / (tab_spacing + tab_width))
                tab_inset_distance = arc_length - ((tab_width * number_of_tabs) + tab_spacing * (number_of_tabs - 1))
                tab_inset_distance /= 2

                self.arc_args = {
                    'self': self,
                    'x1': last_x,
                    'y1': last_y,
                    'x2': current_x,
                    'y2': current_y,
                    'r': radius,
                    'd': 0,
                    'clockwise': arc_command == 'G2'
                }

                for tab_index in range(number_of_tabs):
                    reverse_index = number_of_tabs - 1 - tab_index
                    total_tab_width = tab_width * (reverse_index + 1)
                    total_base_tab_spacing = tab_spacing * reverse_index

                    tab_start_distance = arc_length - (total_tab_width + total_base_tab_spacing + tab_inset_distance)
                    tab_end_distance = arc_length - (
                                total_tab_width - tab_width + total_base_tab_spacing + tab_inset_distance)

                    tab_cut_height = current_z if current_z > tab_top_z else tab_top_z

                    modified_gcode += self.add_tab(self, arc_command, (tab_start_distance, tab_end_distance), current_z,
                                                   tab_cut_height, xy_feed, tool_diameter, three_d_tabs, radius)

        return modified_gcode

    @staticmethod
    def calculate_arc_point(self, x1, y1, x2, y2, r, d, clockwise):
        """
        Calculate the coordinates of a point on an arc.

        x1, y1: The coordinates of the starting point of the arc.
        x2, y2: The coordinates of the ending point of the arc.
        r: The radius of the arc.
        d: The distance from the starting point to the point of interest.
        clockwise: The direction of the arc.

        Returns the coordinates of the point.
        """

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

        x1, y1: The coordinates of the starting point of the arc.
        x2, y2: The coordinates of the ending point of the arc.
        clockwise: The direction of the arc.

        Returns the coordinates of the center of the circle.
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

    @staticmethod
    def add_tab(self, command, boundaries, current_z, tab_cut_height, xy_feed, tool_diameter, three_d, radius=None):
        """
        Produce gcode to insert a tab at a given location on a straight line or arc.

        command: The gcode command to use. (G1, G2, G3)
        boundaries: The start and end points of the line or arc.
        current_z: The current Z position.
        tab_cut_height: The height of the tab.
        xy_feed: The feedrate to use.
        tool_diameter: The diameter of the tool.
        three_d: Whether to cut the tab in 3D.
        radius: The radius of the arc. (Only for arcs)
        """
        z_param = ""
        radius = round(radius, 2) if radius else None
        radius_param = " R{}".format(radius) if radius else ""
        gcode = []
        tool_radius = tool_diameter / 2

        if command in ['G2', 'G3']:
            start_distance, end_distance = boundaries

            start_distance = start_distance - tool_radius
            end_distance = end_distance + tool_radius

            self.arc_args['d'] = start_distance
            start_x, start_y = self.calculate_arc_point(**self.arc_args)

            self.arc_args['d'] = end_distance
            end_x, end_y = self.calculate_arc_point(**self.arc_args)

            centre_distance = (start_distance + end_distance) / 2

            start_x = round(start_x, 2)
            start_y = round(start_y, 2)
            end_x = round(end_x, 2)
            end_y = round(end_y, 2)
            current_z = round(current_z, 2)
            tab_cut_height = round(tab_cut_height, 2)

            start_point = (start_x, start_y, current_z)
            end_point = (end_x, end_y, current_z)

            if three_d:
                self.arc_args['d'] = centre_distance - tool_radius
                x, y = self.calculate_arc_point(**self.arc_args)
                second_point = x, y, tab_cut_height
                self.arc_args['d'] = centre_distance + tool_radius
                x, y = self.calculate_arc_point(**self.arc_args)
                third_point = x, y, tab_cut_height
            else:
                second_point = (start_x, start_y, tab_cut_height)
                third_point = (end_x, end_y, tab_cut_height)

        elif command in ['G1']:
            start_point, end_point = boundaries

            x_move = abs(end_point[0] - start_point[0]) > abs(end_point[1] - start_point[1])
            x_move_positive = end_point[0] - start_point[0] > 0
            y_move_positive = end_point[1] - start_point[1] > 0

            if x_move:
                polariser = 1 if x_move_positive else -1
                x_compensation = tool_radius * polariser
                y_compensation = 0
            else:
                polariser = 1 if y_move_positive else -1
                x_compensation = 0
                y_compensation = tool_radius * polariser

            start_point = start_point[0] - x_compensation, start_point[1] - y_compensation, current_z
            end_point = end_point[0] + x_compensation, end_point[1] + y_compensation, current_z

            if three_d:
                tab_centre_x = (start_point[0] + end_point[0]) / 2
                tab_centre_y = (start_point[1] + end_point[1]) / 2

                second_point = tab_centre_x - x_compensation, tab_centre_y - y_compensation, tab_cut_height
                third_point = tab_centre_x + x_compensation, tab_centre_y + y_compensation, tab_cut_height
            else:
                second_point = start_point[0] - x_compensation, start_point[1] - y_compensation, tab_cut_height
                third_point = end_point[0] + x_compensation, end_point[1] + y_compensation, tab_cut_height

        else:
            raise ValueError("Invalid command: {}".format(command))

        points = [start_point, second_point, third_point, end_point]

        previous_z = current_z

        for point in points:
            x, y, z = point
            x, y, z = round(x, 2), round(y, 2), round(z, 2)

            feed_param = " F{}".format(int(xy_feed))

            if z != previous_z:
                # Move in Z
                z_param = " Z{}".format(z)

            previous_z = z

            gcode.append("{} X{} Y{}{}{}{}\n".format(command, x, y, z_param, radius_param, feed_param))

        return gcode

    @staticmethod
    def adjust_tab_spacing(base_tab_spacing, movement_distance):
        """
        Adjust tab spacing based on the distance moved to avoid having loads of tabs on large segments.
        """

        k = 1  # adjustment factor

        return base_tab_spacing * k * movement_distance ** 0.5

