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

    # Job recovery
    job_recovery_info_filepath = './asmcnc/job/job_recovery.txt'
    job_recovery_filepath = ''
    job_recovery_cancel_line = 0
    job_recovery_selected_line = -1
    job_recovery_gcode = []
    job_recovery_offset = 0 # How many lines the software added to the start of the file

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

        # Restore job recovery info
        self.read_from_recovery_file()

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

            print(self.metadata_dict)

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


    def read_from_recovery_file(self):
        try:
            with open(self.job_recovery_info_filepath, 'r') as job_recovery_info_file:
                job_recovery_info = job_recovery_info_file.read().splitlines()

            self.job_recovery_filepath = job_recovery_info[0]
            self.job_recovery_cancel_line = int(job_recovery_info[1])

        except:
            print("Could not read recovery info")
            print(str(traceback.format_exc()))

    def write_to_recovery_file(self, cancel_line):
        try:
            # Account for number of lines added in by the software when running file
            cancel_line -= self.job_recovery_offset
            self.job_recovery_offset = 0

            with open(self.job_recovery_info_filepath, 'w+') as job_recovery_info_file:
                job_recovery_info_file.write(self.filename + "\n" + str(cancel_line))

            # Simultaneously update variables
            self.job_recovery_filepath = self.filename
            self.job_recovery_cancel_line = cancel_line
            self.job_recovery_selected_line = -1
            self.job_recovery_gcode = []
            self.job_recovery_offset = 0
        
        except:
            print("Could not write recovery info")
            print(str(traceback.format_exc()))

    def clear_recovery_file(self):
        try:
            open(self.job_recovery_info_filepath, 'w').close()

            # Simultaneously update variables
            self.job_recovery_filepath = ''
            self.job_recovery_cancel_line = 0
            self.job_recovery_selected_line = -1
            self.job_recovery_gcode = []
            self.job_recovery_offset = 0
        
        except:
            print("Could not clear recovery info")
            print(str(traceback.format_exc()))


    def reset_recovery(self):
        self.job_recovery_selected_line = -1
        self.job_recovery_gcode = []
        self.job_recovery_offset = 0

    def generate_recovery_gcode(self):
        try:
            recovery_gcode = []

            # Recover modal gcodes

            # Coordinate System Select
            coord_system_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G5[4-9]", s)), None)
            if coord_system_line:
                recovery_gcode.append(re.search("G5[4-9](\.[1-3])?", coord_system_line).group(0))

            # Plane selection
            plane_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G1[7-9]", s)), None)
            if plane_line:
                recovery_gcode.append(re.search("G1[7-9]", plane_line).group(0))

            # Absolute or incremental distance mode
            distance_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G9[0,1]([A-Z]|\s|$)", s)), None)
            if distance_line:
                # Recovery not allowed if G91 is used
                if re.search("G91([A-Z]|\s|$)", distance_line):
                    return False, 'The last positioning declaration was incremental (G91), and therefore this job cannot be recovered.'
                recovery_gcode.append("G90")

            # Arc IJK distance mode
            arc_mode_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G9[0,1]\.1", s)), None)
            if arc_mode_line:
                return False, 'Job recovery does not currently support arc distance modes. This job contains [G90.1/G91.1], and therefore cannot be recovered.'

            # Feed rate mode
            feedrate_mode_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G9[3-5]", s)), None)
            if feedrate_mode_line:
                if re.search("G94", feedrate_mode_line):
                    recovery_gcode.append('G94')
                else:
                    return False, 'Job recovery only supports feed rate mode G94. This job contains [G93/G95], and therefore cannot be recovered.'

            # Units
            unit_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G2[0,1]", s)), None)
            if unit_line:
                recovery_gcode.append(re.search("G2[0,1]", unit_line).group(0))

            # Cutter radius compensation
            if next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if 'G40' in s), None):
                recovery_gcode.append('G40')

            # Tool length offset
            tool_length_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G4(3\.1|9)", s)), None)
            if tool_length_line:
                recovery_gcode.append(re.search("G4(3\.1|9)", tool_length_line).group(0))

            # Program mode
            program_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("M0?[0-2](\D|$)|M30", s)), None)
            if program_line:
                # String needs to be sliced to different length depending on whether there is an extra 0
                if re.search("M0[0-2](\D|$)|M30", program_line):
                    recovery_gcode.append(re.search("M0?[0-2](\D|$)|M30", program_line).group(0)[:3])
                else:
                    recovery_gcode.append(re.search("M0?[0-2](\D|$)|M30", program_line).group(0)[:2])

            # Spindle state
            spindle_state_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("M0?[3-5](\D|$)", s)), None)
            if spindle_state_line:
                # String needs to be sliced to different length depending on whether there is an extra 0
                if re.search("M0[3-5](\D|$)", spindle_state_line):
                    recovery_gcode.append(re.search("M0?[3-5](\D|$)", spindle_state_line).group(0)[:3])
                else:
                    recovery_gcode.append(re.search("M0?[3-5](\D|$)", spindle_state_line).group(0)[:2])

            # Coolant state
            gcode_to_search = reversed(self.job_gcode[:self.job_recovery_selected_line])
            coolant_line = next((s for s in gcode_to_search if re.search("M0?[7-9](\D|$)", s)), None)
            if coolant_line:
                if re.search("M0?9(\D|$)", coolant_line):
                    recovery_gcode.append("M9")
                else:
                    # M7 and M8 can be enabled simultaneously according to documentation
                    if 'M7' in coolant_line or 'M07' in coolant_line:
                        previous_coolant_line = next((s for s in gcode_to_search if re.search("M0?[8,9](\D|$)", s)), None)
                        if previous_coolant_line:
                            if 'M8' in previous_coolant_line or 'M08' in previous_coolant_line:
                                recovery_gcode += ['M8', 'M7']
                            else:
                                recovery_gcode.append('M7')
                    elif 'M8' in coolant_line or 'M08' in coolant_line:
                        previous_coolant_line = next((s for s in gcode_to_search if re.search("M0?[7,9](\D|$)", s)), None)
                        if previous_coolant_line:
                            if 'M7' in previous_coolant_line or 'M07' in previous_coolant_line:
                                recovery_gcode += ['M7', 'M8']
                            else:
                                recovery_gcode.append('M8')


            # Recover most recent spindle speed
            spindle_speed_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if 'S' in s), None)
            if spindle_speed_line:
                spindle_speed = spindle_speed_line[spindle_speed_line.find("S")+1:].split("M")[0]
                recovery_gcode.append("S" + spindle_speed)

            # Recover most recent feedrate
            feedrate_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if 'F' in s), None)
            if feedrate_line:
                feedrate = re.match('\d+',feedrate_line[feedrate_line.find("F")+1:]).group()


            # Recover most recent position
            x_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if 'X' in s), None)
            if x_line:
                x = re.split('(X|Y|Z|F|S|I|J|K|G)', x_line)[re.split('(X|Y|Z|F|S|I|J|K|G)', x_line).index('X') + 1]
            else:
                x = "0.000"
            y_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if 'Y' in s), None)
            if y_line:
                y = re.split('(X|Y|Z|F|S|I|J|K|G)', y_line)[re.split('(X|Y|Z|F|S|I|J|K|G)', y_line).index('Y') + 1]
            else:
                y = "0.000"
            z_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if 'Z' in s), None)
            if z_line:
                z = re.split('(X|Y|Z|F|S|I|J|K|G)', z_line)[re.split('(X|Y|Z|F|S|I|J|K|G)', z_line).index('Z') + 1]
            else:
                z = "0.000"

            # Motion mode
            motion_line = next((s for s in reversed(self.job_gcode[:self.job_recovery_selected_line]) if re.search("G0?[0,1](\D|$)", s)), None)
            if motion_line:
                # Do G0 or G1 last depending on which happened latest
                if re.search("G0?1(\D|$)", motion_line):
                    recovery_gcode.append("G0 X" + x + " Y" + y)
                    recovery_gcode.append("G0 Z" + z)
                    if feedrate_line:
                        recovery_gcode.append("G1 F" + feedrate)
                else:
                    if feedrate_line:
                        recovery_gcode.append("G1 F" + feedrate)
                    recovery_gcode.append("G0 X" + x + " Y" + y)
                    recovery_gcode.append("G0 Z" + z)
            else:
                recovery_gcode.append("G0 X" + x + " Y" + y)
                recovery_gcode.append("G0 Z" + z)
                if feedrate_line:
                    recovery_gcode.append("G1 F" + feedrate)


            # Recovery gcode now contains scraped modal gcode, not in the original file
            # Selected line represents the number of lines of the original file that will be skipped
            # Both need to be accounted for in the offset in case of repeat cancellation while running recovered code
            self.job_recovery_offset = len(recovery_gcode) - self.job_recovery_selected_line

            recovery_gcode += self.job_gcode[self.job_recovery_selected_line:]
            self.job_recovery_gcode = recovery_gcode

            return True, ''

        except:
            # An error occurred, job cannot be recovered
            return False, 'This job cannot be recovered! Please check your job for errors.'
