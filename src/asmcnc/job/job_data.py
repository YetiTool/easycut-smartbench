'''
Created on 2 Aug 2021
@author: Dennis
Module used to keep track of information about the current job
'''

def remove_newlines(gcode_line):
    if gcode_line == '\n':
        return ' '
    return gcode_line.replace('\n', '')

def filter_out_none(value):
    if value == None:
        return False
    return True

def filter_for_integers(character):
    try:
        int(character)
        return True
    except:
        # Decimal points need to be kept in
        if character == '.':
            return True
        return False

def space_out_gcodes(character):
    if character.isalpha():
        return ' ' + character
    return character

def filter_for_comments(gcode_line):
    if gcode_line[0] == '(':
        return True
    return False

def filter_for_rates(gcode_line):
    if ('F' in gcode_line or 'S' in gcode_line) and gcode_line[0] != '(':
        return True
    return False

def map_feedrates_to_values(gcode_line):
    # Ensure that gcodes are spaced out
    gcode_line = map(space_out_gcodes, gcode_line)
    gcode_line = ''.join(gcode_line)
    # Now that gcodes are definitely spaced out, split into list
    gcode_line = gcode_line.split()
    return map(map_for_feedrate_values, gcode_line)

def map_for_feedrate_values(gcode):
    if gcode[0] == 'F':
        gcode = list(gcode)
        gcode = filter(filter_for_integers, gcode)
        try:
            return int(''.join(gcode))
        except:
            # For the case when non integer values are given
            return float(''.join(gcode))

def filter_for_spindle_speeds(gcode_line):
    if 'S' in gcode_line and gcode_line[0] != '(':
        return True
    return False

def map_spindle_speed_to_values(gcode_line):
    # Ensure that gcodes are spaced out
    gcode_line = map(space_out_gcodes, gcode_line)
    gcode_line = ''.join(gcode_line)
    # Now that gcodes are definitely spaced out, split into list
    gcode_line = gcode_line.split()
    return map(map_for_spindle_speed_values, gcode_line)

def map_for_spindle_speed_values(gcode):
    if gcode[0] == 'S':
        gcode = list(gcode)
        gcode = filter(filter_for_integers, gcode)
        try:
            return int(''.join(gcode))
        except:
            # For the case when non integer values are given
            return float(''.join(gcode))

class JobData(object):

    filename = ''
    job_gcode = []
    job_gcode_raw = []
    job_gcode_modified = []
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

    def reset_values(self):
        self.filename = ''
        self.job_gcode = []
        self.job_gcode_raw = []
        self.job_gcode_modified = []
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

    def generate_job_data(self, raw_gcode):

        # Reset max and min values in case no new ones are found
        self.feedrate_max = None
        self.feedrate_min = None
        self.spindle_speed_max = None
        self.spindle_speed_min = None

        self.job_gcode_raw = map(remove_newlines, raw_gcode)

        self.comments_list = filter(filter_for_comments, self.job_gcode_raw)

        # Filter raw gcode for every line containing feedrate or spindle speed adjustments
        feed_speed_commands_list = filter(filter_for_rates, self.job_gcode_raw)
        # Search commands for values
        self.find_feedrates_max_min(feed_speed_commands_list)
        self.find_spindle_speed_max_min(feed_speed_commands_list)


    def find_feedrates_max_min(self, commands_list):
        # Extract integer values from gcode
        feedrates_list = map(map_feedrates_to_values, commands_list)
        # Flatten 2D list into single list
        feedrates_list = [item for sublist in feedrates_list for item in sublist]
        # Remove all instances of None where no feedrates are found
        feedrates_list = filter(filter_out_none, feedrates_list)
        try:
            # List should now be just feedrate values, so find max and min
            self.feedrate_max = max(feedrates_list)
            self.feedrate_min = min(feedrates_list)
        except:
            # If file has no feedrate gcodes then max and min cannot be found
            pass

    def find_spindle_speed_max_min(self, commands_list):
        # Extract integer values from gcode
        spindle_speed_list = map(map_spindle_speed_to_values, commands_list)
        # Flatten 2D list into single list
        spindle_speed_list = [item for sublist in spindle_speed_list for item in sublist]
        # Remove all instances of None where no spindle speeds are found
        spindle_speed_list = filter(filter_out_none, spindle_speed_list)
        try:
            # List should now be just spindle speed values, so find max and min
            self.spindle_speed_max = max(spindle_speed_list)
            self.spindle_speed_min = min(spindle_speed_list)
        except:
            # If file has no spindle speed gcodes then max and min cannot be found
            pass
