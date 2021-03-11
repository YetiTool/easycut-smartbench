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
from numpy import median

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
from asmcnc.skavaUI import widget_status_bar, widget_gcode_monitor

from asmcnc.production import micrometer, dti_widget_xy_move


USB0 = '/dev/ttyUSB0'
USB1 = '/dev/ttyUSB1'
y_length = float(2645 - 20)

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

# SET UP SCREEN

Builder.load_string("""

<ProcessMicrometerScreen>:

    status_container:status_container
    gcode_monitor_container:gcode_monitor_container
    move_container: move_container

    bench_id : bench_id 
    test_id : test_id
    travel : travel
    data_status_label : data_status_label
    h_read_label : h_read_label
    f_read_label : f_read_label

    prep_test : prep_test
    go_stop : go_stop
    calibrate_stop : calibrate_stop


    # test_type_toggle:test_type_toggle
    # side_toggle:side_toggle
    # send_data_button:send_data_button
    # home_data_status_label:home_data_status_label
    # far_data_status_label:far_data_status_label
    # dti_read_label:dti_read_label

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
                cols: 6
                cols_minimum: {0: 200, 1: 100, 2: 100, 3: 100, 4: 150, 5: 150}
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
                    text: "Data status:"
                    color: 0,0,0,1

                Label: 
                    text: "DTI Home"
                    color: 0,0,0,1

                Label: 
                    text: "DTI Far"
                    color: 0,0,0,1


                # Test setting inputs/buttons

                TextInput: 
                    id: bench_id 
                    text: "YB"
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

# ## OLD:                     
#             GridLayout: 
#                 pos: self.parent.pos
#                 size_hint_y: 0.15
#                 rows: 2
#                 cols: 8

#                 # Test set up labels

#                 Label: 
#                     text: "Bench ID"
#                     color: 0,0,0,1

#                 Label: 
#                     text: "Testing:"
#                     color: 0,0,0,1
#                 Label: 
#                     text: "Travel"
#                     color: 0,0,0,1
#                 Label: 
#                     text: "Test no."
#                     color: 0,0,0,1

#                 Label: 
#                     text: "Measuring:"
#                     color: 0,0,0,1

#                 Label: 
#                     text: "HOME DATA"
#                     color: 0,0,0,1

#                 Label: 
#                     text: "FAR DATA"
#                     color: 0,0,0,1

#                 Label:
#                     text: "DTI Read"
#                     color: 0,0,0,1

#                 # Test setting inputs/buttons

#                 TextInput: 
#                     id: bench_id 
#                     text: "id"
#                     multiline: False

#                 ToggleButton:
#                     id: test_type_toggle
#                     text: "EXTRUSION"
#                     on_press: root.toggle_test_type()

#                 TextInput: 
#                     id: travel
#                     text: "2500"
#                     input_filter: 'float'
#                     multiline: False

#                 TextInput: 
#                     id: test_id
#                     text: "1"
#                     input_filter: 'int'
#                     multiline: False

#                 ToggleButton:
#                     id: side_toggle
#                     text: "HOME SIDE"
#                     on_press: root.toggle_home_far()

#                 Label: 
#                     id: home_data_status_label
#                     text: "status"
#                     color: 0,0,0,1

#                 Label: 
#                     id: far_data_status_label
#                     text: "status"
#                     color: 0,0,0,1

#                 Label: 
#                     id: dti_read_label
#                     text: "-"
#                     color: 0,0,0,1

            GridLayout: 
                pos: self.parent.pos
                size_hint_y: 0.15
                rows: 1
                cols: 4
                spacing: 5

                # ToggleButton:
                #     id: home_stop
                #     text: "HOME"
                #     on_press: root.home_machine_pre_test()
                #     background_color: [0,0,0,1]
                #     background_normal: ''

                ToggleButton:
                    id: prep_test
                    text: "GET READY"
                    on_press: root.set_up_for_test()
                    background_color: [0,0,0,1]
                    background_normal: ''

                ToggleButton:
                    id: go_stop
                    text: "MEASURE"
                    on_press: root.run_stop_test()
                    background_color: [0,0,0,1]
                    background_normal: ''

                ToggleButton:
                    id: calibrate_stop
                    text: "CALIBRATE"
                    on_press: root.run_stop_test()
                    background_color: [0,0,0,1]
                    background_normal: ''

                # Button:
                #     text: "RESET DATA"
                #     on_press: root.clear_data()
                
                # Button:
                #     id: send_data_button
                #     text: "SEND DATA"
                #     on_press: root.send_data()

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

class ProcessMicrometerScreen(Screen):

    # CALIBRATORS AND CONSTANTS
    Calibration_list = []
    translation_from_jig_to_Y_pos = 0
    arbitrary_width_constant = 1

    # LISTS TO HOLD RAW RECORDED DATA
    jig_pos_list = []
    DTI_read_home = []
    DTI_read_far = []

    # LISTS FOR NORMALIZED DATA (against median value)
    Y_pos = []
    HOME_normalized = []
    FAR_normalized = []

    # LISTS FOR DATA THAT GOES TO GOOGLE SHEETS
    jig_position_converted = []
    y_pos_converted = []
    calibration_list_converted = []
    home_raw_converted = []
    far_raw_converted = []
    home_measurement_converted = []
    far_measurement_converted = []

    # TEST PARAMETERS
    starting_jig_pos = 0
    max_pos = 0
    DTI_initial_value_home = 0
    DTI_initial_value_far = 0

    # TEMPLATE SHEET THAT SHEET FORMAT IS COPIED FROM
    master_sheet_key = '1y1Rq29icpISFIGvaygeI-jye40V_g5lE2NIVgMf_cI8'

    # FOLDER ID TO COLLATE RESULTS
    live_measurements_id = '15iBk8f-_VqnOwfOuWBJQBgTFznjY_TQu'

    # GOOGLE API OBJECTS
    gsheet_client = None
    drive_service = None

    active_folder_id = ''
    active_spreadsheet_object = None
    active_spreadsheet_name = ''
    active_spreadsheet_id = ''

    # STATUS FLAGS
    data_status = 'Ready'

    # READ IN VALUE
    home_dti_read = ''
    far_dti_read = ''

    # SET UP KIVY CLOCK EVENT OBJECTS
    poll_for_screen = None

    def __init__(self, **kwargs):

        super(ProcessMicrometerScreen, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        # WIDGET SETUP
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))
        self.gcode_monitor_container.add_widget(widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.sm))
        self.move_container.add_widget(dti_widget_xy_move.DTIJigXYMove(machine=self.m, screen_manager=self.sm))

        ## GSHEET SETUP
        if sys.platform != 'win32' and sys.platform != 'darwin':
            scope = [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/drive.file'
                ]
            file_name = os.path.dirname(os.path.realpath(__file__)) + '/keys/live-measurements-api-key.json'
            creds = service_account.Credentials.from_service_account_file(file_name, scopes=scope)
            self.drive_service = build('drive', 'v3', credentials=creds)
            self.gsheet_client = gspread.authorize(creds)

        # MICROMETER CONNECTION
        self.DTI_H = micrometer.micrometer(USB0)
        self.DTI_F = micrometer.micrometer(USB1)

    def on_enter(self):

        self.poll_for_screen = Clock.schedule_interval(self.update_screen, 0.2)
        if self.m.is_machine_homed:
            self.prep_test.background_color = [0,0.502,0,1]

        # TURNS BUTTON GREEN IF DTI IS CONNECTED
        if self.DTI_H != None and self.DTI_F != None:
            self.go_stop.background_color = [0,0.502,0,1]
            self.calibrate_stop.background_color = [0,0.502,0,1]

        self.go_stop.state == 'normal'
        self.go_stop.text = 'MEASURE'

        self.calibrate_stop.state == 'normal'
        self.calibrate_stop.text = 'CALIBRATE'


    def go_to_lobby(self):
        self.sm.current = 'developer_temp'


    # TEST SET UP
    def  set_up_for_test(self):
        self.home_machine_pre_test()
        # might also want to add a command that takes the jig to a start point - 
        # perhaps in line with the first metal datum? 


    # HOME FUNCTION

    def home_machine_pre_test(self):

        if self.prep_test.state == 'down':

            ## CHANGE BUTTON
            self.prep_test.background_color = [1,0,0,1]
            self.prep_test.text = 'STOP'

            normal_homing_sequence = ['$H']
            self.m.s.start_sequential_stream(normal_homing_sequence)

            self.check_for_home_end_event = Clock.schedule_interval(self.check_home_completion, 3)

        elif self.prep_test.state == 'normal':

            # CANCEL HOMING
            self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
            self.m.reset_on_cancel_homing()

            self.prep_test.text = 'GET READY'
            self.prep_test.background_color = [0,0.502,0,1]

    # update home button when homing has finished
    def check_home_completion(self, dt):

        if not self.m.s.is_sequential_streaming:
            Clock.unschedule(self.check_for_home_end_event)
            self.prep_test.text = 'GET READY'
            self.prep_test.background_color = [0,0.502,0,1]
            self.prep_test.state = 'normal'


    # MACHINE RUN TEST FUNCTIONS

    def run_stop_test(self):

        if self.go_stop.state == 'down':

            ## CHANGE BUTTON
            self.go_stop.background_color = [1,0,0,1]
            self.go_stop.text = 'STOP'

            ## SET VARIABLES
            self.clear_data()
            self.starting_jig_pos = float(self.m.mpos_x())
            self.max_pos = self.set_max_pos()

            ## START THE TEST
            log('Starting test...')
            self.data_status = 'Collecting'
            run_command = 'G0 G91 X' + str(self.max_pos)
            self.m.send_any_gcode_command(run_command)
            self.test_run = Clock.schedule_interval(self.do_test_step, 0.1)

        elif self.go_stop.state == 'normal':
            log('Cancel from button')
            self.end_of_test_sequence()

            if self.m.state() == 'Run':
                self.m.soft_stop()
                self.m.stop_from_soft_stop_cancel()

    def end_of_test_sequence(self):

        Clock.unschedule(self.test_run)
        self.data_status = 'Collected'
        self.go_stop.background_color = [0,0.502,0,1]
        self.go_stop.text = 'MEASURE'
        self.go_stop.state = 'normal'

    def set_max_pos(self):
        return self.starting_pos - float(self.travel.text)

    def do_test_step(self, dt):

        if self.m.mpos_x() >= self.max_pos:
            self.jig_pos_list.append(float(self.m.mpos_x()))
            self.DTI_read_home.append(float(self.DTI_H.read_mm()))
            self.DTI_read_far.append(float(self.DTI_F.read_mm()))

        else:
            log('Cancel from test step')
            self.end_of_test_sequence()


    # CLEAR (RESET) LOCAL DATA (DOES NOT AFFECT ANYTHING ALREADY SENT TO SHEETS)
    def clear_data(self, clearall = False):

        # LISTS TO HOLD RAW RECORDED DATA
        self.jig_pos_list = []
        self.DTI_read_home = []
        self.DTI_read_far = []

        # LISTS FOR NORMALIZED DATA (against median value)
        self.Y_pos = []
        self.HOME_normalized = []
        self.FAR_normalized = []

        # LISTS FOR DATA THAT GOES TO GOOGLE SHEETS
        self.jig_position_converted = []
        self.y_pos_converted = []
        self.calibration_list_converted = []
        self.home_raw_converted = []
        self.far_raw_converted = []
        self.home_measurement_converted = []
        self.far_measurement_converted = []

        # TEST PARAMETERS
        self.starting_jig_pos = 0
        self.max_pos = 0
        self.DTI_initial_value_home = 0
        self.DTI_initial_value_far = 0

        self.data_status = 'Cleared'


    ## SENDING DATA

    # MAIN FUNCTION CALLED BY BUTTON
    def send_data(self):

        # screen needs to be updated before sending data
        # as data sending is an intensive process and locks up kivy
        self.data_status = 'Sending'

        # start main data sending processes after 2 seconds
        Clock.schedule_once(self.do_data_send, 2)


    def do_data_send(self, dt):

        self.active_spreadsheet_name = self.bench_id.text + ' - ' + str(date.today()) + ' - ' + str(self.test_id.text)
        self.format_output()
        self.open_spreadsheet() # I.E. OPEN GOOGLE SHEETS DOCUMENT
        self.write_to_worksheet()

        try: self.write_to_worksheet()
        except: 
            Clock.schedule_once(lambda dt: self.write_to_worksheet(), 10)
            log('Failed to write to sheet, trying again in 10 seconds')

    # GOOGLE SHEETS DATA FORMATTING FUNCTIONS
    # NEEDS REDOING
    def format_output(self):


        # LISTS TO HOLD RAW RECORDED DATA
        self.jig_pos_list = []
        self.DTI_read_home = []
        self.DTI_read_far = []

        # LISTS FOR NORMALIZED DATA (against median value)
        self.Y_pos = []
        self.HOME_normalized = []
        self.FAR_normalized = []

        # LISTS FOR DATA THAT GOES TO GOOGLE SHEETS
        self.jig_position_converted = []
        self.y_pos_converted = []
        self.calibration_list_converted = []
        self.home_raw_converted = []
        self.far_raw_converted = []
        self.home_measurement_converted = []
        self.far_measurement_converted = []

        # TEST PARAMETERS
        self.starting_pos = 0
        self.max_pos = 0
        self.DTI_initial_value_home = 0
        self.DTI_initial_value_far = 0


        # self.starting_jig_pos

        # x axis has to be a continuous list for both datasets to be mapped against, so both sets of data have to be conjoined
        x_axis = []
        raw_data = []
        self.all_dti_measurements = []
        self.raw_dti_measurements = []

        try: 
            # normalize against median value
            HOME_NORMALIZATION_VALUE = median(self.HOME_DTI_abs_list)
            self.HOME_normalized = [(H - HOME_NORMALIZATION_VALUE) for H in self.HOME_DTI_abs_list]
            x_axis.extend(self.HOME_normalized)
            raw_data.extend(self.HOME_DTI_abs_list)

        except: 
            self.HOME_normalized = []

        try: 
            # normalize against median value
            FAR_NORMALIZATION_VALUE = median(self.FAR_DTI_abs_list)
            self.FAR_normalized = [-1*(F - FAR_NORMALIZATION_VALUE) for F in self.FAR_DTI_abs_list]
            x_axis.extend(self.FAR_normalized)
            raw_data.extend(self.FAR_DTI_abs_list)

        except: 
            self.FAR_normalized = []

        self.all_dti_measurements = self.convert_to_json(x_axis)
        self.raw_dti_measurements = self.convert_to_json(raw_data)

        #  both positional datasets need to be the same length, so that both y series can be mapped to the same x axis. 
        try:

            # multiply by -1 for google sheets display purposes
            HOME_y_pos_raw = [(-1*POS) for POS in self.HOME_Y_pos_list]

            # extend data to match length of FAR data
            data_extension = len(self.FAR_Y_pos_list)*['']
            HOME_y_pos_raw.extend(data_extension)

        except: 
            HOME_y_pos_raw = []

        try:
            # offset data to match length of FAR data
            FAR_y_pos_raw = len(self.HOME_Y_pos_list)*['']

            # specific to far pos - coordinates need flipping because far side is flipped
            # # this gives out coord as positive value, which is great for google sheets display purposes
            FAR_y_pos_raw.extend([(y_length + POS) for POS in self.FAR_Y_pos_list])

        except: 
            FAR_y_pos_raw = []

        self.HOME_Y_pos_list_converted = self.convert_to_json(HOME_y_pos_raw)
        self.FAR_Y_pos_list_converted = self.convert_to_json(FAR_y_pos_raw)


    def convert_to_json(self, data):
        # Need to convert to json format in order to export to gsheets

        new_data = []

        data = [str(x).split() for x in data]

        for list in data:
            new_list_item = [float(e) for e in list]
            new_data.append(new_list_item)

        return new_data


    # FUNCTIONS TO MANAGE SPREADSHEET - OPENING AND MOVING

    def open_spreadsheet(self):

        if self.look_for_existing_folder():
            if self.look_for_existing_file(): pass
            else: self.create_new_document()

        else:
            self.create_new_folder()
            self.create_new_document()


    def look_for_existing_folder(self):

        # FOLDER SEARCH

        # this is the query that gets passed to the files.list function, and looks for files in the straigtness measurements folder
        # and with a name that contains the current bench id
        folder_q_str = "'" + self.live_measurements_id + "'" + " in parents and name = " + "'" + self.bench_id.text + "'" + \
         ' and ' + "mimeType = 'application/vnd.google-apps.folder'"
        folder_page_token = None

        while True:
            log('Looking for existing folder to send data to...')
            lookup_folder = self.drive_service.files().list(q=folder_q_str,
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=folder_page_token).execute()

            for file in lookup_folder.get('files', []):
                log('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
                self.active_folder_id = file.get('id')
                return True

            folder_page_token = lookup_folder.get('nextPageToken', None)
            if folder_page_token is None:
                self.active_folder_id = ''
                return False


    def look_for_existing_file(self):

        # GO INTO FOLDER AND LIST FILES:
        log('Filename: ' + self.active_spreadsheet_name)
        file_q_str = "'" + self.active_folder_id + "'" + " in parents and name = " + "'" + self.active_spreadsheet_name + "'"
        document_page_token = None

        while True:
            log('Looking for existing file to send data to...')
            lookup_file = self.drive_service.files().list(q=file_q_str,
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=document_page_token).execute()

            for file in lookup_file.get('files', []):
                self.active_spreadsheet_object = self.gsheet_client.open_by_key(file.get('id'))
                return True

            document_page_token = lookup_file.get('nextPageToken', None)
            if document_page_token is None:
                return False


    def create_new_folder(self):

        folder_metadata = {
            'name': self.bench_id.text,
            'mimeType': 'application/vnd.google-apps.folder',
        }

        folder = self.drive_service.files().create(body=folder_metadata,
                                            fields='id').execute()
        self.active_folder_id = folder.get('id')
        log('Found folder: ' + str(folder.get('id')))

        # Remove the API service bot's default parents, which will hopefully enable access
        folder = self.drive_service.files().get(fileId=self.active_folder_id,
                                            fields='parents').execute()

        previous_parents = ",".join(folder.get('parents'))
        # Move the file to the new folder
        folder = self.drive_service.files().update(fileId=self.active_folder_id,
                                            addParents=self.live_measurements_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()


    def create_new_document(self):
        log('Creating new document')
        self.active_spreadsheet_object = self.gsheet_client.copy(self.master_sheet_key, title = self.active_spreadsheet_name, copy_permissions = True)
        self.active_spreadsheet_object.share('yetitool.com', perm_type='domain', role='writer')
        self.move_document_to_bench_folder()


    def move_document_to_bench_folder(self):

        log("Moving document to production > operator resources > live measurements > [serial_number]")

        # Take the file ID and move it into the folder for the bench (named by serial number)

        # Retrieve the existing parents to remove
        file = self.drive_service.files().get(fileId=self.active_spreadsheet_object.id,
                                         fields='parents').execute()

        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = self.drive_service.files().update(fileId=self.active_spreadsheet_object.id,
                                            addParents=self.active_folder_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()

    # FUNCTION TO WRITE DATA TO WORKSHEET
    def write_to_worksheet(self):

        # INDICATE IF BENCH OR EXTRUSION
        test_data_worksheet_name = 'Straightness Data'

        try: 
            # try accessing worksheet, which will work if it already exists
            worksheet = self.active_spreadsheet_object.worksheet(test_data_worksheet_name)
            log('Using worksheet ' + str(test_data_worksheet_name))

        except:
            id_to_copy_from = (self.active_spreadsheet_object.worksheets()[0]).id
            # if worksheet for this test does not exist yet, create a new one
            worksheet = self.active_spreadsheet_object.duplicate_sheet(id_to_copy_from, insert_sheet_index=None, new_sheet_id=None, new_sheet_name=test_data_worksheet_name)

            # need to clear data if duplicating sheets
            self.delete_existing_spreadsheet_data(test_data_worksheet_name)

            log('Created worksheet ' + str(test_data_worksheet_name))

            # delete Sheet1 if it exists (for sake of tidyness)
            try: self.active_spreadsheet_object.del_worksheet(self.active_spreadsheet_object.worksheet('Sheet1'))
            except: pass

        log("Writing DTI measurements to Gsheet")

        worksheet.update('B4:B' , self.raw_dti_measurements)
        worksheet.update('C4:C', self.all_dti_measurements)

        if self.HOME_Y_pos_list != []:
            worksheet.update('D4:D', self.HOME_Y_pos_list_converted)
            self.home_data_status = 'Sent'
            log('Home side data sent')

        if self.FAR_Y_pos_list != []:
            worksheet.update('E4:E', self.FAR_Y_pos_list_converted)
            self.far_data_status = 'Sent'
            log('Far side data sent')

        log("Recording test metadata")

        current_utc = datetime.utcnow()
        current_time = current_utc.strftime("%H:%M:%S")
        current_date = date.today()
        # Date
        worksheet.update('A2', str(current_date))
        # Time
        worksheet.update('A4', str(current_time))
        # Bench ID:
        worksheet.update('A6', str(self.bench_id.text))
        # Test Type:
        worksheet.update('A8', str(self.test_type))
        # Test no: 
        worksheet.update('A10', str(self.test_id.text))  

        if ((self.HOME_Y_pos_list != []) and (self.FAR_Y_pos_list != [])):
            self.last_bench = self.bench_id.text
            self.last_test = self.test_id.text
            self.test_id.text = str(int(self.last_test) + 1)
            self.clear_data(clearall = True)

        log('Finished writing data')

        self.go_stop.state = 'normal'
        self.go_stop.text = 'MEASURE'
        self.go_stop.background_color = [0,0.502,0,1]


    def delete_existing_spreadsheet_data(self, worksheet_name):

        B_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "B4:B"
        C_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "C4:C"
        D_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "D4:D"
        E_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "E4:E"

        self.active_spreadsheet_object.values_clear(B_str_to_clear)
        self.active_spreadsheet_object.values_clear(C_str_to_clear)
        self.active_spreadsheet_object.values_clear(D_str_to_clear)
        self.active_spreadsheet_object.values_clear(E_str_to_clear)


    ## ENSURE SCREEN IS UPDATED TO REFLECT STATUS
    # update with general status information - DTI read & data sending info

    def update_screen(self, dt):

        self.data_status_label.text = self.data_status
        self.h_read_label.text = str(self.DTI_H.read_mm())
        self.f_read_label.text = str(self.DTI_F.read_mm())


    def on_leave(self):

        if self.poll_for_screen != None:
            Clock.unschedule(self.poll_for_screen)























