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
    range_x = [99,99] 
    range_y = [99,99] 
    range_z = [99,99]

    def __init__(self):
        pass

    def check_circle_mode(self, input_line):
        isacircle = 0
        line_start = ['G2X', 'G3X',  # many assumptions built in here...
                      'G2 X', 'G3 X',
                      'G2Y', 'G3Y',
                      'G2 Y', 'G3 Y',
                      'G2Z', 'G3Z',
                      'G2 Z', 'G3 Z']
        if input_line.startswith(tuple(line_start)): # then basic X-axis arc
            isacircle = 1
            print(input_line)
        return isacircle

    def add_circle_mode(self, circle_line):
        self.circle_lines.append(circle_line)
 
    def set_job_envelope(self, gcode_file_path):
        x_values = []
        y_values = []
        z_values = []
        g_values = []
        # use sample data for now to prove a point
        sample_only_value = 1.1
        x_values.append(sample_only_value)
        y_values.append(sample_only_value)
        z_values.append(sample_only_value)

        includes_arcs = 0
        
        gcode_file = open(gcode_file_path,'r')
        for line in gcode_file:
            blocks = line.strip().split(" ")
            for part in blocks:
                try:
                    if part.startswith(('X')): 
                        x_values.append(float(part[1:]))
                        # print('APPENDING to x')
                    if part.startswith(('Y')): 
                        y_values.append(float(part[1:]))
                    if part.startswith(('Z')): 
                        z_values.append(float(part[1:]))

                    ### IDENTIFY ARCS OR CIRCLES with G2 or G3
                    if part.startswith('G2') or part.startswith('G3'): 
                        includes_arcs = self.check_circle_mode(line)

                    if includes_arcs: # WAS... part.startswith(('G')):
                        # need to sort through G values, as multi-facted line...
                        # the approach used for x, y, z above won't operate:
                        check = self.sortarclinepart(part)
                        if type(check) == list and type(check[0]) == float: 
                            # print('going to to APPEND to g {}'.format(part))
                            g_values.append(check)
                        else:
                            pass
                    includes_arcs = 0
                        
                except TypeError as e:
                    print(
                        'TypeError: {} HERE '.format(e))
                except ValueError as e:
                    print( ' ValueError: {}: skipped {}'.format(e, part))
        # HERE IS THE (or at least one) BROKEN BIT, BROKEN BIT, BROKEN BIT
            # there should be no instances of "X0.000Y0.000" included
        dothis = 0
        if dothis == 1:
            try:  
                self.range_x[0], self.range_x[1] = min(x_values), max(x_values)
            except ValueError as e:
                print('xxx HERE ERROR, ERROR!! ValueError: {}'.format(e))
            try:
                self.range_y[0], self.range_y[1] = min(y_values), max(y_values)
            except ValueError as e:
                print('yyy HERE ERROR, ERROR!! ValueError: {}'.format(e))
            try:
                self.range_z[0], self.range_z[1] = min(z_values), max(z_values)
            except ValueError as e:
                print('zzz HERE ERROR, ERROR!! ValueError: {}'.format(e))

        try:
            gcode_file.close()
        except UnknownFileError:
            print(">>>>  Error: " + UnknownFileError)

    def sortarclinepart(self, glinepart):
        '''
        EXAMPLE: going through lines like this: 
            G2X747.643Y448.226I180.000J0.000
            G2X927.643Y268.226I0.000J-180.000F3000.0
        and trying to sort out the ARC data and split it out. bit complex.
        '''
        f = [1.0, 2.0, 3.0]
        # print('NOT ENTERING G-PART... sortarclinepart: {glinepart}')
        return f
