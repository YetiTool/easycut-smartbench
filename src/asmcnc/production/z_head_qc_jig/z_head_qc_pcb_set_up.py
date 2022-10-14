from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from datetime import datetime
from kivy.uix.spinner import Spinner

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadPCBSetUp>:

    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.2

                Button:
                    text: '<<< Home'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label: 
                    text: "info"
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: 'Disconnect'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

            BoxLayout: 
                orientation: 'horizontal'
                size_hint_y: 0.6

                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(10),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "FW version"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(10),0]

                        Label: 
                            text: "Recommended: "
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "firmware" 
                            Label:
                                text: "2.5.5"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]

                        Label: 
                            text: "Alternative & available: "
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'

                            BoxLayout: 
                                orientation: 'horizontal'
                                CheckBox:
                                    size_hint_x: 0.2
                                    group: "firmware" 
                                Label:
                                    text: "2.5.4"
                                    text_size: self.size
                                    markup: 'True'
                                    halign: 'left'
                                    valign: 'middle'
                                    padding: [dp(10),0]

                            BoxLayout: 
                                orientation: 'horizontal'
                                CheckBox:
                                    size_hint_x: 0.2
                                    group: "firmware" 
                                Label:
                                    text: "1.4.0"
                                    text_size: self.size
                                    markup: 'True'
                                    halign: 'left'
                                    valign: 'middle'
                                    padding: [dp(10),0]



                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(10),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "Z current (v1.3)"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(10),0]

                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "z_current" 
                            Label:
                                text: "25"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]

                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "z_current" 
                            Label:
                                text: "Other"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]

                            Spinner:
                                text: "25"


                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(10),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "X current (v1.3)"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(10),0]

                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "x_current" 
                            Label:
                                text: "26 (single stack)"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]

                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "x_current" 
                            Label:
                                text: "20 (double stack)"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]

                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "x_current" 
                            Label:
                                text: "Other"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]

                            Spinner:
                                text: "25"

                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(10),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "Thermal coefficients (v1.3)"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(10),0]

                        Label: 
                            text: "Recommended: "
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "x_current" 
                            Label:
                                text: "10000, 5000, 5000"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]


                        BoxLayout: 
                            orientation: 'horizontal'
                            CheckBox:
                                size_hint_x: 0.2
                                group: "x_current" 
                            Label:
                                text: "Other"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'
                                padding: [dp(10),0]

                        GridLayout: 
                            cols: 3
                            rows: 2
                            Label:
                                text: "X"
                            Label:
                                text: "Y"
                            Label:
                                text: "Z"
                            TextInput:
                                text: "25"
                            TextInput:
                                text: "25"
                            TextInput:
                                text: "25"



            Button:
                on_press: 
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2


        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
    

""")

def log(message):
    timestamp = datetime.now()
    print ('Z Head Connecting Screen: ' + timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadPCBSetUp(Screen):

    def __init__(self, **kwargs):

        super(ZHeadPCBSetUp, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)