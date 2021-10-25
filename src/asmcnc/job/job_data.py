'''
Created on 2 Aug 2021
@author: Dennis
Module used to keep track of information about the current job
'''
import sys, os, re
from datetime import datetime, timedelta
from pipes import quote

def remove_newlines(gcode_line):
    if gcode_line in ['\n', '\r', '\r\n']:
        return ' '
    gcode_line = gcode_line.strip('\n')
    gcode_line = gcode_line.strip('\r')
    return gcode_line

# def filter_out_brackets(character):
#     if character in ['(',')']:
#         return False
#     return True

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
    pause_duration = ''
    total_time = ''
    
    # Production notes
    post_production_notes = ''
    batch_number = ''

    # Metadata formatting
    gcode_summary_string = ''
    smarttransfer_metadata_string = ''
    feeds_speeds_and_boundaries_string = ''
    check_info_string = ''    
    comments_string = ''

    def __init__(self, **kwargs):
        self.l = kwargs['localization']

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

        self.batch_number = ''
        self.post_production_notes = ''

        self.gcode_summary_string = ''
        self.smarttransfer_metadata_string = ''
        self.feeds_speeds_and_boundaries_string = ''
        self.check_info_string = ''    
        self.comments_string = ''

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

            metadata = [(line.strip('()')).split(': ', 1) for line in metadata if (line.split(':', 1)[1]).strip('() ')]
            # metadata = [line.split(': ', 1) for line in metadata]
            self.metadata_dict = dict(metadata)

            print self.metadata_dict

            # Metadata looks like comments so needs to be removed
            gcode_without_metadata = self.job_gcode_raw[0:metadata_start_index] + self.job_gcode_raw[metadata_end_index + 1:-1]
            
            self.comments_list = [''.join(re.findall('\(.*?\)',s)) for s in gcode_without_metadata if "(" in s]

        except:
            # If no metadata in file
            self.comments_list = [''.join(re.findall('\(.*?\)',s)) for s in self.job_gcode_raw if "(" in s]


    def create_gcode_summary_string(self):

        print("Create summary string")

        self.smarttransfer_metadata_into_string()
        self.scraped_feeds_speeds_and_boundaries_into_string()
        self.check_info_into_string()
        self.comments_into_string()
        
        self.gcode_summary_string = (

            self.smarttransfer_metadata_string + \
            self.feeds_speeds_and_boundaries_string + \
            self.check_info_string  + \
            self.comments_string

            )

    def update_changeables_in_gcode_summary_string(self):


        print("Update changeable string")

        self.check_info_into_string()
        self.smarttransfer_metadata_into_string()
        
        self.gcode_summary_string = (

            self.smarttransfer_metadata_string + \
            self.feeds_speeds_and_boundaries_string + \
            self.check_info_string  + \
            self.comments_string
            
            )


    def smarttransfer_metadata_into_string(self):

        summary_list = []
        
        # metadata_list = self.metadata_dict.items()
        # if len(metadata_list) > 0:

        if self.metadata_dict:
            metadata_list = self.metadata_dict.items()

            [summary_list.append(': '.join(map(self.l.get_str, sublist))) for sublist in metadata_list]

            try: 
                summary_list.sort(key = lambda i: self.metadata_order[i.split(':')[0]])

            except Exception as e:
                print(str(e))

            summary_list.insert(0, "[b]SmartTransfer data[/b]")
            summary_list.insert(1, "")
            summary_list.append('')

        summary_list.append('')
        self.smarttransfer_metadata_string = '\n'.join(summary_list)


    def scraped_feeds_speeds_and_boundaries_into_string(self):

        summary_list = []

        summary_list.append('[b]Feeds and Speeds:[/b]\n')
        if self.feedrate_max == None and self.feedrate_min == None:
            summary_list.append('Feed rate range: Undefined')
        else:
            summary_list.append('Feed rate range: ' + str(self.feedrate_min) + ' to ' + str(self.feedrate_max))

        if self.spindle_speed_max == None and self.feedrate_min == None:
            summary_list.append('Spindle speed range: Undefined\n')
        else:
            summary_list.append('Spindle speed range: ' + str(self.spindle_speed_min) + ' to ' + str(self.spindle_speed_max) + '\n')


        summary_list.append('[b]Working volume:[/b]\n')
        if self.x_max == -999999 and self.x_min == 999999:
            summary_list.append('X range: Undefined\n')
        else:
            summary_list.append('X min: ' + str(self.x_min))
            summary_list.append('X max: ' + str(self.x_max) + '\n')

        if self.y_max == -999999 and self.y_min == 999999:
            summary_list.append('Y range: Undefined\n')
        else:
            summary_list.append('Y min: ' + str(self.y_min))
            summary_list.append('Y max: ' + str(self.y_max) + '\n')

        if self.z_max == -999999 and self.z_min == 999999:
            summary_list.append('Z range: Undefined\n')
        else:
            summary_list.append('Z min: ' + str(self.z_min))
            summary_list.append('Z max: ' + str(self.z_max) + '\n')

        summary_list.append('')
        self.feeds_speeds_and_boundaries_string = '\n'.join(summary_list)


    def check_info_into_string(self):

        summary_list = []

        summary_list.append('[b]Check info and warnings:[/b]\n')
        if self.checked == False:
            summary_list.append('Checked: No\n')
        else:
            summary_list.append('Checked: Yes')
            summary_list.append('Check warning: ' + self.check_warning + '\n')

        summary_list.append('')

        self.check_info_string = '\n'.join(summary_list)


    def comments_into_string(self):

        if self.comments_list:
            summary_list = []

            summary_list.append('[b]Comments:[/b]\n')
            summary_list.extend(self.comments_list[:20])
            summary_list.append('')

            self.comments_string = '\n'.join(summary_list)

        else:
            self.comments_string = ''


    def post_job_data_update_pre_send(self, successful, extra_parts_completed = 0):

        self.update_parts_completed(successful, extra_parts_completed)
        self.update_update_info_in_metadata()
        self.update_changeables_in_gcode_summary_string()

    def update_parts_completed(self, successful, extra_parts_completed = 0):

        if "Parts Made So Far" in self.metadata_dict:

            try:
                prev_parts_completed_so_far = int(self.metadata_dict["Parts Made So Far"])

                if successful:
                    self.metadata_dict["Parts Made So Far"] = str(prev_parts_completed_so_far + int(self.metadata_dict.get('Parts Made Per Job', 1)))

                    # # Update parts completed in job file
                    self.update_metadata_in_original_file("Parts Made So Far")

                elif extra_parts_completed > prev_parts_completed_so_far:
                    self.metadata_dict["Parts Made So Far"] = str(int(extra_parts_completed))

                    # # Update parts completed in job file
                    self.update_metadata_in_original_file("Parts Made So Far")

            except:
                print("Parts Made So Far couldn't be updated.")


    def update_update_info_in_metadata(self):
        if self.metadata_dict:
            self.metadata_dict['Last Updated By'] = 'SmartBench'
            timestamp = datetime.now()
            self.metadata_dict['Last Updated Time'] = timestamp.strftime('%d-%b-%y %H:%M:%S')

            self.update_metadata_in_original_file("Last Updated Time")
            self.update_metadata_in_original_file("Last Updated By")

    def update_metadata_in_original_file(self, key_to_update):

        # Update in job file
        grep_command = 'grep "' + key_to_update + '" ' + quote(self.filename)
        line_to_replace = (os.popen(grep_command).read()).strip()
        new_line = '(' + key_to_update + ': ' + str(self.metadata_dict.get(key_to_update)) + ')'
        sed_command = 'sudo sed -i "s/' + line_to_replace + '/' + new_line + '/" ' + quote(self.filename)
        os.system(sed_command)


    def post_job_data_update_post_send(self):

        self.post_production_notes = ''
        self.batch_number = ''
        self.percent_thru_job = 0


    metadata_order = {

            "Last Updated Time": 0,
            "Last Updated By": 1,
            "Internal Order Code": 2,
            "Process Step": 3,
            "Total Parts Required": 4,
            "Parts Made Per Job": 5,
            "Stock Material Type": 6,
            "Job Size X Axis": 7,
            "Job Size Y Axis": 8,
            "Job Size Z Axis": 9,
            "Stock Material Size": 10,
            "Pre Production Notes": 11,
            "Primary Operator": 12,
            "Job Duration": 13,
            "End Effector": 14,
            "Tool Diameter And Type": 15,
            "Toolpath Name": 16,
            "XY Datum Position": 17,
            "Z Datum Position": 18,
            "Maximum Feed Rate": 19,
            "Maximum Plunge Rate": 20,
            "Maximum Spindle Speed": 21,
            "Customer Name": 22,
            "Customer Part Number": 22,
            "Customer Part Description": 23,
            "Customer Order Reference": 24,
            "Parts Made So Far": 25
            }
