'''
Created on 2 Aug 2021
@author: Dennis
Module used to keep track of information about the current job
'''
import sys, os, re
from datetime import datetime, timedelta
from pipes import quote
from chardet import detect
from itertools import takewhile
import traceback

decode_and_encode = lambda x: (unicode(x, detect(x)['encoding']).encode('utf-8'))

def remove_newlines(gcode_line):
    if gcode_line in ['\n', '\r', '\r\n']:
        return ' '
    gcode_line = decode_and_encode(gcode_line).strip('\n\r')
    return gcode_line

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

    # YetiPilot
    job_start_time = None
    g0_lines = []
    spindle_speeds = []

    def __init__(self, **kwargs):
        self.l = kwargs['localization']
        self.set = kwargs['settings_manager']

        self.metadata_order = {

            self.l.get_bold("Last Updated Time"): 0,
            self.l.get_bold("Last Updated By"): 1,
            self.l.get_bold("Internal Order Code"): 2,
            self.l.get_bold("Process Step"): 3,
            self.l.get_bold("Total Parts Required"): 4,
            self.l.get_bold("Parts Made Per Job"): 5,
            self.l.get_bold("Stock Material Type"): 6,
            self.l.get_bold("Job Size X Axis"): 7,
            self.l.get_bold("Job Size Y Axis"): 8,
            self.l.get_bold("Job Size Z Axis"): 9,
            self.l.get_bold("Stock Material Size"): 10,
            self.l.get_bold("Pre Production Notes"): 11,
            self.l.get_bold("Primary Operator"): 12,
            self.l.get_bold("Job Duration"): 13,
            self.l.get_bold("End Effector"): 14,
            self.l.get_bold("Tool Diameter And Type"): 15,
            self.l.get_bold("Toolpath Name"): 16,
            self.l.get_bold("XY Datum Position"): 17,
            self.l.get_bold("Z Datum Position"): 18,
            self.l.get_bold("Maximum Feed Rate"): 19,
            self.l.get_bold("Maximum Plunge Rate"): 20,
            self.l.get_bold("Maximum Spindle Speed"): 21,
            self.l.get_bold("Customer Name"): 22,
            self.l.get_bold("Customer Part Number"): 22,
            self.l.get_bold("Customer Part Description"): 23,
            self.l.get_bold("Customer Order Reference"): 24,
            self.l.get_bold("Parts Made So Far"): 25
            }

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

    # JOB DATA

    def scrape_last_feed_command(self, job_gcode_object, index): 

        try:
            feedrate_line = next((s for s in reversed(job_gcode_object[:index+1]) if 'F' in s), None)
            if feedrate_line:
                feedrate = re.match('\d+(\.\d+)?',feedrate_line[feedrate_line.find("F")+1:]).group()

            return float(feedrate)

        except: 
            return 0

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

            [summary_list.append('[b]:[/b] '.join([self.l.get_bold(sublist[0]), sublist[1]])) for sublist in metadata_list]

            try: 
                summary_list.sort(key = lambda i: self.metadata_order[i.split('[b]:[/b]')[0]])

            except Exception as e:
                print(str(e))

            summary_list.insert(0, self.l.get_bold("SmartTransfer data"))
            summary_list.insert(1, "")
            summary_list.append('')

        summary_list.append('')
        self.smarttransfer_metadata_string = '\n'.join(summary_list)


    def scraped_feeds_speeds_and_boundaries_into_string(self):

        summary_list = []

        summary_list.append(self.l.get_bold('Feeds and Speeds') + '\n')
        if self.feedrate_max == None and self.feedrate_min == None:
            summary_list.append(self.l.get_str('Feed rate range:') + ' ' + self.l.get_str('Undefined'))
        else:
            summary_list.append(self.l.get_str('Feed rate range:') + ' ' + str(self.feedrate_min) + ' - ' + str(self.feedrate_max))

        if self.spindle_speed_max == None and self.feedrate_min == None:
            summary_list.append(self.l.get_str('Spindle speed range:') + ' ' + self.l.get_str('Undefined') + '\n')
        else:
            summary_list.append(self.l.get_str('Spindle speed range:') + ' ' + str(self.spindle_speed_min) + ' - ' + str(self.spindle_speed_max) + '\n')


        summary_list.append(self.l.get_bold('Working volume') + '\n')
        if self.x_max == -999999 and self.x_min == 999999:
            summary_list.append(self.l.get_str('X range:') + ' ' + self.l.get_str('Undefined') + '\n')
        else:
            summary_list.append(self.l.get_str('X min:') + ' ' + str(self.x_min))
            summary_list.append(self.l.get_str('X max:') + ' ' + str(self.x_max) + '\n')

        if self.y_max == -999999 and self.y_min == 999999:
            summary_list.append(self.l.get_str('Y range:') + ' ' + self.l.get_str('Undefined') + '\n')
        else:
            summary_list.append(self.l.get_str('Y min:') + ' ' + str(self.y_min))
            summary_list.append(self.l.get_str('Y max:') + ' ' + str(self.y_max) + '\n')

        if self.z_max == -999999 and self.z_min == 999999:
            summary_list.append(self.l.get_str('Z range:') + ' ' + self.l.get_str('Undefined') + '\n')
        else:
            summary_list.append(self.l.get_str('Z min:') + ' ' + str(self.z_min))
            summary_list.append(self.l.get_str('Z max:') + ' ' + str(self.z_max) + '\n')

        summary_list.append('')
        self.feeds_speeds_and_boundaries_string = '\n'.join(summary_list)


    def check_info_into_string(self):

        summary_list = []

        summary_list.append(self.l.get_bold('Check info and warnings') + '\n')
        if self.checked == False:
            summary_list.append(self.l.get_str('Checked:') + ' ' + self.l.get_str('No') + '\n')
        else:
            summary_list.append(self.l.get_str('Checked:') + ' ' + self.l.get_str('Yes'))
            summary_list.append(self.l.get_str('Check warning:') + ' ' + self.check_warning + '\n')

        summary_list.append('')

        self.check_info_string = '\n'.join(summary_list)


    def comments_into_string(self):

        if self.comments_list:
            summary_list = []

            summary_list.append(self.l.get_bold('Comments') + '\n')
            summary_list.extend(self.comments_list[:20])
            summary_list.append('')

            self.comments_string = '\n'.join(summary_list)

        else:
            self.comments_string = ''


    def post_job_data_update_pre_send(self, successful, extra_parts_completed = 0):

        self.update_parts_completed(successful, extra_parts_completed)
        self.update_metadata_in_original_file()
        self.update_changeables_in_gcode_summary_string()

    def update_parts_completed(self, successful, extra_parts_completed = 0):

        if "Parts Made So Far" in self.metadata_dict:

            try:
                prev_parts_completed_so_far = int(self.metadata_dict["Parts Made So Far"])

                if successful:
                    self.metadata_dict["Parts Made So Far"] = str(prev_parts_completed_so_far + int(self.metadata_dict.get('Parts Made Per Job', 1)))

                elif extra_parts_completed > prev_parts_completed_so_far:
                    self.metadata_dict["Parts Made So Far"] = str(int(extra_parts_completed))

            except:
                print("Parts Made So Far couldn't be updated.")


    def update_update_info_in_metadata(self):

        if self.metadata_dict:
            self.metadata_dict['Last Updated By'] = 'SmartBench'
            self.metadata_dict['Last Updated Time'] = datetime.now(self.set.timezone).strftime('%Y-%m-%d %H:%M:%S')

    def update_metadata_in_original_file(self):

        try:

            self.update_update_info_in_metadata()

            def not_end_of_metadata(x):
                if "(End of YetiTool SmartBench MES-Data)" in x: return False
                else: return True

            def replace_metadata(old_line):
                key_to_update = old_line.split(':')[0]
                return ('(' + key_to_update + ': ' + str(self.metadata_dict.get(key_to_update, "")) + ')\n')

            with open(self.filename, "r+") as previewed_file:

                first_line = previewed_file.readline()

                if '(YetiTool SmartBench MES-Data)' in first_line:

                    all_lines = [first_line] + previewed_file.readlines()                    
                    metadata = map(replace_metadata, [decode_and_encode(i).strip('\n\r()') for i in takewhile(not_end_of_metadata, all_lines[1:]) ])
                    all_lines[1: len(metadata) + 1] = metadata
                    previewed_file.seek(0)
                    previewed_file.writelines(all_lines)
                    previewed_file.truncate()

        except:
            print("Could not update file")
            print(str(traceback.format_exc()))


    def post_job_data_update_post_send(self):

        self.post_production_notes = ''
        self.batch_number = ''
        self.percent_thru_job = 0

    def get_excluded_line_numbers(self, gcode):
        self.g0_lines[:] = []
        for i, line in enumerate(gcode):
            if 'G0' in line:
                self.g0_lines.append(i)
                for j, next_line in enumerate(gcode[i + 1:]):
                    if 'G1' in next_line or 'G2' in next_line or 'G3' in next_line:
                        break
                    else:
                        self.g0_lines.append(i + j + 1)
        return self.g0_lines

    def get_spindle_speeds(self, gcode):
        self.spindle_speeds[:] = []
        for i, line in enumerate(gcode):
            if 'S' in line:
                s_index = line.index('S')
                end_index = s_index + 1
                while end_index < len(line) and not line[end_index].isalpha():
                    end_index += 1
                s_value = float(line[s_index + 1:end_index].strip())
                self.spindle_speeds.append([i, s_value])
        return self.spindle_speeds