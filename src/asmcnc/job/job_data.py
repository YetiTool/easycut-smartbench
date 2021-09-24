'''
Created on 2 Aug 2021
@author: Dennis
Module used to keep track of information about the current job
'''
import sys, os, re, subprocess
from itertools import takewhile
from pipes import quote

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

    # Job identifiers
    filename = ''
    job_name = ''

    # GCode containers
    job_gcode = []
    job_gcode_raw = []
    job_gcode_modified = []
    job_gcode_running = []
    
    ## METADATA
    # job info scraped from file
    comments_list = []
    feedrate_max = None
    feedrate_min = None
    spindle_speed_max = None
    spindle_speed_min = None
    
    # boundary info
    x_max = None
    x_min = None
    y_max = None
    y_min = None
    z_max = None
    z_min = None
    
    # check info
    checked = False
    check_warning = ''
    
    # SmartTransfer metadata container
    metadata_dict = {}

    # DURING JOB
    screen_to_return_to_after_job = 'home'
    screen_to_return_to_after_cancel = 'home'
    
    percent_thru_job = 0
    
    ## END OF JOB
    
    # Time taken
    actual_runtime = ''
    total_time = ''
    
    # Production notes
    production_notes = ''


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

        self.screen_to_return_to_after_job = 'home'
        self.screen_to_return_to_after_cancel = 'home'

        self.percent_thru_job = 0

        self.actual_runtime = ''
        self.total_time = ''

        self.production_notes = ''


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

            print self.metadata_dict

            # Metadata looks like comments so needs to be removed
            gcode_without_metadata = self.job_gcode_raw[0:metadata_start_index] + self.job_gcode_raw[metadata_end_index + 1:-1]
            self.comments_list = filter(filter_for_comments, gcode_without_metadata)

        except:
            # In case no metadata in file
            self.comments_list = filter(filter_for_comments, self.job_gcode_raw)

        # TEST
        self.post_job_data_update_pre_send(True)

    def post_job_data_update_pre_send(self, successful, extra_parts_completed = 0):

        if "PartsCompletedSoFar" in self.metadata_dict:

            prev_parts_completed_so_far = int(self.metadata_dict["PartsCompletedSoFar"])

            print prev_parts_completed_so_far
            print self.metadata_dict.get('PartsPerJob', 1)

            if successful:
                self.metadata_dict["PartsCompletedSoFar"] = str(prev_parts_completed_so_far + int(self.metadata_dict.get('PartsPerJob', 1)))

            elif extra_parts_completed:
                self.metadata_dict["PartsCompletedSoFar"] = str(prev_parts_completed_so_far + int(extra_parts_completed))

            # # Update parts completed in job file
            grep_command = 'grep "' + 'PartsCompletedSoFar' + '" ' + quote(self.filename)
            line_to_replace = (os.popen(grep_command).read())
            new_line = '(PartsCompletedSoFar:' + str(self.metadata_dict.get("PartsCompletedSoFar")) + ")"
            sed_command = 'sudo sed -i "s/' + quote(line_to_replace) + '/' + quote(new_line) + '/" ' + quote(self.filename)
            os.system(sed_command)



    def post_job_data_update_post_send(self):

        self.production_notes = ''
        self.percent_thru_job = 0



