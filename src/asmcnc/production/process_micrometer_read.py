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

            GridLayout: 
                pos: self.parent.pos
                size_hint_y: 0.15
                rows: 1
                cols: 4
                spacing: 5

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

    # HARDWARE PARAMETERS
    ## will need final jig to measure these
    X_start_coordinate = -1260
    translation_from_jig_to_Y_pos = 0
    y_length = float(2645 - 20)

    # CALIBRATORS AND CONSTANTS
    Calibration_list_home = []
    Calibration_list_far = []
    arbitrary_width_constant = 1

    # LISTS TO HOLD RAW RECORDED DATA
    jig_pos_list = []
    DTI_read_home = []
    DTI_read_far = []

    # LISTS FOR DATA THAT GOES TO GOOGLE SHEETS
    jig_position_converted = []
    y_pos_converted = []
    calibration_list_converted = []
    home_raw_converted = []
    far_raw_converted = []
    home_measurement_converted = []
    far_measurement_converted = []
    home_with_offset_converted = []
    far_with_offset_converted = []

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
    test_completed = False

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

        # TURNS BUTTON GREEN IF DTI IS CONNECTED
        if self.DTI_H != None and self.DTI_F != None:
            self.prep_test.background_color = [0,0.502,0,1]

        self.go_stop.state == 'normal'
        self.go_stop.text = 'MEASURE'

        self.calibrate_stop.state == 'normal'
        self.calibrate_stop.text = 'CALIBRATE'


    def go_to_lobby(self):
        self.sm.current = 'developer_temp'

    def on_leave(self):
        if self.poll_for_screen != None:
            Clock.unschedule(self.poll_for_screen)


    # TEST SET UP
    def  set_up_for_test(self):
        self.home_machine_pre_test()
        # the check home event (set up in homing function) then also sends command to set specific X coordinate when homing complete

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
            self.m.jog_absolute_single_axis('X', self.X_start_coordinate, 3000)
            self.prep_test.text = 'GET READY'
            self.prep_test.background_color = [0,0.502,0,1]
            self.prep_test.state = 'normal'
            self.go_stop.background_color = [0,0.502,0,1]
            self.calibrate_stop.background_color = [0,0.502,0,1]


    # MACHINE RUN TEST FUNCTIONS

    def run_stop_test(self):

        # TEST GETS STARTED
        if self.go_stop.state == 'down':

            ## CHANGE BUTTON
            self.go_stop.background_color = [1,0,0,1]
            self.go_stop.text = 'STOP'

            ## SET VARIABLES
            self.clear_data()
            self.starting_jig_pos = float(self.m.mpos_x())
            self.DTI_initial_value_home = float(self.DTI_H.read_mm())
            self.DTI_initial_value_far = float(self.DTI_F.read_mm())
            self.max_pos = self.set_max_pos()

            ## START THE TEST
            log('Starting test...')
            self.test_completed = False
            self.data_status = 'Collecting'
            run_command = 'G0 G91 X' + str(self.max_pos)
            self.m.send_any_gcode_command(run_command)
            self.test_run = Clock.schedule_interval(self.do_test_step, 0.1)

        # TEST GETS STOPPED PREMATURELY
        elif self.go_stop.state == 'normal':

            log('Test cancelled')
            self.test_completed = False
            self.end_of_test_sequence()

            if self.m.state() == 'Run':
                self.m.soft_stop()
                self.m.stop_from_soft_stop_cancel()

    def end_of_test_sequence(self):

        Clock.unschedule(self.test_run)
        self.go_stop.background_color = [0,0.502,0,1]
        self.go_stop.text = 'MEASURE'
        self.go_stop.state = 'normal'

        if self.test_completed:
            self.data_status = 'Collected'
            Clock.schedule_once(lambda dt: self.send_data(), 1)
        else: 
            self.data_status = 'Test cancelled'
            self.clear_data()


    def set_max_pos(self):
        return self.starting_jig_pos - float(self.travel.text)

    def do_test_step(self, dt):

        if self.m.mpos_x() >= self.max_pos:
            self.jig_pos_list.append(float(self.m.mpos_x()))
            self.DTI_read_home.append(float(self.DTI_H.read_mm()))
            self.DTI_read_far.append(float(self.DTI_F.read_mm()))

        else:
            log('Test finished')
            self.test_completed = True
            self.end_of_test_sequence()


    # CALIBRATION
    def calibrate_straightness_jig(self):
        pass


    # CLEAR (RESET) LOCAL DATA (DOES NOT AFFECT ANYTHING ALREADY SENT TO SHEETS)
    def clear_data(self, clearall = False):

        # LISTS TO HOLD RAW RECORDED DATA
        self.jig_pos_list = []
        self.DTI_read_home = []
        self.DTI_read_far = []

        # LISTS FOR DATA THAT GOES TO GOOGLE SHEETS
        self.jig_position_converted = []
        self.y_pos_converted = []
        self.calibration_list_converted = []
        self.home_raw_converted = []
        self.far_raw_converted = []
        self.home_measurement_converted = []
        self.far_measurement_converted = []
        self.home_with_offset_converted = []
        self.far_with_offset_converted = []

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

        ## adjust data: convert, adjust to baseline and calibration. 

        # convert jig coordinates into associated y coordinates
        Y_pos = [((-1*x) - self.translation_from_jig_to_Y_pos) for x in self.jig_pos_list]

        # adjust by calibration values
        # this needs checking - need to think about the way that calibration works, and how to "bin" data
        # and will need function to scrape the calibration data
        # HOME_baseline_corrected = list(map(lambda h, c: h - float(self.DTI_initial_value_home) + c, self.DTI_read_home, self.Calibration_list_home))
        # # multiply far side by -1 for symmetry
        # FAR_baseline_corrected = list(map(lambda f, c: -1*(f - float(self.DTI_initial_value_far) + c), self.DTI_read_far, self.Calibration_list_far))

        # for debugging
        HOME_baseline_corrected = list(map(lambda h: h - float(self.DTI_initial_value_home), self.DTI_read_home))
        # multiply far side by -1 for symmetry
        FAR_baseline_corrected = list(map(lambda f: -1*(f - float(self.DTI_initial_value_far)), self.DTI_read_far))
        
        # add arbitrary width so that bench shape is visible on graphs
        HOME_with_offset = [(arbitrary_width_constant + m) for m in HOME_baseline_corrected]
        FAR_with_offset = [(-arbitrary_width_constant - n) for n in FAR_baseline_corrected]

        ## convert to json format for API:
        self.jig_position_converted = self.convert_to_json(self.jig_pos_list)
        self.y_pos_converted = self.convert_to_json(Y_pos)
        self.home_calibration_list_converted = self.convert_to_json(self.Calibration_list_home)
        self.far_calibration_list_converted = self.convert_to_json(self.Calibration_list_far)
        self.home_raw_converted = self.convert_to_json(self.DTI_read_home)
        self.far_raw_converted = self.convert_to_json(self.DTI_read_far)
        self.home_measurement_converted = self.convert_to_json(HOME_baseline_corrected)
        self.far_measurement_converted = self.convert_to_json(FAR_baseline_corrected)
        self.home_with_offset_converted = self.convert_to_json(HOME_with_offset)
        self.far_with_offset_converted = self.convert_to_json(FAR_with_offset)


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
        straightness_data_worksheet_name = 'Straightness Data'

        worksheet = self.active_spreadsheet_object.worksheet(straightness_data_worksheet_name)
        log('Using new worksheet ' + str(straightness_data_worksheet_name))

        # pre-clear data (this includes any rows that just contain dummy data to force the charts to work)
        self.delete_existing_spreadsheet_data(straightness_data_worksheet_name)

        log("Writing straightness measurements to Gsheet")

        worksheet.update('A5:A', self.jig_position_converted)
        worksheet.update('B5:B', self.y_pos_converted)
        worksheet.update('C5:C', self.home_calibration_list_converted)
        worksheet.update('D5:D', self.far_calibration_list_converted)
        worksheet.update('E5:E', self.home_raw_converted)
        worksheet.update('F5:F', self.far_raw_converted)
        worksheet.update('G5:G', self.home_measurement_converted)
        worksheet.update('H5:H', self.far_measurement_converted)
        worksheet.update('I5:I', self.home_with_offset_converted)
        worksheet.update('K5:K', self.far_with_offset_converted)

        log('Straightness test data sent')
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

        # Travel:
        worksheet.update('E2', str(self.travel.text))

        # DTI initial value home side
        worksheet.update('F2', str(self.DTI_initial_value_home))

        # DTI initial value far side
        worksheet.update('G2', str(self.DTI_initial_value_far))

        self.data_status ='Sent'
        log('Clear local test data')
        self.clear_data()
        self.test_id.text = str(int(self.test_id.text) + 1)

        self.go_stop.state = 'normal'
        self.go_stop.text = 'MEASURE'
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


    ## ENSURE SCREEN IS UPDATED TO REFLECT STATUS
    # update with general status information - DTI read & data sending info

    def update_screen(self, dt):

        self.data_status_label.text = self.data_status
        self.h_read_label.text = str(self.DTI_H.read_mm())
        self.f_read_label.text = str(self.DTI_F.read_mm())






















