'''
Created on 2 Aug 2021
@author: Dennis
Module used to keep track of information about the current job
'''

def remove_newlines(gcode_line):
    if gcode_line == '\n':
        return ' '
    return gcode_line.replace('\n', '')

def filter_out_non_values(value):
    if value:
        return True
    return False

def filter_for_integers(gcode_character):
    try:
        int(gcode_character)
        return True
    except:
        return False

def filter_for_comments(gcode_line):
    if gcode_line[0] == '(':
        return True
    return False

def filter_for_feedrates(gcode_line):
    if 'F' in gcode_line and gcode_line[0] != '(':
        return True
    return False

def map_feedrates_to_values(gcode_line):
    gcode_line = gcode_line.split()
    return map(map_for_feedrate_values, gcode_line)

def map_for_feedrate_values(gcode):
    if gcode[0] == 'F':
        gcode = list(gcode)
        gcode = filter(filter_for_integers, gcode)
        return int(''.join(gcode))

def filter_for_spindle_speeds(gcode_line):
    if 'S' in gcode_line and gcode_line[0] != '(':
        return True
    return False

def map_spindle_speed_to_values(gcode_line):
    gcode_line = gcode_line.split()
    return map(map_for_spindle_speed_values, gcode_line)

def map_for_spindle_speed_values(gcode):
    if gcode[0] == 'S':
        gcode = list(gcode)
        gcode = filter(filter_for_integers, gcode)
        return int(''.join(gcode))

class JobData(object):

    filename = ''
    job_gcode = []
    job_gcode_raw = []
    comments_list = []
    feedrate_min = 0
    feedrate_max = 0

    def generate_job_data(self, raw_gcode):

        # Reset max and min value in case no new ones are found
        self.feedrate_max = 0
        self.feedrate_min = 0

        self.job_gcode_raw = map(remove_newlines, raw_gcode)

        self.comments_list = filter(filter_for_comments, self.job_gcode_raw)

        # Filter raw gcode for every line containing feedrate adjustments
        feedrates_commands_list = filter(filter_for_feedrates, self.job_gcode_raw)
        # Extract integer values from gcode
        feedrates_list = map(map_feedrates_to_values, feedrates_commands_list)
        # Flatten 2D list into single list simply containing values
        feedrates_list = [item for sublist in feedrates_list for item in sublist]
        # Remove all instances of None where no feedrates are found
        feedrates_list = filter(filter_out_non_values, feedrates_list)
        try:
            # List should now be just feedrate values, so find max and min
            self.feedrate_max = max(feedrates_list)
            self.feedrate_min = min(feedrates_list)
        except:
            # If file has no feedrate gcodes then max and min cannot be found
            pass

        # Filter raw gcode for every line containing spindle speed adjustments
        spindle_speed_commands_list = filter(filter_for_spindle_speeds, self.job_gcode_raw)
        # Extract integer values from gcode
        spindle_speed_list = map(map_spindle_speed_to_values, spindle_speed_commands_list)
        # Flatten 2D list into single list simply containing values
        spindle_speed_list = [item for sublist in spindle_speed_list for item in sublist]
        # Remove all instances of None where no spindle speeds are found
        
