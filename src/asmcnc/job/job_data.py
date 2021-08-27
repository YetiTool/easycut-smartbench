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

def filter_out_brackets(character):
    if character in ['(',')']:
        return False
    return True

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
    metadata_dict = {}

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
        self.metadata_dict = {}

    def generate_job_data(self, raw_gcode):

        self.job_gcode_raw = map(remove_newlines, raw_gcode)

        try:
            metadata_start_index = self.job_gcode_raw.index('(YetiTool SmartBench MES-Data)')
            metadata_end_index = self.job_gcode_raw.index('(End of YetiTool SmartBench MES-Data)')
            metadata = self.job_gcode_raw[metadata_start_index + 1:metadata_end_index]

            metadata = [line.strip('()') for line in metadata]
            metadata = [line.split(':', 1) for line in metadata]
            self.metadata_dict = dict(metadata)

            # Metadata looks like comments so needs to be removed
            gcode_without_metadata = self.job_gcode_raw[0:metadata_start_index] + self.job_gcode_raw[metadata_end_index + 1:-1]
            self.comments_list = filter(filter_for_comments, gcode_without_metadata)

        except Exception as e:
            self.metadata_dict['error'] = str('(YetiTool SmartBench MES-Data)' == self.job_gcode_raw[0])
            self.metadata_dict['line_zero'] = self.job_gcode_raw[0]

            # In case no metadata in file
            self.comments_list = filter(filter_for_comments, self.job_gcode_raw)

