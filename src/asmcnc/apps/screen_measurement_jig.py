'''
Screen to 
'''

# Build step: pip install gspread oauth2client
import os
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
                cols: 5


                Label: 

                    text: "Bench ID"
                    color: 0,0,0,1
                Label: 
                    id: test_id
                    text: "Test ID"
                    color: 0,0,0,1
                Label: 
                    id: travel
                    text: "Travel"
                    color: 0,0,0,1
                Label: 
                    id: wheel_home
                    text: "Wheel diameter HOME"
                    color: 0,0,0,1
                Label: 
                    id: wheel_far
                    text: "Wheel diameter FAR"
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

    direction = 'forward'
    test_data = [['mY', 'L', 'R']]
    starting_pos = 0
    max_pos = 0
    last_bench = ''
    last_test = ''

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

            ## CHANGE BUTTON
            self.go_stop.background_color = [1,0,0,1]
            self.go_stop.text = 'STOP'

            ## SET VARIABLES
            self.starting_pos = self.m.mpos_y()
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
                self.test_data.append([str(round(self.m.mpos_y(), 2)), self.e0.L_side + self.e1.L_side, self.e0.R_side + self.e1.R_side])
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
                self.test_data.append([str(round(self.m.mpos_y(), 2)),  self.e0.L_side + self.e1.L_side, self.e0.R_side + self.e1.R_side])
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

    def send_data_to_gsheet(self, rows):

        # rows = self.format_output(rows)

        ## GSHEET SETUP
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
            ]
        file_name = os.path.dirname(os.path.realpath(__file__)) + '/gsheet_client_key.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
        client = gspread.authorize(creds)
        
        #Set the sheet to dump to
        name_of_GSheet = 'Y axis linear calibration'
        spread= client.open(name_of_GSheet)
        UL_data_worksheet_name = "Data dump"

        print ("Wiping old count sheet in GSheet \"" + name_of_GSheet + "\"...")
        sheet = spread.worksheet(UL_data_worksheet_name)
        spread.values_clear(UL_data_worksheet_name)

        print ("Writing stock values to GSheet...")
        sheet.update('A1:G', rows)

        print ("Updating job stats...")
        sheet = spread.worksheet("Test info")
        current_utc =   datetime.utcnow()
        # Time
        sheet.update('B1', str(current_utc))
        # Bench ID:
        sheet.update('B2', str(self.bench_id.text))
        # Test ID: 
        sheet.update('B3', str(self.test_id.text))
        # Travel: 
        sheet.update('B4', str(self.travel.text))
        # Wheel diameter HOME:
        sheet.update('B5', str(self.wheel_home.text))
        # Wheel diameter FAR:
        sheet.update('B6', str(self.wheel_far.text))        
        # Direction: 
        sheet.update('B7', str(self.direction)) 
        print ("ALL DONE!!! You're welcome.")

        self.go_stop.state = 'normal'
        self.go_stop.text = 'GO'
        self.go_stop.background_color = [0,0.502,0,1]


    def create_new_spreadsheet(self):

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

        else:
            spread = client.open(name_of_GSheet)

        test_data_worksheet_name = 'Test' + self.test_id.text

        ## don't know if this will work, might need to do 'if none'
        try: 
            worksheet = spread.worksheet(test_data_worksheet_name)

        except:
            test_data_worksheet_name = 'Test' + self.test_id.text
            worksheet = spread.duplicate_sheet(0, insert_sheet_index=None, new_sheet_id=None, new_sheet_name=test_data_worksheet_name)

        print ("Wiping old count sheet in GSheet \"" + name_of_GSheet + "\"...")
        spread.values_clear(test_data_worksheet_name)

        print ("Writing stock values to GSheet...")
        worksheet.update('A1:F', self.test_data)

        print ("Updating job stats...")
        current_utc =   datetime.utcnow()
        # Time
        worksheet.update('H1', str(current_utc))
        # Bench ID:
        worksheet.update('H2', str(self.bench_id.text))
        # Test ID: 
        worksheet.update('H3', str(self.test_id.text))
        # Travel: 
        worksheet.update('H4', str(self.travel.text))
        # Wheel diameter HOME:
        worksheet.update('H5', str(self.wheel_home.text))
        # Wheel diameter FAR:
        worksheet.update('H6', str(self.wheel_far.text))        
        # Direction: 
        worksheet.update('H7', str(self.direction)) 
        print ("ALL DONE!!! You're welcome.")

        self.last_bench = self.bench_id.text
        self.last_test = self.test_id.text
        self.test_id.text = str(int(self.last_test) + 1)

        self.go_stop.state = 'normal'
        self.go_stop.text = 'GO'
        self.go_stop.background_color = [0,0.502,0,1]


    def clear_data(self):
        self.test_data = [['mY', 'L', 'R']]

    def go_to_lobby(self):
        self.sm.current = 'lobby'






