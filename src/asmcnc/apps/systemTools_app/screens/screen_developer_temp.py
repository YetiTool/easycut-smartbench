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
        font_size: str(get_scaled_width(10)) + 'sp'
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
        font_size: str(get_scaled_width(12)) + 'sp'
        text: root.text
        max_lines: 20

<DeveloperTempScreen>

    output_view: output_view
    input_view: input_view
    gCodeInput: gCodeInput

    BoxLayout:
        height: dp(app.get_scaled_height(800))
        width: dp(app.get_scaled_width(480))
        canvas.before:
            Color: 
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding:(dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
            spacing:0.0208333333333*app.height
            orientation: "vertical"
            BoxLayout:
                padding:dp(0)
                spacing: 0
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(70))
                    width: dp(app.get_scaled_width(780))
                    text: "Developer"
                    color: [0,0,0,1]
                    font_size:dp(0.0375*app.width)
                    halign: "center"
                    valign: "bottom"
                    markup: True
       
            BoxLayout:
                size_hint: (None,None)
                width: dp(app.get_scaled_width(780))
                height: dp(app.get_scaled_height(240))
                padding:dp(0)
                spacing:0.0125*app.width
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(577.5))
                    height: dp(app.get_scaled_height(240))
                    padding:(dp(app.get_scaled_width(20)),dp(app.get_scaled_height(20)))
                    spacing:0.0416666666667*app.height
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
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: "Update test"
                            on_press: root.open_update_testing()
                                    
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''
                                       
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''
                                       
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''
                                       
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            text: ''

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(192.5))
                    height: dp(app.get_scaled_height(240))
                    padding:(dp(app.get_scaled_width(20)),dp(app.get_scaled_height(20)))
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
                width: dp(app.get_scaled_width(780))
                height: dp(app.get_scaled_height(130))
                padding:dp(0)
                spacing:0.0125*app.width
                orientation: 'horizontal'
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(192.5))
                    height: dp(app.get_scaled_height(130))
                    padding:dp(0)
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(app.get_scaled_height(130))
                        width: dp(app.get_scaled_width(192.5))
                        padding:(dp(app.get_scaled_width(52.25)),dp(app.get_scaled_height(31)),dp(app.get_scaled_width(52.25)),dp(app.get_scaled_height(31)))
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(68))
                            width: dp(app.get_scaled_width(88))
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.go_back()
                            BoxLayout:
                                padding:dp(0)
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
                    width: dp(app.get_scaled_width(385))
                    height: dp(app.get_scaled_height(130))
                    padding:(dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
                    spacing: 0
                    orientation: 'vertical'

                    ScrollableLabelLogsView:
                        id: output_view

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(192.5))
                    height: dp(app.get_scaled_height(130))
                    padding:dp(0)
                    spacing: 0    


                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(app.get_scaled_height(130))
                        width: dp(app.get_scaled_width(192.5))
                        padding:(dp(app.get_scaled_width(40.25)),dp(app.get_scaled_height(9)),dp(app.get_scaled_width(40.25)),dp(app.get_scaled_height(9)))
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(112))
                            width: dp(app.get_scaled_width(112))
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.exit_app()
                            BoxLayout:
                                padding:dp(0)
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
