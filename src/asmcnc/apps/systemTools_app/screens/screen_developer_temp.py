"""
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.clock import Clock

Builder.load_string(
"""

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
        font_size: app.get_scaled_sp('10.0sp')
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
        font_size: app.get_scaled_sp('12.0sp')
        text: root.text
        max_lines: 20

<DeveloperTempScreen>

    output_view: output_view
    input_view: input_view
    gCodeInput: gCodeInput

    BoxLayout:
        height: app.get_scaled_height(800.000000002)
        width: app.get_scaled_width(480.0)
        canvas.before:
            Color: 
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: app.get_scaled_tuple([10.0, 10.0])
            spacing: app.get_scaled_width(9.99999999998)
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
                    height: app.get_scaled_height(69.9999999998)
                    width: app.get_scaled_width(780.0)
                    text: "Developer"
                    color: [0,0,0,1]
                    font_size: app.get_scaled_width(30.0)
                    halign: "center"
                    valign: "bottom"
                    markup: True
       
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(780.0)
                height: app.get_scaled_height(240.0)
                padding: 0
                spacing: app.get_scaled_width(10.0)
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(577.5)
                    height: app.get_scaled_height(240.0)
                    padding: app.get_scaled_tuple([20.0, 20.0])
                    spacing: app.get_scaled_width(20.0)
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
                            font_size: app.get_scaled_sp('15.0sp')
                            text: "Update test"
                            on_press: root.open_update_testing()
                                    
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''
                                       
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''
                            
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''
                                       
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''
                            
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''
                                       
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''
                            
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''
                            
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            text: ''

                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(192.5)
                    height: app.get_scaled_height(240.0)
                    padding: app.get_scaled_tuple([20.0, 20.0])
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
                width: app.get_scaled_width(780.0)
                height: app.get_scaled_height(130.0)
                padding: 0
                spacing: app.get_scaled_width(10.0)
                orientation: 'horizontal'
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size

                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(192.5)
                    height: app.get_scaled_height(130.0)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: app.get_scaled_height(130.0)
                        width: app.get_scaled_width(192.5)
                        padding: app.get_scaled_tuple([52.25, 31.0, 52.25, 31.0])
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(68.0000000002)
                            width: app.get_scaled_width(88.0)
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
                    width: app.get_scaled_width(385.0)
                    height: app.get_scaled_height(130.0)
                    padding: app.get_scaled_tuple([10.0, 10.0])
                    spacing: 0
                    orientation: 'vertical'

                    ScrollableLabelLogsView:
                        id: output_view

                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(192.5)
                    height: app.get_scaled_height(130.0)
                    padding: 0
                    spacing: 0


                    BoxLayout: 
                        size_hint: (None, None)
                        height: app.get_scaled_height(130.0)
                        width: app.get_scaled_width(192.5)
                        padding: app.get_scaled_tuple([40.25, 9.0, 40.25, 9.0])
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(112.0)
                            width: app.get_scaled_width(112.0)
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
"""
)


class ScrollableLabelLogsView(ScrollView):
    text = StringProperty("")


class ScrollableLabelCommandView(ScrollView):
    text = StringProperty("")


class DeveloperTempScreen(Screen):
    def __init__(self, **kwargs):
        super(DeveloperTempScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs["system_tools"]
        self.m = kwargs["machine"]

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def send_gcode_textinput(self):
        self.m.send_any_gcode_command(str(self.gCodeInput.text))

    def open_update_testing(self):
        self.systemtools_sm.open_update_testing_screen()
