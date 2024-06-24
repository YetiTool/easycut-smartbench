'''
Created on 3 Feb 2018
@author: Ed
TODO: This all looks a bit lonely. Reintegrate back with the other UI widgets e.g. widget_virtual_bed?
'''
from asmcnc.comms.logging_system.logging_system import Logger


class BoundingBox(object):

    def __init__(self):
        
        pass
    

    range_x = [0,0] 
    range_y = [0,0] 
    range_z = [0,0] 
        
 
    def set_job_envelope(self, gcode_file_path):
        
        x_values = []
        y_values = []
        z_values = []
        file = open(gcode_file_path,'r');
        for line in file:
            blocks = line.strip().split(" ")
            for part in blocks:
                try:
                    if part.startswith(('X')): x_values.append(float(part[1:]))
                    if part.startswith(('Y')): y_values.append(float(part[1:]))
                    if part.startswith(('Z')): z_values.append(float(part[1:]))
                except:
                    Logger.exception("Envelope calculator: skipped '" + part + "'")
        self.range_x[0], self.range_x[1] = min(x_values), max(x_values)
        self.range_y[0], self.range_y[1] = min(y_values), max(y_values)
        self.range_z[0], self.range_z[1] = min(z_values), max(z_values)
        file.close()