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


DONE >>>> ?? need confirmation:
Circles:
    # Improve the capture of circle mode G2 or G3
            # many assumptions built in here:
            # G2X, G2 X, G3X, G3 X etc Y, Z...
            # see line_start in funciton: 
            # check_circle_mode

Also: 
Distinguish effectively between modal (changing mode within gcode) and
non-modal (just detailing more coordinates)
As per Ed's original code

'''
from distutils.errors import UnknownFileError

class BoundingBox():
    arc_line_type = ['G2X',  'G3X',  # many assumptions built in here...
                     'G2 X', 'G3 X',
                     'G2Y',  'G3Y',
                     'G2 Y', 'G3 Y',
                     'G2Z',  'G3Z',
                     'G2 Z', 'G3 Z']
 
    line_modal_type = ['G0X',  'G1X',  # many assumptions built in here...
                       'G0 X', 'G1 X',
                       'G0Y',  'G1Y',
                       'G0 Y', 'G1 Y',
                       'G0Z',  'G1Z',
                       'G0 Z', 'G1 Z']

    circle_lines = [""]
    range_x = [109, 1099] 
    range_y = [109, 1099] 
    range_z = [109, 1099]
    range_g = [109, 1099]

    def __init__(self):
        pass

    def check_circle_mode(self, input_line):
        isarc = 0
        if input_line.startswith(tuple(self.arc_line_type)): # then arc
            isarc = 1
            # print(input_line) # don't this this anymore, useful to see what ARCs are found
        return isarc

    def check_other_type(self, input_line):
        lineartype = ''
        if input_line.startswith(tuple(self.line_modal_type)):  # then linear modal
            lineartype = 'linear modal'
            # print(input_line) # don't this this anymore, useful to see what is found
        else:
            lineartype = 'linear non-modal'  # ASSUMPTIONS HERE:
        return lineartype

    def add_circle_mode(self, circle_line):
        self.circle_lines.append(circle_line)
 
    def set_job_envelope(self, gcode_file_path):
        print('WORKING @@: {}'.format(gcode_file_path))
        x_values = []
        y_values = []
        z_values = []
        g_values = []
        # use sample data for now to prove a point 
        # these 'get through' but datum_x is still zero
        sample_only_value = 1.1
        x_values.append(sample_only_value)
        y_values.append(sample_only_value+0.1)
        z_values.append(sample_only_value+0.2)
        g_values.append(sample_only_value+0.3)

        values_list_xyzg = [x_values, y_values, z_values, g_values]
        includes_arcs = 0
        
        
        count_linear_gcodelines = 0
        count_arc_gcodelines = 0

        gcode_file = open(gcode_file_path,'r')
        for line in gcode_file:
            blocks = line.strip().split(" ")
            
            
            for part in blocks:
                

                """
                NOTE: part is a complex thing, 
                      it's just a line of gcode, but it can come in many forms
                
                A) Going to parcel out each 'type of form' into a separate function
                B) Also a function for 'what type of form' is the part

                """
                gcode_linetype = self.determine_part_type(part)
                if gcode_linetype == 'arc':
                    # arc fasion:
                    count_arc_gcodelines += 1
                    # values_list_xyzg = [0]
                elif gcode_linetype.startswith(('linear')):
                    # linear fasion
                    count_linear_gcodelines += 1 
                    # values_list_xyzg = [0]

                
                dothis = 0
                if dothis == 1:
                    try:
                        print('APPENDING to x,y,z & g _values: {},  {}'.format(
                            part, part[1]))
                        if part.startswith(('G0')) or part.startswith(('G1')):
                            pass
                        elif part.startswith(('X')) or part.startswith(('Y')) or part.startswith(('Z')):
                            if part.startswith(('X')) or part[1] == 'X': 
                                x_values.append(float(part[1:]))
                                print('APPENDING to x: {}', format(float(part[1:])))
                            if part.startswith(('Y')): 
                                y_values.append(float(part[1:]))
                            if part.startswith(('Z')): 
                                z_values.append(float(part[1:]))
                        elif part.startswith('G2') or part.startswith('G3'): 
                            ### IDENTIFY ARCS OR CIRCLES with G2 or G3
                            includes_arcs = self.check_circle_mode(line)

                        if includes_arcs: # WAS... part.startswith(('G')):
                            # need to sort through G values, as multi-facted line...
                            # the approach used for x, y, z above won't operate:
                            check = self.sort_arc_part(part)
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
            
            # this is where the range_x, range_etc are set?

            dothat = 0
            if dothat == 1:
                    try:  
                        self.range_x[0], self.range_x[1] = min(x_values), max(x_values)
                    except ValueError as e:
                        print('x HERE ERROR, ERROR!! ValueError: {}'.format(e))
                    try:
                        self.range_y[0], self.range_y[1] = min(y_values), max(y_values)
                    except ValueError as e:
                        print('y HERE ERROR, ERROR!! ValueError: {}'.format(e))
                    try:
                        self.range_z[0], self.range_z[1] = min(z_values), max(z_values)
                    except ValueError as e:
                        print('z HERE ERROR, ERROR!! ValueError: {}'.format(e))
                    try:
                        self.range_g[0], self.range_g[1] = min(g_values), max(g_values)
                    except ValueError as e:
                        print('g HERE ERROR, ERROR!! ValueError: {}'.format(e))
                        
                    print("""job_env_w_arc.set_job_envelope: 
                                range_x: {} 
                                range_y: {} 
                                range_z: {} 
                                range_g: {} """.format(self.range_x, self.range_y, 
                                                        self.range_z, self.range_g))
        try:
            gcode_file.close()
        except UnknownFileError:
            print(">>>>  Error: " + UnknownFileError)

        print('arc fasion: {}, linear fasion: {}'.format(count_arc_gcodelines, count_linear_gcodelines))


    def sort_arc_part(self, glinepart):
        '''
        EXAMPLE: going through lines like this: 
            G2X747.643Y448.226I180.000J0.000
            G2X927.643Y268.226I0.000J-180.000F3000.0
        and trying to sort out the ARC data and split it out. bit complex.
        '''
        f = [77.0, 88.0, 99.0]
        # print('NOT ENTERING G-PART... sort_arc_part: {glinepart}')
        return f

    def determine_part_type(self, parttocheck):
        # modal or non-modal
        part_type = ''
        if self.check_circle_mode(parttocheck):
            part_type = 'arc'
        else:
            part_type = self.check_other_type(parttocheck)
        return part_type