'''
Module to process readings from DTI, and send to Production > Operator Resources > Live Measurements > Straightness Data
'''
import os, sys
import math
import operator
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pprint
from datetime import datetime, date


import requests.auth
import binascii
import hashlib
import hmac
import json

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from asmcnc.skavaUI import widget_status_bar, widget_gcode_monitor, widget_xy_move

from asmcnc.production import encoder_connection, linear_encoder_widget_xy_move


AMA0 = 'ttyACM0' # check these when HW is installed
AMA1 = 'ttyACM1' # check these when HW is installed
y_length = float(2640 - 20) #mm
encoder_resolution = 0.025 # mm (25 microns)
x_beam_length = 1300 # mm


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

# SET UP SCREEN

Builder.load_string("""

<ProcessLinearEncoderScreen>:

    bench_id : bench_id 
    travel : travel
    test_id : test_id
    bench_width : bench_width
    data_status_label : data_status_label
    h_read_label : h_read_label
    f_read_label : f_read_label

    prep_test : prep_test
    go_stop : go_stop
    move_container : move_container
    gcode_monitor_container : gcode_monitor_container
    status_container : status_container

    BoxLayout:
        padding: 0
        spacing: 0
        orientation: "vertical"
        canvas:
            Color:
                rgba: hex('#E5E5E5FF')
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            size_hint_y: 0.92
            padding: 0
            spacing: 10
            orientation: "vertical"

            GridLayout: 
                pos: self.parent.pos
                size_hint_y: 0.15
                rows: 2
                cols: 7
                cols_minimum: {0: 200, 1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100}
                rows_minimum: {0: 10, 1: 20}

                # Test set up labels

                Label: 
                    text: "Bench ID"
                    color: 0,0,0,1

                Label: 
                    text: "Travel"
                    color: 0,0,0,1

                Label: 
                    text: "Test no."
                    color: 0,0,0,1
                
                Label: 
                    text: "Bench width."
                    color: 0,0,0,1

                Label: 
                    text: "Data status:"
                    color: 0,0,0,1

                Label: 
                    text: "H Read"
                    color: 0,0,0,1

                Label: 
                    text: "F Read"
                    color: 0,0,0,1


                # Test setting inputs/buttons

                TextInput: 
                    id: bench_id 
                    text: "test-reformat"
                    multiline: False
                    font_size: '20sp'

                TextInput: 
                    id: travel
                    text: "2489"
                    input_filter: 'float'
                    multiline: False
                    font_size: '20sp'

                TextInput: 
                    id: test_id
                    text: "1"
                    input_filter: 'int'
                    multiline: False
                    font_size: '20sp'

                TextInput: 
                    id: bench_width
                    text: "460"
                    multiline: False
                    font_size: '20sp'

                Label: 
                    id: data_status_label
                    text: "status"
                    color: 0,0,0,1

                Label: 
                    id: h_read_label
                    text: "-"
                    color: 0,0,0,1

                Label: 
                    id: f_read_label
                    text: "-"
                    color: 0,0,0,1

            GridLayout: 
                pos: self.parent.pos
                size_hint_y: 0.15
                rows: 1
                cols: 4
                spacing: 5

                Button:
                    id: prep_test
                    text: "GET READY"
                    on_press: root.set_up_for_test()
                    background_color: [0,0,0,1]
                    background_normal: ''

                ToggleButton:
                    id: go_stop
                    text: "GO"
                    on_press: root.run_stop_test()
                    background_color: [0,0,0,1]
                    background_normal: ''

                Button:
                    text: "RESET DATA"
                    on_press: root.clear_data()

                Button:
                    text: "QUIT"
                    on_press: root.go_to_lobby()

            BoxLayout:
                size_hint_y: 0.62
                orientation: 'horizontal'
                BoxLayout:
                    height: self.parent.height
                    size_hint_x: 0.57
                    id: move_container
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                BoxLayout:
                    height: self.parent.height
                    id: gcode_monitor_container
        BoxLayout:
            size_hint_y: 0.08
            id: status_container
""")

