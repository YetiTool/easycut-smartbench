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
        font_size: str(0.0125*app.width) + 'sp'
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
        font_size: str(0.015*app.width) + 'sp'
        text: root.text
        max_lines: 20

<DeveloperTempScreen>

    output_view: output_view
    input_view: input_view
    gCodeInput: gCodeInput

    BoxLayout:
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
        canvas.before:
            Color: 
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
            spacing:0.0208333333333*app.height
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
                    height: dp(0.145833333333*app.height)
                    width: dp(0.975*app.width)
                    text: "Developer"
                    color: [0,0,0,1]
                    font_size: 0.0375*app.width
                    halign: "center"
                    valign: "bottom"
                    markup: True
       
            BoxLayout:
                size_hint: (None,None)
                width: dp(0.975*app.width)
                height: dp(0.5*app.height)
                padding: 0
                spacing:0.0125*app.width
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.721875*app.width)
                    height: dp(0.5*app.height)
                    padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
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
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: "Update test"
                            on_press: root.open_update_testing()
                                    
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''
                                       
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''
                                       
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''
                                       
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''
                            
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: ''

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.240625*app.width)
                    height: dp(0.5*app.height)
                    padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
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
                width: dp(0.975*app.width)
                height: dp(0.270833333333*app.height)
                padding: 0
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
                    width: dp(0.240625*app.width)
                    height: dp(0.270833333333*app.height)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(0.270833333333*app.height)
                        width: dp(0.240625*app.width)
                        padding:[dp(0.0653125)*app.width, dp(0.0645833333333)*app.height, dp(0.0653125)*app.width, dp(0.0645833333333)*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.141666666667*app.height)
                            width: dp(0.11*app.width)
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
                    width: dp(0.48125*app.width)
                    height: dp(0.270833333333*app.height)
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    spacing: 0
                    orientation: 'vertical'

                    ScrollableLabelLogsView:
                        id: output_view

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.240625*app.width)
                    height: dp(0.270833333333*app.height)
                    padding: 0
                    spacing: 0    


                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(0.270833333333*app.height)
                        width: dp(0.240625*app.width)
                        padding:[dp(0.0503125)*app.width, dp(0.01875)*app.height, dp(0.0503125)*app.width, dp(0.01875)*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.233333333333*app.height)
                            width: dp(0.14*app.width)
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
        self.systemtools_sm = kwargs.pop("system_tools")
        self.m = kwargs.pop("machine")
        super(DeveloperTempScreen, self).__init__(**kwargs)

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def send_gcode_textinput(self):
        self.m.send_any_gcode_command(str(self.gCodeInput.text))

    def open_update_testing(self):
        self.systemtools_sm.open_update_testing_screen()
