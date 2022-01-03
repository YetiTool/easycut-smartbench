'''
Created on 3 Feb 2018
@author: Ed (original job_envelope)
@author: hsth
@author hugh.harford@yetitool.com
@author hugh.harford@poscoconsulting.com
TODO: This all looks a bit lonely. 
Reintegrate back with the other UI widgets e.g. widget_virtual_bed?

TODO (hsth):
Deal with circles in set_job_envelope
The simple min-max and "grab line if starts with X or Y" 
isn't going to cut it


Circles:
    # Improve the capture of circle mode G2 or G3
            # many assumptions built in here:
            # G2X, G2 X, G3X, G3 X etc Y, Z...
            # see line_start in funciton: 
            # check_circle_mode


'''
from distutils.errors import UnknownFileError

class BoundingBox():

    circle_lines = [""]
    range_x = [0,0] 
    range_y = [0,0] 
    range_z = [0,0]


    def __init__(self):
        pass

    def check_circle_mode(self, input_line):
        isacircle = 0
        
        line_start = ['G2X', 'G3X', 
                      'G2 X', 'G3 X',
                      'G2Y', 'G3Y',
                      'G2 Y', 'G3 Y',
                      'G2Z', 'G3Z',
                      'G2 Z', 'G3 Z']
        
            # many assumptions built in here...
        
        if input_line.startswith(tuple(line_start)):
            # then basic X-axis described circle
            isacircle = 1
            print(input_line)
        return isacircle

    def add_circle_mode(self, circle_line):
        self.circle_lines.append(circle_line)
 
    def set_job_envelope(self, gcode_file_path):
        
        x_values = []
        y_values = []
        z_values = []
        
        includes_arcs = 0
        
        
        file_in_use = open(gcode_file_path,'r')
        for line in file_in_use:
            blocks = line.strip().split(" ")
                     
            for part in blocks:
                try:
                    if "X0.000Y0.000" in part:
                        # skip any line at this point (bit risky)
                        # as assuming datum is actual datum
                        # and not part of cut workflow
                        # FOR DEBUG ### print("DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM ")
                        continue
                    else:
                        if part.startswith(('X')): x_values.append(float(part[1:]))
                        if part.startswith(('Y')): y_values.append(float(part[1:]))
                        if part.startswith(('Z')): z_values.append(float(part[1:]))
                    
                        ### IDENTIFY ARCS OR CIRCLES with G2 or G3
                        if part.startswith('G2') or part.startswith('G3'): 
                            
                            includes_arcs = self.check_circle_mode(line)
                            print("includes_arcs: {}".format(includes_arcs))
                        
                        else:
                            includes_arcs = 0
                            


                except TypeError:
                    print( "TypeError TypeError HERE HERE HERE HERE HERE HERE HERE ")
                except ValueError:
                    print( "Envelope calculator: skipped '" + part + "'")

        try:  
            
            # the range CANNOT be set by the simple MIN()
            # as the 0,0,0 datum will therefore always be one corner...
            if "X0.000Y0.000" in part:
                # don't do anything here, 
                # just don't add to range_x and range_y
                print("DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM DATUM ")
                # pass # knowingly, trying to do nothing here
            else:
            
                self.range_x[0], self.range_x[1] = min(x_values), max(x_values)
                self.range_y[0], self.range_y[1] = min(y_values), max(y_values)
                self.range_z[0], self.range_z[1] = min(z_values), max(z_values)

        except ValueError:
            print("Error found, likely empty: {}".format(ValueError))

        try:
            file_in_use.close()
        except UnknownFileError:
            print(">>>>  Error: " + UnknownFileError)
        