class ProcessLinearEncoderScreen(Screen):

    POLL_TIME = 1

    # LISTS TO HOLD RAW RECORDED DATA AS IT COMES IN
    Y_pos_list = []
    HOME_raw_pulse_list = []
    FAR_raw_pulse_list = []

    # JSON FORMAT LISTS (AFTER CALCULATIONS)
    machine_Y_coordinate = []

    HOME_raw_converted = []
    FAR_raw_converted = []

    HOME_distance_abs = []
    FAR_distance_abs = []

    Y_true = []
    angle_off_square = []

    delta_y_grbl_home = []
    delta_y_grbl_far = []
    Y_axis_linear_drift = []
    Y_axis_angular_offset = []
    delta_y_home = []
    delta_y_far = []

    DELTA_Y_X_BEAM = []
    DELTA_Y_PER_METER = []

    # TEST PARAMETERS
    starting_pos = 0
    max_pos = 0

    # TEMPLATE SHEET THAT SHEET FORMAT IS COPIED FROM
    master_sheet_key = '1y1Rq29icpISFIGvaygeI-jye40V_g5lE2NIVgMf_cI8'

    # FOLDER ID TO COLLATE RESULTS
    squareness_measurements_id = '1WcHTrNSNO3skkT3-kKhAi4qjv6-t2xQV'

    # GOOGLE API OBJECTS
    gsheet_client = None
    drive_service = None

    active_spreadsheet_object = None
    active_spreadsheet_name = ''
    active_spreadsheet_id = ''

    # STATUS FLAGS
    data_status = 'Ready'

    # READ IN VALUES
    H_read = ''
    F_read = ''

    # SET UP KIVY CLOCK EVENT OBJECTS
    poll_for_screen = None

    def __init__(self, **kwargs):

        super(ProcessLinearEncoderScreen, self).__init__(**kwargs)

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        # WIDGET SETUP
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))
        self.gcode_monitor_container.add_widget(widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.sm))
        # self.move_container.add_widget(widget_xy_move.XYMove(machine=self.m, screen_manager=self.sm))
        self.move_container.add_widget(linear_encoder_widget_xy_move.LinEncXYMove(machine=self.m, screen_manager=self.sm))

        if sys.platform != 'win32' and sys.platform != 'darwin':

            ## GSHEET SETUP
            scope = [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/drive.file'
                ]
            file_name = os.path.dirname(os.path.realpath(__file__)) + '/keys/live-measurements-api-key.json'
            creds = service_account.Credentials.from_service_account_file(file_name, scopes=scope)
            self.drive_service = build('drive', 'v3', credentials=creds)
            self.gsheet_client = gspread.authorize(creds)

        # ENCODER SERIAL CONNECTION SET UP
        self.e0 = encoder_connection.EncoderConnection(self.sm, AMA0)
        self.e1 = encoder_connection.EncoderConnection(self.sm, AMA1)

        self.e0.establish_connection()
        self.e1.establish_connection()


    def on_enter(self):

        self.poll_for_screen = Clock.schedule_interval(self.update_screen, 0.2)

        if self.m.is_machine_homed:
            self.prep_test.background_color = [0,0.502,0,1]

            # TURNS BUTTON GREEN IF DTI IS CONNECTED
            if self.e0.is_connected() and self.e1.is_connected():
                self.go_stop.background_color = [0,0.502,0,1]


    def go_to_lobby(self):
        self.sm.current = 'developer_temp'

    def on_leave(self):

        if self.poll_for_screen != None:
            Clock.unschedule(self.poll_for_screen)


    # TEST SET UP

    def set_up_for_test(self):
        self.m.jog_absolute_single_axis('Y', self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Y', (self.m.y_min_jog_abs_limit + 10.00), 6000)
        # self.m.send_any_gcode_command('G0 G91 Y10')


    # MACHINE RUN TEST FUNCTIONS

    def run_stop_test(self):

        if self.go_stop.state == 'down':

            ## CHANGE BUTTON
            self.go_stop.background_color = [1,0,0,1]
            self.go_stop.text = 'STOP'

            ## SET VARIABLES
            self.clear_data()
            self.starting_pos = float(self.m.mpos_y())

            # don't need to worry about which arduino is in which port
            # this is only raw counts
            self.starting_H = self.e0.H_side + self.e1.H_side
            self.starting_F = self.e0.F_side + self.e1.F_side

            self.max_pos = self.set_max_pos()

            ## START THE TEST
            self.test_run = Clock.schedule_interval(self.do_test_step, self.POLL_TIME)
            self.data_status = 'Collecting'

        elif self.go_stop.state == 'normal':
            self.end_of_test_sequence()


    def end_of_test_sequence(self):

        Clock.unschedule(self.test_run)

        self.data_status = 'Collected'

        self.go_stop.background_color = [0,0.502,0,1]
        self.go_stop.text = 'GO'
        self.go_stop.state = 'normal'

        Clock.schedule_once(lambda dt: self.send_data(), 1)


    def set_max_pos(self):
        return self.starting_pos + float(self.travel.text)


    def do_test_step(self, dt):

        ## INCREMENTAL

        if self.m.state() == 'Run':
            pass

        elif self.m.state() == 'Idle' and self.m.mpos_y() <= self.max_pos:

            self.HOME_raw_pulse_list.append(self.e0.H_side + self.e1.H_side)
            self.FAR_raw_pulse_list.append(self.e0.F_side + self.e1.F_side)
            self.Y_pos_list.append(float(self.m.mpos_y()))

            self.m.send_any_gcode_command('G0 G91 Y10')

        else:
            self.end_of_test_sequence()


    # CLEAR (RESET) LOCAL DATA (DOES NOT AFFECT ANYTHING ALREADY SENT TO SHEETS)

    def clear_data(self, clearall = False):

        # LISTS TO HOLD RAW RECORDED DATA
        self.Y_pos_list = []
        self.HOME_raw_pulse_list = []
        self.FAR_raw_pulse_list = []

        # JSON FORMAT LISTS (AFTER CALCULATIONS)
        self.machine_Y_coordinate = []
        self.HOME_raw_converted = []
        self.FAR_raw_converted = []
        self.HOME_distance_abs = []
        self.FAR_distance_abs = []
        self.Y_true = []
        self.angle_off_square = []
        self.delta_y_grbl_home = []
        self.delta_y_grbl_far = []
        self.Y_axis_linear_drift = []
        self.Y_axis_angular_offset = []
        self.delta_y_home = []
        self.delta_y_far = []
        self.DELTA_Y_X_BEAM = []
        self.DELTA_Y_PER_METER = []

        # TEST PARAMETERS
        self.starting_pos = 0
        self.max_pos = 0

        self.data_status = 'Ready'


    ## SENDING DATA

    # MAIN FUNCTION CALLED BY BUTTON
    def send_data(self):

        # screen needs to be updated before sending data
        # as data sending is an intensive process and locks up kivy
        self.data_status = 'Sending'

        # start main data sending processes after 2 seconds
        Clock.schedule_once(self.do_data_send, 2)


    # FUNCTIONS DIRECTLY CALLED BY SEND_DATA()
    def do_data_send(self, dt):

        self.active_spreadsheet_name = self.bench_id.text + ' ' + str(date.today())
        self.format_output()
        self.open_spreadsheet() # I.E. OPEN GOOGLE SHEETS DOCUMENT
        self.write_to_worksheet()

        # try: self.write_to_worksheet()
        # except: 
        #     log('Failed to write to sheet')
        #     self.data_status ='Try Resending'

    # GOOGLE SHEETS DATA FORMATTING FUNCTIONS

    # DEV NOTE: THIS FUNCTION IS ALMOST DONE, BUT STILL NEEDS TESTING

    def format_output(self):

        # work out distance travelled from raw pulses
        HOME_measured_distance = [(self.starting_pos + float((H - self.starting_H)*encoder_resolution)) for H in self.HOME_raw_pulse_list]
        FAR_measured_distance = [(self.starting_pos + float((F - self.starting_F)*encoder_resolution)) for F in self.FAR_raw_pulse_list]

        # grbl machine coordinates
        machine_coordinates = self.Y_pos_list

        # work out absolute difference between measurements (or as modulus in the absolute value maths sense)
        opposite_side = list(map(lambda h, f: operator.sub(h,f), HOME_measured_distance, FAR_measured_distance))

        # work out midpoint of measurement difference
        midpoints = list(map(lambda h, f: (h+f)/2, HOME_measured_distance, FAR_measured_distance))

        # calculate linear drift: offset between each midpoint and the reported Y position from the machine
        linear_drift = list(map(operator.sub, midpoints, machine_coordinates))

        # calculate diff between grbl value and each measurement
        delta_y_grbl_h = list(map(operator.sub, HOME_measured_distance, machine_coordinates))
        delta_y_grbl_f = list(map(operator.sub, FAR_measured_distance, machine_coordinates))

        # calculate angle at each data point using artan trig (tan(theta) = opp/adj)
        adjacent_side = float(self.bench_width.text)
        angle_radians = list(map(lambda o: (math.atan(o/adjacent_side)), opposite_side)) # radians
        angle_degrees = list(map(lambda a: a*(180/math.pi), angle_radians))

        # calculate maximum y difference across beam ends
        DELTA_Y_X = list(map(lambda a: x_beam_length*(math.sin(a)), angle_radians))

        # calculate maximum mm offset at extremes due to angle out of square
        delta_y_mid_end = list(map(lambda d: d/2, DELTA_Y_X))

        # calculate aggregate offset due to both linear drift and angle out of square at home side
        delta_y_h = list(map(lambda l, a: l+a, linear_drift, delta_y_mid_end))

        # calculate aggregate offset due to both linear drift and angle out of square at far side
        delta_y_f = list(map(lambda l, a: l-a, linear_drift, delta_y_mid_end))

        DELTA_Y_PM = list(map(lambda a: (1000*math.tan(a)), angle_radians))

        # convert everthing into json format, ready to send out to gsheets
        self.HOME_raw_converted = self.convert_to_json(self.HOME_raw_pulse_list)
        self.FAR_raw_converted = self.convert_to_json(self.FAR_raw_pulse_list)

        self.HOME_distance_abs = self.convert_to_json(HOME_measured_distance)
        self.FAR_distance_abs = self.convert_to_json(FAR_measured_distance)
        self.Y_true = self.convert_to_json(midpoints)

        self.machine_Y_coordinate = self.convert_to_json(machine_coordinates)

        self.angle_off_square = self.convert_to_json(angle_degrees)

        self.delta_y_grbl_home = self.convert_to_json(delta_y_grbl_h)
        self.delta_y_grbl_far = self.convert_to_json(delta_y_grbl_f)
        self.Y_axis_linear_drift = self.convert_to_json(linear_drift)
        self.Y_axis_angular_offset = self.convert_to_json(delta_y_mid_end)

        self.delta_y_home = self.convert_to_json(delta_y_h)
        self.delta_y_far = self.convert_to_json(delta_y_f)

        self.DELTA_Y_X_BEAM = self.convert_to_json(DELTA_Y_X)
        self.DELTA_Y_PER_METER = self.convert_to_json(DELTA_Y_PM)


    def convert_to_json(self, data):
        # Need to convert to json format in order to export to gsheets

        new_data = []

        data = [str(x).split() for x in data]

        for list in data:
            new_list_item = [float(e) for e in list]
            new_data.append(new_list_item)

        return new_data


    # FUNCTIONS TO MANAGE SPREADSHEET - OPENING AND MOVING
    # FUNCTIONS TO MANAGE SPREADSHEET - OPENING AND MOVING

    def open_spreadsheet(self):

        # CHECK WHETHER SPREADSHEET FOR SERIAL NUMBER ALREADY EXISTS

        page_token = None
        create_new_document = True

        # this is the query that gets passed to the files.list function, and looks for files in the straigtness measurements folder
        # and with a name that contains the current bench id
        q_str = "'" + self.squareness_measurements_id + "'" + " in " + "parents" + ' and ' "name" + " contains " + "'" + self.bench_id.text + "'"

        while True:
            log('Looking for existing file to send data to...')
            lookup_file = self.drive_service.files().list(q=q_str,
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=page_token).execute()

            for file in lookup_file.get('files', []): # this is written to loop through and find multiple files, but actually we only want one (and only expect one!)

                log('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                found_spreadsheet_object = self.gsheet_client.open_by_key(file.get('id'))
                if found_spreadsheet_object.title != self.active_spreadsheet_name:
                    self.rename_file_with_current_date(found_spreadsheet_object)
                else:
                    self.active_spreadsheet_object = found_spreadsheet_object
                create_new_document = False

            if not create_new_document:
                break

            page_token = lookup_file.get('nextPageToken', None)
            if page_token is None:
                break

        # IF THIS IS A NEW BENCH/EXTRUSION, CREATE A NEW SPREADSHEET
        if create_new_document:

            log('Creating new document')
            self.active_spreadsheet_object = self.gsheet_client.copy(self.master_sheet_key, title = self.active_spreadsheet_name, copy_permissions = True)
            self.active_spreadsheet_object.share('yetitool.com', perm_type='domain', role='writer')
            self.rename_template_sheets()
            self.move_sheet_to_operator_resources()


    def rename_file_with_current_date(self, found_spreadsheet):

        self.active_spreadsheet_object = self.gsheet_client.copy(found_spreadsheet.id, title = self.active_spreadsheet_name, copy_permissions = True)
        self.gsheet_client.del_spreadsheet(found_spreadsheet.id)


    def rename_template_sheets(self):

        # this function can only be used on fresh duplicated spreadsheet - not individually copied sheets
        self.active_spreadsheet_object.worksheet('Calibration - Date - Test').update_title(calibration_data_worksheet_name)
        self.active_spreadsheet_object.worksheet('Straightness - Date - Test').update_title(straightness_data_worksheet_name)
        self.active_spreadsheet_object.worksheet('Summary - Date - Test').update_title(summary_data_worksheet_name)


    def copy_template_worksheets_to_existing_spread(self):

        # order of this important - need to trick the summary sheet into looking at the new copied data sheets

        # set up new names
        calibration_data_worksheet_name =  'Calibration' + " - " + str(date.today()) + " - " + self.test_id.text
        straightness_data_worksheet_name =  'Straightness' + " - " + str(date.today()) + " - " + self.test_id.text
        summary_data_worksheet_name =  'Summary' + " - " + str(date.today()) + " - " + self.test_id.text

        # set up worksheet objects from the master sheet, which we'll copy across individually
        master_sheet_object = self.gsheet_client.open_by_key(self.master_sheet_key)
        Calibration_master_sheet = master_sheet_object.worksheet('Calibration - Date - Test')
        Straightness_master_sheet = master_sheet_object.worksheet('Straightness - Date - Test')
        Summary_master_sheet = master_sheet_object.worksheet('Summary - Date - Test')

        # first, ONLY copy the data sheets
        Calibration_master_sheet.copy_to(self.active_spreadsheet_object.id)
        Straightness_master_sheet.copy_to(self.active_spreadsheet_object.id)

        # when they are individually copied, they come across as "Copy of X" - need to rename them so that the Summary sheet will recognize
        # the template naming convention
        self.active_spreadsheet_object.worksheet('Copy of Calibration - Date - Test').update_title('Calibration - Date - Test')
        self.active_spreadsheet_object.worksheet('Copy of Straightness - Date - Test').update_title('Straightness - Date - Test')

        # Now copy the master sheet
        Summary_master_sheet.copy_to(self.active_spreadsheet_object.id)

        # When master sheet is looking at the right data sheets, rename them all together
        self.active_spreadsheet_object.worksheet('Calibration - Date - Test').update_title(calibration_data_worksheet_name)
        self.active_spreadsheet_object.worksheet('Straightness - Date - Test').update_title(straightness_data_worksheet_name)
        self.active_spreadsheet_object.worksheet('Copy of Summary - Date - Test').update_title(summary_data_worksheet_name)

        # Update index of most recent summary sheet so that it sits at the front of the worksheet (after the key)
        self.active_spreadsheet_object.worksheet(summary_data_worksheet_name).update_index(1)


    def move_sheet_to_operator_resources(self):

        log('Moving document to production > operator resources > live measurements')

        # Take the file ID and move it into the operator resources folder

        # Retrieve the existing parents to remove
        file = self.drive_service.files().get(fileId=self.active_spreadsheet_object.id,
                                         fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = self.drive_service.files().update(fileId=self.active_spreadsheet_object.id,
                                            addParents=self.squareness_measurements_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()
    # def open_spreadsheet(self):

    #     # CHECK WHETHER SPREADSHEET FOR SERIAL NUMBER ALREADY EXISTS

    #     page_token = None
    #     create_new_document = True

    #     # this is the query that gets passed to the files.list function, and looks for files in the straigtness measurements folder
    #     # and with a name that contains the current bench id
    #     q_str = "'" + self.squareness_measurements_id + "'" + " in " + "parents" + ' and ' "name" + " contains " + "'" + self.bench_id.text + "'"

    #     while True:
    #         log('Looking for existing file to send data to...')
    #         lookup_file = self.drive_service.files().list(q=q_str,
    #                                                     spaces='drive',
    #                                                     fields='nextPageToken, files(id, name)',
    #                                                     pageToken=page_token).execute()

    #         for file in lookup_file.get('files', []): # this is written to loop through and find multiple files, but actually we only want one (and only expect one!)

    #             log('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    #             self.active_spreadsheet_object = self.gsheet_client.open_by_key(file.get('id'))
    #             self.rename_file_with_current_date()
    #             create_new_document = False
    #             break

    #         if not create_new_document:
    #             break

    #         page_token = lookup_file.get('nextPageToken', None)
    #         if page_token is None:
    #             break

    #     # IF THIS IS A NEW BENCH/EXTRUSION, CREATE A NEW SPREADSHEET
    #     if create_new_document:

    #         log('Creating new sheet')
    #         self.active_spreadsheet_object = self.gsheet_client.copy(self.master_sheet_key, title = self.active_spreadsheet_name, copy_permissions = True)
    #         self.active_spreadsheet_object.share('yetitool.com', perm_type='domain', role='writer')
    #         self.move_sheet_to_operator_resources()


    # def rename_file_with_current_date(self):

    #     file_metadata = {
    #         'name': "'" + self.active_spreadsheet_name + "'"
    #         }        

    #     file = self.drive_service.files().update(fileId=self.active_spreadsheet_id,
    #                                             body = file_metadata)



    # def move_sheet_to_operator_resources(self):

    #     log('Moving sheet to production > operator resources > live measurements')

    #     # Take the file ID and move it into the operator resources folder
    #     self.active_spreadsheet_id = self.active_spreadsheet_object.id

    #     # Retrieve the existing parents to remove
    #     file = self.drive_service.files().get(fileId=self.active_spreadsheet_id,
    #                                      fields='parents').execute()
    #     previous_parents = ",".join(file.get('parents'))
    #     # Move the file to the new folder
    #     file = self.drive_service.files().update(fileId=self.active_spreadsheet_id,
    #                                         addParents=self.squareness_measurements_id,
    #                                         removeParents=previous_parents,
    #                                         fields='id, parents').execute()


    # FUNCTION TO WRITE DATA TO WORKSHEET
    def write_to_worksheet(self):

        # INDICATE IF BENCH OR EXTRUSION
        calibration_data_worksheet_name =  'Calibration' + " - " + str(date.today()) + " - " + self.test_id.text

        # try: 
        #     # try accessing worksheet, which will work if it already exists
        #     worksheet = self.active_spreadsheet_object.worksheet(calibration_data_worksheet_name)
        #     log('Using existing worksheet ' + str(calibration_data_worksheet_name))

        # except:
        self.copy_template_worksheets_to_existing_spread()
        worksheet = self.active_spreadsheet_object.worksheet(calibration_data_worksheet_name)
        log('Using new worksheet ' + str(calibration_data_worksheet_name))

        # pre-clear data
        self.delete_existing_spreadsheet_data(calibration_data_worksheet_name)

        log("Writing calibration measurements to Gsheet")

        worksheet.update('A5:A', self.machine_Y_coordinate)
        worksheet.update('B5:B', self.HOME_raw_converted)
        worksheet.update('C5:C', self.FAR_raw_converted)
        worksheet.update('D5:D', self.HOME_distance_abs)
        worksheet.update('E5:E', self.FAR_distance_abs)
        worksheet.update('F5:F', self.Y_true)
        worksheet.update('G5:G', self.angle_off_square)
        worksheet.update('H5:H', self.delta_y_grbl_home)
        worksheet.update('I5:I', self.delta_y_grbl_far)
        worksheet.update('K5:K', self.Y_axis_linear_drift)
        worksheet.update('J5:J', self.Y_axis_angular_offset)
        worksheet.update('L5:L', self.delta_y_home)
        worksheet.update('M5:M', self.delta_y_far)
        worksheet.update('N5:N', self.DELTA_Y_X_BEAM)
        worksheet.update('O5:O', self.DELTA_Y_PER_METER)

        self.data_status ='Sent'
        log('Calibration test data sent')

        log("Recording test metadata")

        # Bench ID:
        worksheet.update('A2', str(self.bench_id.text))

        # Get time and date
        current_utc = datetime.utcnow()
        current_time = current_utc.strftime("%H:%M:%S")
        current_date = date.today()

        # Date
        worksheet.update('B2', str(current_date))
        
        # Time
        worksheet.update('C2', str(current_time))

        # Test no: 
        worksheet.update('D2', str(self.test_id.text))          

        # Bench width: 
        worksheet.update('E2', str(self.bench_width.text))

        # Travel:
        worksheet.update('F2', str(self.travel.text))

        log('Clear local test data')
        self.clear_data()
        self.test_id.text = str(int(self.test_id.text) + 1)

        self.go_stop.state = 'normal'
        self.go_stop.text = 'GO'
        self.go_stop.background_color = [0,0.502,0,1]


    def delete_existing_spreadsheet_data(self, worksheet_name):

        A_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "A5:A"
        B_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "B5:B"
        C_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "C5:C"
        D_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "D5:D"
        E_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "E5:E"
        F_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "F5:F"
        G_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "G5:G"
        H_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "H5:H"
        I_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "I5:I"
        J_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "J5:J"
        K_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "K5:K"
        L_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "L5:L"
        M_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "M5:M"
        N_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "N5:N"
        O_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "O5:O"

        self.active_spreadsheet_object.values_clear(A_str_to_clear)
        self.active_spreadsheet_object.values_clear(B_str_to_clear)
        self.active_spreadsheet_object.values_clear(C_str_to_clear)
        self.active_spreadsheet_object.values_clear(D_str_to_clear)
        self.active_spreadsheet_object.values_clear(E_str_to_clear)
        self.active_spreadsheet_object.values_clear(F_str_to_clear)
        self.active_spreadsheet_object.values_clear(G_str_to_clear)
        self.active_spreadsheet_object.values_clear(H_str_to_clear)
        self.active_spreadsheet_object.values_clear(I_str_to_clear)
        self.active_spreadsheet_object.values_clear(J_str_to_clear)
        self.active_spreadsheet_object.values_clear(K_str_to_clear)
        self.active_spreadsheet_object.values_clear(L_str_to_clear)
        self.active_spreadsheet_object.values_clear(M_str_to_clear)
        self.active_spreadsheet_object.values_clear(N_str_to_clear)
        self.active_spreadsheet_object.values_clear(O_str_to_clear)


    ## ENSURE SCREEN IS UPDATED TO REFLECT STATUS
    # update with general status information - DTI read & data sending info
    def update_screen(self, dt):

        self.data_status_label.text = self.data_status

        # show distance encoder thinks it's travelled on screen, to 3dp
        self.h_read_label.text = "{:.3f}".format(float(self.e0.H_side + self.e1.H_side)*encoder_resolution)
        self.f_read_label.text = "{:.3f}".format(float(self.e0.F_side + self.e1.F_side)*encoder_resolution)


