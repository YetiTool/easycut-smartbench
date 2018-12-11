
class GcodeWriter():

    filename = None

    def write_gcode(self, filename, layers_points, bit_width, depth_increment, feedrate):
        
        self.filename = filename
        file = open(filename, "w")
        if file:
            self.new_gcode_file(file, filename)
            self.write_layers(file, layers_points, bit_width, depth_increment, feedrate)


    def new_gcode_file(self, file, filename):

        file.write("%\n(" + filename +
""")
(T1  D=3 CR=0 - ZMIN=-10 - flat end mill)
G90 G94
G17
G21

(2D Contour1)
M9
T1 M6
S5000 M3
G54
M8
"""         )


    def write_layers(self, file, layers_points, bit_width, depth_increment, feedrate):

        for layer_points in layers_points:
            pass
