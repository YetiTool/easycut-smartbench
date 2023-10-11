import re, svgwrite

class GeometryToGcode(object):

    def __init__(self, **kwargs):
        pass

    def create_empty_svg(self, svg_output_filepath, svg_width, svg_height, editor_height, editor_width):
        # Viewbox can be set to the container size, so that positions can then be defined in pixels rather than relative to actual size of the SVG
        # The height and width are switched - this is necessary so that everything is drawn in full size but out of bounds, which is fixed by a reflection later on
        return svgwrite.Drawing(filename=svg_output_filepath, size=(svg_width,svg_height), viewBox='0 0 %s %s' % (editor_height, editor_width))

    def get_global_transformation(self, editor_height):
        # The long side has to be drawn parallel to the y axis - to solve this, this matrix transformation performs a reflection in the line y=x
        # This means that the long side can be drawn parallel to the x axis, directly from the kivy coords, instead of figuring out how to switch all the x/y coords
        transformation = "matrix(0 1 1 0 0 0)"
        # Additionally, when an object is drawn, a scaling and translation is applied, which vertically flips the svg
        # This is needed because kivy measures Y coords from the opposite end of the screen and draws stuff upside down
        transformation += " scale(1,-1) translate(0,%s)" % -editor_height
        return transformation

    def create_geberit_panel(self, dwg, editor_height, panel_pos, panel_centre, panel_rotation, panel_width, panel_height):
        transformation = self.get_global_transformation(editor_height)

        # Now rotate around the centre of the panel
        transformation += " rotate(%s,%s,%s)" % (panel_rotation, panel_centre[0], panel_centre[1])

        # If the panel is turned sideways
        if int(panel_rotation) % 180 != 0:
            # Then rotation will mess up its position so align centre first
            # It is important to note that this has to be added after the rotation, because transformations are performed right to left
            transformation += " translate(%s,%s)" % (panel_width/2, -panel_height/4)

        panel_size = (panel_width, panel_height)

        # Create rectangle for panel background
        dwg.add(dwg.rect(panel_pos, panel_size, fill='white', stroke='black', transform=transformation))

        # Set up objects for the detail of the panel as relative to rectangle position and size
        # The same transform can be used as the rectangle transform as it is done relative to the centre of the panel
        big_circle_centre = (panel_pos[0] + (panel_width / 2), panel_pos[1] + (panel_height / 4))
        big_circle_radius = panel_height / 10
        dwg.add(dwg.circle(big_circle_centre, big_circle_radius, fill='white', stroke='black', transform=transformation))

        small_circle_centre = (panel_pos[0] + (panel_width / 2), panel_pos[1] + (panel_height * 0.45))
        small_circle_radius = panel_height / 40
        dwg.add(dwg.circle(small_circle_centre, small_circle_radius, fill='white', stroke='black', transform=transformation))

        small_rect_pos = (panel_pos[0] + (panel_width / 4), panel_pos[1] + (panel_height * 0.78))
        small_rect_size = (panel_width / 2, panel_width / 4)
        dwg.add(dwg.rect(small_rect_pos, small_rect_size, fill='white', stroke='black', transform=transformation))

        rounded_rect_size = (panel_width / 6, panel_width / 16)
        roundedness = rounded_rect_size[0] / 10

        rounded_rect_left_pos = (panel_pos[0] + (panel_width * 0.18), panel_pos[1] + (panel_height * 0.37))
        dwg.add(dwg.rect(rounded_rect_left_pos, rounded_rect_size, roundedness, roundedness, fill='white', stroke='black', transform=transformation))

        rounded_rect_right_pos = (panel_pos[0] + (panel_width * 0.82) - rounded_rect_size[0], panel_pos[1] + (panel_height * 0.37))
        dwg.add(dwg.rect(rounded_rect_right_pos, rounded_rect_size, roundedness, roundedness, fill='white', stroke='black', transform=transformation))

    def post_process_gcode(self, raw_gcode):

        def map_gcodes(line):
            # Stop turning off spindle throughout file by deleting all M5 commands
            if 'M5' in line:
                line = line.replace('M5', '')

            # This rounds every decimal to 2dp
            # The regex matches all decimals with 3+dp, then the lambda function rounds it by casting to 2dp float
            line = re.sub(r"\d+\.\d{3,}", lambda x: "{:.2f}".format(float(x.group())), line)

            return line

        processed_gcode = map(map_gcodes, raw_gcode)
        # Then turn spindle off at the end
        processed_gcode.append('M5')

        return processed_gcode