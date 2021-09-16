'''
Created on 2 Aug 2021
@author: Dennis
Module used to keep track of information about the current job
'''
import sys

def remove_newlines(gcode_line):
    if gcode_line in ['\n', '\r', '\r\n']:
        return ' '
    gcode_line = gcode_line.strip('\n')
    gcode_line = gcode_line.strip('\r')
    return gcode_line

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
    job_name = ''
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
    actual_runtime = ''
    total_time = ''
    screen_to_return_to_after_job = 'home'
    screen_to_return_to_after_cancel = 'home'
    percent_thru_job = 0

    def reset_values(self):
        self.filename = ''
        self.job_name = ''
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
        self.actual_runtime = ''
        self.total_time = ''
        self.percent_thru_job = 0
        self.screen_to_return_to_after_job = 'home'
        self.screen_to_return_to_after_cancel = 'home'

    def set_job_filename(self, job_path_and_name):

        self.filename = job_path_and_name

        if sys.platform == 'win32':
            self.job_name = self.filename.split("\\")[-1]
        else:
            self.job_name = self.filename.split("/")[-1]

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

        except:
            # In case no metadata in file
            self.comments_list = filter(filter_for_comments, self.job_gcode_raw)

