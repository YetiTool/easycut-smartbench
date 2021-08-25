'''
Created on 2 Aug 2021
@author: Dennis
Module used to keep track of information about the current job
'''

def remove_newlines(gcode_line):
    if gcode_line == '\n':
        return ' '
    return gcode_line.replace('\n', '')

def filter_for_comments(gcode_line):
    if gcode_line[0] == '(':
        return True
    return False

class JobData(object):

    filename = ''
    job_gcode = []
    job_gcode_raw = []
    job_gcode_modified = []
    job_gcode_running = []
    comments_list = []
    feedrate_max = None
    feedrate_min = None
    spindle_speed_max = None
    spindle_speed_min = None
    x_max = None
    x_min = None
    y_max = None
    y_min = None
    z_max = None
    z_min = None
    checked = False
    check_warning = ''

    def reset_values(self):
        self.filename = ''
        self.job_gcode = []
        self.job_gcode_raw = []
        self.job_gcode_modified = []
        self.job_gcode_running = []
        self.comments_list = []
        self.feedrate_max = None
        self.feedrate_min = None
        self.spindle_speed_max = None
        self.spindle_speed_min = None
        self.x_max = None
        self.x_min = None
        self.y_max = None
        self.y_min = None
        self.z_max = None
        self.z_min = None
        self.checked = False
        self.check_warning = ''

    def generate_job_data(self, raw_gcode):

        self.job_gcode_raw = map(remove_newlines, raw_gcode)

        self.comments_list = filter(filter_for_comments, self.job_gcode_raw)

