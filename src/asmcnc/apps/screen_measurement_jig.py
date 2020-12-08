'''
Screen to 
'''

# Build step: pip install gspread oauth2client
import os
import math
import operator
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from datetime import datetime


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
from asmcnc.comms import encoder_connection_ACM0
from asmcnc.comms import encoder_connection_ACM1

Builder.load_string("""


<JigScreen>:

    status_container:status_container
    gcode_monitor_container:gcode_monitor_container
    move_container: move_container
    bench_id:bench_id 
    test_id:test_id
    travel:travel
    wheel_home:wheel_home
    wheel_far:wheel_far
    go_stop: go_stop
    dir_toggle:dir_toggle
    pulse_home:pulse_home
    pulse_far:pulse_far

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


                Label: 
                    text: "Bench ID"
                    color: 0,0,0,1
                Label: 
                    text: "Test ID"
                    color: 0,0,0,1
                Label: 
                    text: "Travel"
                    color: 0,0,0,1
                Label: 
                    text: "Wheel HOME"
                    color: 0,0,0,1
                Label: 
                    text: "Wheel FAR"
                    color: 0,0,0,1
                Label: 
                    text: "Pulse/rev HOME"
                    color: 0,0,0,1
                Label: 
                    text: "Pulse/rev FAR"
                    color: 0,0,0,1


                TextInput: 
                    id: bench_id 
                    text: "default"
                TextInput: 
                    id: test_id
                    text: "1"
                    input_filter: 'int'
                TextInput: 
                    id: travel
                    text: "2500"
                    input_filter: 'float'
                TextInput: 
                    id: wheel_home
                    text: "42.000"
                    input_filter: 'float'
                TextInput: 
                    id: wheel_far
                    text: "42.000"
                    input_filter: 'float'
                TextInput:
                    id: pulse_home
                    text: "1024"
                    input_filter: 'int'
                TextInput:
                    id: pulse_far
                    text: "2000"
                    input_filter: 'int'

            GridLayout: 

                pos: self.parent.pos
                size_hint_y: 0.15
                rows: 1
                cols: 4
                spacing: 5

                ToggleButton:
                    id: dir_toggle
                    text: "Going Forwards"
                    on_press: root.toggle_direction()
                ToggleButton:
                    id: go_stop
                    text: "GO"
                    on_press: root.run_stop_test()
                    background_color: [0,0,0,1]
                    background_normal: ''
                Button:
                    text: "RESET"
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

class JigScreen(Screen):

    Y_pos_list = []
    L_abs_list = []
    R_abs_list = []

    L_diff_list = []
    R_diff_list = []
    Y_travel_list = []

    L_pulse_raw = []
    R_pulse_raw = []

    direction = 'forward'
    starting_pos = 0
    max_pos = 0
    last_bench = ''
    last_test = ''

    L_abs_initial_value = 0
    R_abs_initial_value = 0

    master_sheet_key = '1WE10SOkcf1MLIn5g6cQYoiqJIPZj70tyPoenw3KAqnM'

    def __init__(self, **kwargs):

        super(JigScreen, self).__init__(**kwargs)

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        # Establish 's'erial comms and initialise
        self.e0 = encoder_connection_ACM0.EncoderConnection(self, self.sm)
        self.e1 = encoder_connection_ACM1.EncoderConnection(self, self.sm)
        self.e0.establish_connection()
        self.e1.establish_connection()

        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))
        self.gcode_monitor_container.add_widget(widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.sm))
        self.move_container.add_widget(widget_xy_move.XYMove(machine=self.m, screen_manager=self.sm))

    def on_enter(self):

        if (self.e0.is_connected() and self.e1.is_connected()):
            self.go_stop.background_color = [0,0.502,0,1]

    def toggle_direction(self):
        if self.dir_toggle.state == 'down':
            self.dir_toggle.text = 'Going Backwards'
            self.direction = 'backward'
        elif self.dir_toggle.state == 'normal':
            self.dir_toggle.text = 'Going Forwards'
            self.direction = 'forward'

    def run_stop_test(self):

        if self.go_stop.state == 'down':

            self.clear_data()

            ## CHANGE BUTTON
            self.go_stop.background_color = [1,0,0,1]
            self.go_stop.text = 'STOP'

            ## SET VARIABLES
            self.starting_pos = float(self.m.mpos_y())
            self.starting_L = self.e0.L_side + self.e1.L_side
            self.starting_R = self.e0.R_side + self.e1.R_side
            self.max_pos = self.set_max_pos()

            ## START THE TEST
            self.test_run = Clock.schedule_interval(self.do_test_step, 0.5)

        elif self.go_stop.state == 'normal':
            self.end_of_test_sequence()

    def end_of_test_sequence(self):
            Clock.unschedule(self.test_run)
            self.go_stop.text = 'UPLOADING...'

            ## GET DATA UPDATED
            Clock.schedule_once(lambda dt: self.create_new_spreadsheet(), 1)

    def set_max_pos(self):

        if self.direction == 'forward':
            return self.starting_pos + float(self.travel.text)

        elif self.direction == 'backward':
            return self.starting_pos - float(self.travel.text)

    def do_test_step(self, dt):

        if self.direction == 'forward':
            if self.m.state() == 'Jog':
                pass

            elif self.m.state() == 'Idle' and self.m.mpos_y() <= self.max_pos:

                self.Y_pos_list.append(float(self.m.mpos_y()))
                self.L_abs_list.append(float(self.e0.L_side + self.e1.L_side))
                self.R_abs_list.append(float(self.e0.R_side + self.e1.R_side))

                self.m.jog_relative('Y', 10, 6000)

            elif self.m.state() == 'Idle' and self.m.mpos_y() > self.max_pos:
                self.end_of_test_sequence()
            else: 
                Clock.unschedule(self.test_run)
                self.go_stop.state = 'normal'
                self.go_stop.text = 'GO'
                self.go_stop.background_color = [0,0.502,0,1]

        else:
            if self.m.state() == 'Jog':
                pass

            elif self.m.state() == 'Idle' and self.m.mpos_y() >= self.max_pos:

                self.Y_pos_list.append(float(self.m.mpos_y()))
                self.L_abs_list.append(float(self.e0.L_side + self.e1.L_side))
                self.R_abs_list.append(float(self.e0.R_side + self.e1.R_side))

                self.m.jog_relative('Y', -10, 6000)
            elif self.m.state() == 'Idle' and self.m.mpos_y() < self.max_pos:
                self.end_of_test_sequence()
            else: 
                Clock.unschedule(self.test_run)
                self.go_stop.state = 'normal'
                self.go_stop.text = 'GO'
                self.go_stop.background_color = [0,0.502,0,1]

    # def format_output(self, rows):
    #     rows[1:] = [str(int(L) - int(self.starting_L)) for L in rows[1:]]
    #     rows[2:] = [str(int(R) - int(self.starting_R)) for R in rows[2:]]
    #     return rows

    def format_output(self):

        self.L_pulse_raw = self.convert_to_json(self.L_abs_list)
        self.R_pulse_raw = self.convert_to_json(self.R_abs_list)

        if self.direction == 'forward':

            self.L_abs_list = [float(self.starting_pos + float(((int(L) - int(self.starting_L))*(math.pi*float(self.wheel_home.text)/float(self.pulse_home.text))))) for L in self.L_abs_list]
            self.R_abs_list = [float(self.starting_pos + float(((int(R) - int(self.starting_R))*(math.pi*float(self.wheel_far.text)/float(self.pulse_far.text))))) for R in self.R_abs_list]

        else:
            self.L_abs_list = [float(self.starting_pos - float(((int(L) - int(self.starting_L))*(math.pi*float(self.wheel_home.text)/float(self.pulse_home.text))))) for L in self.L_abs_list]
            self.R_abs_list = [float(self.starting_pos - float(((int(R) - int(self.starting_R))*(math.pi*float(self.wheel_far.text)/float(self.pulse_far.text))))) for R in self.R_abs_list]

        self.L_abs_initial_value = self.L_abs_list[0]
        self.R_abs_initial_value = self.R_abs_list[0]

        self.Y_travel_list = [(y - self.starting_pos) for y in self.Y_pos_list]
        self.L_abs_list = [(L - self.L_abs_initial_value) for L in self.L_abs_list]
        self.R_abs_list = [(R - self.R_abs_initial_value) for R in self.R_abs_list]
        self.L_diff_list = list(map(operator.sub, self.L_abs_list, self.Y_travel_list))
        self.R_diff_list = list(map(operator.sub, self.R_abs_list, self.Y_travel_list))
        # self.L_diff_list = self.L_abs_list - self.Y_pos_list
        # self.R_diff_list = self.R_abs_list - self.Y_pos_list

        self.Y_pos_list = self.convert_to_json(self.Y_pos_list)
        self.L_abs_list = self.convert_to_json(self.L_abs_list)
        self.R_abs_list = self.convert_to_json(self.R_abs_list)
        self.L_diff_list = self.convert_to_json(self.L_diff_list)
        self.R_diff_list = self.convert_to_json(self.R_diff_list)
        self.Y_travel_list = self.convert_to_json(self.Y_travel_list)

    def convert_to_json(self, data):
        new_data = []

        data = [str(x).split() for x in data]

        for list in data:
            new_list_item = [float(e) for e in list]
            new_data.append(new_list_item)

        return new_data

    def create_new_spreadsheet(self):

        self.format_output()

        name_of_GSheet = 'Y axis linear calibration ' + self.bench_id.text

        ## GSHEET SETUP
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
            ]
        file_name = os.path.dirname(os.path.realpath(__file__)) + '/gsheet_client_key.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
        client = gspread.authorize(creds)

        if self.bench_id.text != self.last_bench:
            #Create the sheet to dump to
            spread = client.copy(self.master_sheet_key, title=name_of_GSheet, copy_permissions=True)
            spread.share('yetitool.com', perm_type='domain', role='writer')
            spread.share('lettie.adkins@yetitool.com', perm_type='user', role='writer', notify=True, email_message=self.bench_id.text, with_link=False)
            spread.share('ed.sells@yetitool.com', perm_type='user', role='writer', notify=True, email_message=self.bench_id.text, with_link=False)

        else:
            spread = client.open(name_of_GSheet)

        test_data_worksheet_name = 'Test ' + self.test_id.text

        ## don't know if this will work, might need to do 'if none'
        try: 
            worksheet = spread.worksheet(test_data_worksheet_name)

        except:
            test_data_worksheet_name = 'Test ' + self.test_id.text
            worksheet = spread.duplicate_sheet(0, insert_sheet_index=None, new_sheet_id=None, new_sheet_name=test_data_worksheet_name)

        print ("Wiping old count sheet in GSheet \"" + name_of_GSheet + "\"...")
        # spread.values_clear(test_data_worksheet_name)

        print ("Writing stock values to GSheet...")
        worksheet.update('A2:A', self.Y_pos_list)
        worksheet.update('B2:B', self.Y_travel_list)
        worksheet.update('C2:C', self.L_abs_list)
        worksheet.update('D2:D', self.R_abs_list)
        worksheet.update('E2:E', self.L_diff_list)
        worksheet.update('F2:F', self.R_diff_list)

        worksheet.update('M2:M', self.L_pulse_raw)
        worksheet.update('N2:N', self.R_pulse_raw)

        print ("Updating job stats...")
        current_utc =   datetime.utcnow()
        # Time
        worksheet.update('I1', str(current_utc))
        # Bench ID:
        worksheet.update('I2', str(self.bench_id.text))
        # Test ID: 
        worksheet.update('I3', str(self.test_id.text))
        # Travel: 
        worksheet.update('I4', str(self.travel.text))
        # Wheel diameter HOME:
        worksheet.update('I5', str(self.wheel_home.text))
        # Wheel diameter FAR:
        worksheet.update('I6', str(self.wheel_far.text))        
        # Direction: 
        worksheet.update('H7', str(self.direction)) 
        print ("ALL DONE!!! You're welcome.")

        self.last_bench = self.bench_id.text
        self.last_test = self.test_id.text
        self.test_id.text = str(int(self.last_test) + 1)

        self.go_stop.state = 'normal'
        self.go_stop.text = 'GO'
        self.go_stop.background_color = [0,0.502,0,1]

        self.clear_data()

    def clear_data(self):
        self.Y_pos_list = []
        self.L_abs_list = []
        self.R_abs_list = []

        self.L_diff_list = []
        self.R_diff_list = []
        self.Y_travel_list = []

    def go_to_lobby(self):
        self.sm.current = 'lobby'






