'''
Module to process readings from DTI, and send to Production > Operator Resources > Live Measurements > Straightness Data
'''
import os
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

from asmcnc.production import micrometer


PORT = '/dev/ttyUSB0'
DTI = micrometer.micrometer(PORT)
y_length = float(2645 - 20)

# reading = DTI.read_mm()

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

# SET UP SCREEN

Builder.load_string("""

<ProcessMicrometerScreen>:

    status_container:status_container
    gcode_monitor_container:gcode_monitor_container
    move_container: move_container
    bench_id:bench_id 
    test_id:test_id
    travel:travel
    go_stop: go_stop
    home_stop:home_stop
    test_type_toggle:test_type_toggle
    side_toggle:side_toggle
    send_data_button:send_data_button
    home_data_status_label:home_data_status_label
    far_data_status_label:far_data_status_label
    dti_read_label:dti_read_label

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
                cols: 8

                # Test set up labels

                Label: 
                    text: "Bench ID"
                    color: 0,0,0,1

                Label: 
                    text: "Testing:"
                    color: 0,0,0,1
                Label: 
                    text: "Travel"
                    color: 0,0,0,1
                Label: 
                    text: "Test no."
                    color: 0,0,0,1

                Label: 
                    text: "Measuring:"
                    color: 0,0,0,1

                Label: 
                    text: "HOME DATA"
                    color: 0,0,0,1

                Label: 
                    text: "FAR DATA"
                    color: 0,0,0,1

                Label:
                    text: "DTI Read"
                    color: 0,0,0,1

                # Test setting inputs/buttons

                TextInput: 
                    id: bench_id 
                    text: "default"
                    multiline: False

                ToggleButton:
                    id: test_type_toggle
                    text: "EXTRUSION"
                    on_press: root.toggle_test_type()

                TextInput: 
                    id: travel
                    text: "2500"
                    input_filter: 'float'
                    multiline: False

                TextInput: 
                    id: test_id
                    text: "1"
                    input_filter: 'int'
                    multiline: False

                ToggleButton:
                    id: side_toggle
                    text: "HOME SIDE"
                    on_press: root.toggle_home_far()

                Label: 
                    id: home_data_status_label
                    text: "status"
                    color: 0,0,0,1

                Label: 
                    id: far_data_status_label
                    text: "status"
                    color: 0,0,0,1

                Label: 
                    id: dti_read_label
                    text: "-"
                    color: 0,0,0,1

            GridLayout: 
                pos: self.parent.pos
                size_hint_y: 0.15
                rows: 1
                cols: 5
                spacing: 5

                ToggleButton:
                    id: home_stop
                    text: "HOME"
                    on_press: root.home_machine_pre_test()
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
                    id: send_data_button
                    text: "SEND DATA"
                    on_press: root.send_data()

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

    HOME_Y_pos_list = []
    HOME_DTI_abs_list = []

    HOME_DTI_abs_list_converted = []
    FAR_DTI_abs_list_converted = []

    HOME_zeroed_converted = []
    FAR_zeroed_converted = []

    FAR_Y_pos_list = []
    FAR_DTI_abs_list = []

    HOME_SIDE = True
    test_type = 'BENCH'
    starting_pos = 0
    max_pos = 0

    DTI_initial_value = 0

    send_home_data = False
    send_far_data = False

    # TEMPLATE SHEET THAT SHEET FORMAT IS COPIED FROM
    master_sheet_key = '10jyrzSH-_pvieqFW7TTF3JvU786XXVzwrPR-nx0Lx_o'

    # FOLDER ID TO COLLATE RESULTS
    straightness_measurements_id = '12H3XlLc876qia0i9s1a8FQCo7rK7fUzl'

    gsheet_client = None
    drive_service = None

    active_spreadsheet_object = None
    active_spreadsheet_name = ''
    active_spreadsheet_id = ''

    last_bench = ''
    last_test = ''

    # STATUS FLAGS
    home_data_status = 'Ready'
    far_data_status = 'Ready'
    dti_read = ''

    poll_for_screen = None

    def __init__(self, **kwargs):

        super(ProcessMicrometerScreen, self).__init__(**kwargs)

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        # WIDGET SETUP
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))
        self.gcode_monitor_container.add_widget(widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.sm))
        self.move_container.add_widget(widget_xy_move.XYMove(machine=self.m, screen_manager=self.sm))

        ## GSHEET SETUP
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
            ]
        file_name = os.path.dirname(os.path.realpath(__file__)) + '/keys/live-measurements-api-key.json'
        creds = service_account.Credentials.from_service_account_file(file_name, scopes=scope)
        self.drive_service = build('drive', 'v3', credentials=creds)
        self.gsheet_client = gspread.authorize(creds)

    def on_enter(self):

        self.poll_for_screen = Clock.schedule_interval(self.update_screen, 0.2)

        self.home_stop.background_color = [0,0.502,0,1]

        # TURNS BUTTON GREEN IF DTI IS CONNECTED
        if DTI != None:
            self.go_stop.background_color = [0,0.502,0,1]

        self.toggle_home_far()
        self.toggle_test_type()

    def go_to_lobby(self):
        self.sm.current = 'developer_temp'


    # TEST SET UP

    def toggle_home_far(self):

        if self.side_toggle.state == 'down':
            self.side_toggle.background_color = [0,1,0,1]
            self.side_toggle.text = 'FAR SIDE'
            self.HOME_SIDE = False

        elif self.side_toggle.state == 'normal':
            self.side_toggle.background_color = [0,0,1,1]
            self.side_toggle.text = 'HOME SIDE'
            self.HOME_SIDE = True


    def toggle_test_type(self):

        if self.test_type_toggle.state == 'down':
            self.test_type_toggle.background_color = [0,1,0,1]
            self.test_type = 'BENCH'
            self.test_type_toggle.text = self.test_type

        elif self.test_type_toggle.state == 'normal':
            self.test_type_toggle.background_color = [0,0,1,1]
            self.test_type = 'EXTRUSION'
            self.test_type_toggle.text = self.test_type


    # HOME FUNCTION

    def home_machine_pre_test(self):

        if self.home_stop.state == 'down':

            ## CHANGE BUTTON
            self.home_stop.background_color = [1,0,0,1]
            self.home_stop.text = 'STOP'

            normal_homing_sequence = ['$H']
            self.m.s.start_sequential_stream(normal_homing_sequence)

            self.check_for_home_end_event = Clock.schedule_interval(self.check_home_completion, 3)

        elif self.home_stop.state == 'normal':

            # CANCEL HOMING
            self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
            self.m.reset_on_cancel_homing()

            self.home_stop.text = 'HOME'
            self.home_stop.background_color = [0,0.502,0,1]


    # MACHINE RUN TEST FUNCTIONS

    def run_stop_test(self):

        if self.go_stop.state == 'down':

            ## CHANGE BUTTON
            self.go_stop.background_color = [1,0,0,1]
            self.go_stop.text = 'STOP'

            ## SET VARIABLES
            self.clear_data()
            self.starting_pos = float(self.m.mpos_y())
            DTI_initial_value = DTI.read_mm()
            self.max_pos = self.set_max_pos()

            ## START THE TEST
            self.test_run = Clock.schedule_interval(self.do_test_step, 1)

            if self.HOME_SIDE:
                self.home_data_status = 'Collecting'
            else:
                self.far_data_status = 'Collecting'

        elif self.go_stop.state == 'normal':
            self.end_of_test_sequence()


    def end_of_test_sequence(self):

        Clock.unschedule(self.test_run)

        if self.HOME_SIDE:
            self.home_data_status = 'Collected'
        else:
            self.far_data_status = 'Collected'

        self.go_stop.background_color = [0,0.502,0,1]
        self.go_stop.text = 'GO'
        self.go_stop.state = 'normal'


    def set_max_pos(self):
        return self.starting_pos + float(self.travel.text)


    def do_test_step(self, dt):

        if self.m.state() == 'Run':
            pass

        elif self.m.state() == 'Idle' and self.m.mpos_y() <= self.max_pos:

            if self.HOME_SIDE: 
                self.HOME_Y_pos_list.append(float(self.m.mpos_y()))
                self.HOME_DTI_abs_list.append(float(DTI.read_mm()))

            else:
                self.FAR_Y_pos_list.append(float(self.m.mpos_y()))
                self.FAR_DTI_abs_list.append(float(DTI.read_mm()))

            self.m.send_any_gcode_command('G0 G91 Y10')

        elif self.m.state() == 'Idle' and self.m.mpos_y() > self.max_pos:
            self.end_of_test_sequence()

        else: 
            Clock.unschedule(self.test_run)
            self.go_stop.state = 'normal'
            self.go_stop.text = 'GO'
            self.go_stop.background_color = [0,0.502,0,1]


    # CLEAR (RESET) LOCAL DATA (DOES NOT AFFECT ANYTHING ALREADY SENT TO SHEETS)

    def clear_data(self, clearall = False):

        if self.HOME_SIDE:

            self.HOME_DTI_abs_list = []
            self.HOME_Y_pos_list = []

            self.HOME_abs_initial_value = 0
            self.HOME_zeroed_list = []
            self.HOME_Y_pos_list_converted = []
            self.HOME_DTI_abs_list_converted = []
            self.HOME_zeroed_converted = []
            self.home_data_status = 'Cleared'

        else:

            self.FAR_DTI_abs_list = []
            self.FAR_Y_pos_list = []

            self.FAR_abs_initial_value = 0
            self.FAR_zeroed_list = []
            self.FAR_Y_pos_list_converted = []
            self.FAR_DTI_abs_list_converted = []
            self.FAR_zeroed_converted = []
            self.far_data_status = 'Cleared'


        if clearall: 

            self.HOME_DTI_abs_list = []
            self.HOME_Y_pos_list = []

            self.HOME_abs_initial_value = 0
            self.HOME_zeroed_list = []
            self.HOME_Y_pos_list_converted = []
            self.HOME_DTI_abs_list_converted = []
            self.HOME_zeroed_converted = []
            self.home_data_status = 'Cleared'

            self.FAR_DTI_abs_list = []
            self.FAR_Y_pos_list = []

            self.FAR_abs_initial_value = 0
            self.FAR_zeroed_list = []
            self.FAR_Y_pos_list_converted = []
            self.FAR_DTI_abs_list_converted = []
            self.FAR_zeroed_converted = []
            self.far_data_status = 'Cleared'


    ## SENDING DATA


    # MAIN FUNCTION CALLED BY BUTTON
    def send_data(self):

        # screen needs to be updated before sending data
        # as data sending is an intensive process and locks up kivy
        self.update_screen_before_doing_data_send()

        # start main data sending processes after 2 seconds
        Clock.schedule_once(self.do_data_send, 2)


    # FUNCTIONS DIRECTLY CALLED BY SEND_DATA()
    def update_screen_before_doing_data_send(self):

        self.send_data_button.text = 'SENDING DATA...'

        if self.home_data_status == 'Collected':
            self.home_data_status = 'Sending...'

        if self.far_data_status == 'Collected':
            self.far_data_status = 'Sending...'


    def do_data_send(self, dt):

        self.active_spreadsheet_name = self.bench_id.text + ' ' + str(date.today())
        self.format_output()
        self.open_spreadsheet() # I.E. OPEN GOOGLE SHEETS DOCUMENT
        self.write_to_worksheet()

        self.send_data_button.text = 'SEND DATA'


    # GOOGLE SHEETS DATA FORMATTING FUNCTIONS
    def format_output(self):

        # HOME SIDE
        try: 

            # normalize data against first measured value
            self.HOME_abs_initial_value = self.HOME_DTI_abs_list[0]
            self.HOME_zeroed_list = [(H - self.HOME_abs_initial_value) for H in self.HOME_DTI_abs_list]

            # convert to json format
            self.HOME_Y_pos_list_converted = self.convert_to_json(self.HOME_Y_pos_list)
            self.HOME_DTI_abs_list_converted = self.convert_to_json(self.HOME_DTI_abs_list)
            self.HOME_zeroed_converted = self.convert_to_json(self.HOME_zeroed_list)
        except: pass

        # FAR SIDE
        try: 

            # normalize data against first measured value
            self.FAR_abs_initial_value = self.FAR_DTI_abs_list[0]
            self.FAR_zeroed_list = [(F - self.FAR_abs_initial_value) for F in self.FAR_DTI_abs_list]

            # specific to far pos - coordinates need flipping because far side is flipped
            self.FAR_Y_pos_list = [(y_length + POS) for POS in self.FAR_Y_pos_list]

            # convert to json format
            self.FAR_Y_pos_list_converted = self.convert_to_json(self.FAR_Y_pos_list)
            self.FAR_DTI_abs_list_converted = self.convert_to_json(self.FAR_DTI_abs_list)        
            self.FAR_zeroed_converted = self.convert_to_json(self.FAR_zeroed_list)
        except: pass


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

        # CHECK WHETHER SPREADSHEET FOR SERIAL NUMBER ALREADY EXISTS

        page_token = None
        create_new_sheet = True

        # this is the query that gets passed to the files.list function, and looks for files in the straigtness measurements folder
        # and with a name that contains the current bench id
        q_str = "'" + self.straightness_measurements_id + "'" + " in " + "parents" + ' and ' "name" + " contains " + "'" + self.bench_id.text + "'"

        while True:
            log('Looking for existing file to send data to...')
            lookup_file = self.drive_service.files().list(q=q_str,
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=page_token).execute()

            for file in lookup_file.get('files', []): # this is written to loop through and find multiple files, but actually we only want one (and only expect one!)

                log('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                self.active_spreadsheet_object = self.gsheet_client.open_by_key(file.get('id'))
                self.rename_file_with_current_date()
                create_new_sheet = False

            if not create_new_sheet:
                break

            page_token = lookup_file.get('nextPageToken', None)
            if page_token is None:
                break

        # IF THIS IS A NEW BENCH/EXTRUSION, CREATE A NEW SPREADSHEET
        if create_new_sheet:

            log('Creating new sheet')
            self.active_spreadsheet_object = self.gsheet_client.copy(self.master_sheet_key, title = self.active_spreadsheet_name, copy_permissions = True)
            self.active_spreadsheet_object.share('yetitool.com', perm_type='domain', role='writer')
            self.move_sheet_to_operator_resources()

    def rename_file_with_current_date(self):

        file_metadata = {
            'name': "'" + self.active_spreadsheet_name + "'"
            }        

        file = self.drive_service.files().update(fileId=self.active_spreadsheet_id,
                                                body = file_metadata)


    def move_sheet_to_operator_resources(self):

        log('Moving sheet to production > operator resources > live measurements')

        # Take the file ID and move it into the operator resources folder
        self.active_spreadsheet_id = self.active_spreadsheet_object.id

        # Retrieve the existing parents to remove
        file = self.drive_service.files().get(fileId=self.active_spreadsheet_id,
                                         fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = self.drive_service.files().update(fileId=self.active_spreadsheet_id,
                                            addParents=self.straightness_measurements_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()


    # FUNCTION TO WRITE DATA TO WORKSHEET
    def write_to_worksheet(self):

        # INDICATE IF BENCH OR EXTRUSION
        test_data_worksheet_name = str(date.today()) + " " + self.test_type + ": " + self.test_id.text

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

        if self.HOME_zeroed_converted != []:
            self.home_data_status = 'Sending...'
            worksheet.update('C3:C', self.HOME_Y_pos_list_converted)
            worksheet.update('D3:D', self.HOME_zeroed_converted)
            self.home_data_status = 'Sent'
            log('Home side data sent')

        if self.FAR_zeroed_converted != []:
            self.far_data_status = 'Sending...'
            worksheet.update('E3:E', self.FAR_Y_pos_list_converted)
            worksheet.update('F3:F', self.FAR_zeroed_converted)
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

        if (self.HOME_zeroed_converted != []) and (self.FAR_zeroed_converted != []):
            self.last_bench = self.bench_id.text
            self.last_test = self.test_id.text
            self.test_id.text = str(int(self.last_test) + 1)
            self.clear_data(clearall = True)

        self.go_stop.state = 'normal'
        self.go_stop.text = 'GO'
        self.go_stop.background_color = [0,0.502,0,1]


    def delete_existing_spreadsheet_data(self, worksheet_name):

        C_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "C3:C"
        D_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "D3:D"
        E_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "E3:E"
        F_str_to_clear = "'" + str(worksheet_name) + "'" + "!" + "F3:F"

        self.active_spreadsheet_object.values_clear(C_str_to_clear)
        self.active_spreadsheet_object.values_clear(D_str_to_clear)
        self.active_spreadsheet_object.values_clear(E_str_to_clear)
        self.active_spreadsheet_object.values_clear(F_str_to_clear)


    ## ENSURE SCREEN IS UPDATED TO REFLECT STATUS
    # update with general status information - DTI read & data sending info
    def update_screen(self, dt):

        self.home_data_status_label.text = self.home_data_status
        self.far_data_status_label.text = self.far_data_status
        self.dti_read_label.text = str(DTI.read_mm())


    # update home button when homing has finished
    def check_home_completion(self, dt):

        if not self.m.s.is_sequential_streaming:
            Clock.unschedule(self.check_for_home_end_event)
            self.home_stop.text = 'HOME'
            self.home_stop.background_color = [0,0.502,0,1]
            self.home_stop.state = 'normal'
            print('not homing')

        else: 
            print('homing')


    def on_leave(self):

        if self.poll_for_screen != None:
            Clock.unschedule(self.poll_for_screen)























