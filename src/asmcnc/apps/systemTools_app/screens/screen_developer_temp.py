'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.clock import Clock

from asmcnc.production import process_micrometer_read, process_linear_encoder_read, screen_z_head_diagnostics, screen_measurement_jig

Builder.load_string("""

<ScrollableLabelLogsView>:
    scroll_y:1

    canvas.before:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: self.size
            pos: self.pos
    
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        font_size: '10sp'
        text: root.text
        max_lines: 60


<ScrollableLabelCommandView>:
    scroll_y:1

    canvas.before:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: self.size
            pos: self.pos
    
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        font_size: '12sp'
        text: root.text
        max_lines: 20

<DeveloperTempScreen>

    output_view: output_view
    input_view: input_view
    gCodeInput: gCodeInput

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 10
            spacing: 10
            orientation: "vertical"
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(70)
                    width: dp(780)
                    text: "Developer"
                    color: [0,0,0,1]
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
       
            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(240)
                padding: 0
                spacing: 10
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(577.5)
                    height: dp(240)
                    padding: 20
                    spacing: 20
                    orientation: 'vertical'
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                    GridLayout: 
                        size: self.size
                        pos: self.parent.pos
                        cols: 4
                        rows: 4

                        Button:
                            text: 'Micrometer'
                            on_press: root.open_micrometer_jig_screen()
                                    
                        Button:
                            text: 'Calibration'
                            on_press: root.open_squareness_jig_screen()
                                       
                        Button:
                            text: 'Z head diagnostics'
                            on_press: root.open_z_head_diagnostics()
                            
                        Button:
                            text: 'Rotary Jig'
                            on_press: root.open_rotary_jig()

                        Button:
                            text: ''

                        Button:
                            text: ''

                        Button:
                            text: ''
                                       
                        Button:
                            text: ''
                            
                        Button:
                            text: ''

                        Button:
                            text: ''

                        Button:
                            text: ''

                        Button:
                            text: ''
                                       
                        Button:
                            text: ''
                            
                        Button:
                            text: ''

                        Button:
                            text: ''
                            
                        Button:
                            text: ''

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
                    height: dp(240)
                    padding: 20
                    spacing: 0
                    orientation: 'vertical'
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                    TextInput:                      
                        id:gCodeInput
                        multiline: False
                        text: ''
                        on_text_validate: root.send_gcode_textinput()
                        size_hint_y: 0.25

                    ScrollableLabelCommandView:
                        id: input_view



            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(130)
                padding: 0
                spacing: 10
                orientation: 'horizontal'
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
                    height: dp(130)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(130)
                        width: dp(192.5)
                        padding: [52.25,31,52.25,31]
                        Button:
                            size_hint: (None,None)
                            height: dp(68)
                            width: dp(88)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(385)
                    height: dp(130)
                    padding: 10
                    spacing: 0
                    orientation: 'vertical'

                    ScrollableLabelLogsView:
                        id: output_view

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
                    height: dp(130)
                    padding: 0
                    spacing: 0    


                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(130)
                        width: dp(192.5)
                        padding: [40.25,9,40.25,9] 
                        Button:
                            size_hint: (None,None)
                            height: dp(112)
                            width: dp(112)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.exit_app()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_lobby.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
""")

class ScrollableLabelLogsView(ScrollView):
    text = StringProperty('')

class ScrollableLabelCommandView(ScrollView):
    text = StringProperty('')

class DeveloperTempScreen(Screen):

    def __init__(self, **kwargs):
        super(DeveloperTempScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def send_gcode_textinput(self): 
        self.m.send_any_gcode_command(str(self.gCodeInput.text))

    def open_micrometer_jig_screen(self):
        if not self.systemtools_sm.sm.has_screen('micrometer_screen'):
            screen_process_micrometer_read = process_micrometer_read.ProcessMicrometerScreen(name = 'micrometer_screen', screen_manager = self.systemtools_sm.sm, machine = self.m)
            self.systemtools_sm.sm.add_widget(screen_process_micrometer_read)

        self.systemtools_sm.sm.current = 'micrometer_screen'

    def open_squareness_jig_screen(self):
        if not self.systemtools_sm.sm.has_screen('squareness_jig_screen'):
            screen_process_linear_encoder_read = process_linear_encoder_read.ProcessLinearEncoderScreen(name = 'squareness_jig_screen', screen_manager = self.systemtools_sm.sm, machine = self.m)
            self.systemtools_sm.sm.add_widget(screen_process_linear_encoder_read)

        self.systemtools_sm.sm.current = 'squareness_jig_screen'

    def open_z_head_diagnostics(self):
        if not self.systemtools_sm.sm.has_screen('z_head_diagnostics'):
            z_head_diagnostics_screen = screen_z_head_diagnostics.ZHeadDiagnosticsScreen(name = 'z_head_diagnostics', screen_manager = self.systemtools_sm.sm, machine = self.m)
            self.systemtools_sm.sm.add_widget(z_head_diagnostics_screen)

        self.systemtools_sm.sm.current = 'z_head_diagnostics'

    def open_rotary_jig(self):
        if not self.systemtools_sm.sm.has_screen('rotary_jig'):
            y_measurement_jig_screen = screen_measurement_jig.JigScreen(name = 'rotary_jig', screen_manager = self.systemtools_sm.sm, machine = self.m)
            self.systemtools_sm.sm.add_widget(y_measurement_jig_screen)

        self.systemtools_sm.sm.current = 'rotary_jig'
