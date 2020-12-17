'''
Created on nov 2020
@author: Ollie
Text input # on_enter: root.sucessful_activation
'''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from asmcnc.skavaUI import widget_status_bar
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import os

Builder.load_string("""

<WarrantyScreen4>:

    status_container:status_container
    activation_code:activation_code
    error_message_top:error_message_top
    error_message_bottom:error_message_bottom

    BoxLayout: 
        size_hint: (None,None)
        width: dp(800)
        height: dp(480)
        orientation: 'vertical'

        canvas:
            Color:
                rgba: hex('##e5e5e5')
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            id: status_container 
            size_hint_y: 0.08

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'
                
            Label:
                font_size: '30sp'
                text: "[color=333333ff]Enter your activation code:[/color]"
                text_size: self.size
                valign: 'bottom'
                halign: 'center'
                markup: 'true'
                bold: True

            BoxLayout:
                orientation: 'vertical'
                width: dp(800)
                height: dp(75)
                padding: [dp(200), 0]
                size_hint: (None,None)
                TextInput: 
                    id: activation_code
                    valign: 'middle'
                    halign: 'center'
                    height: dp(50)
                    width: dp(400) 
                    size_hint: (None,None)
                    text_size: self.size
                    font_size: '30sp'
                    markup: True
                    multiline: False
                    text: ''
                    input_filter: 'int'
            BoxLayout:
                orientation: 'vertical'
                width: dp(800)
                height: dp(125)
                padding: [dp(20)]
                size_hint: (None,None)
                Label:
                    id: error_message_top
                    font_size: '20sp'
                    text: "Please check your activation code."
                    text_size: self.size
                    valign: 'bottom'
                    halign: 'center'
                    markup: 'true'
                    color: hex('#e64a19ff')
                    opacity: 0
                Label:
                    id: error_message_bottom
                    font_size: '20sp'
                    text: "Stuck on this screen? Contact us at https://www.yetitool.com/support"
                    text_size: self.size
                    valign: 'bottom'
                    halign: 'center'
                    markup: 'true'
                    color: hex('#e64a19ff')
                    opacity: 0

            BoxLayout:
                orientation: 'vertical'
                width: dp(800)
                height: dp(80)
                padding: [dp(254.5),0,dp(254.5),0]
                size_hint: (None,None)

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(79)
                    width: dp(291)
                    
                    Button:
                        background_normal: "./asmcnc/apps/warranty_app/img/next.png"
                        background_down: "./asmcnc/apps/warranty_app/img/next.png"
                        border: [dp(14.5)]*4
                        size_hint: (None,None)
                        width: dp(291)
                        height: dp(79)
                        on_press: root.next_screen(auto=False)
                        text: 'Next...'
                        font_size: '30sp'
                        color: hex('#f9f9f9ff')
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
                                
            BoxLayout:
                orientation: 'vertical'
                padding: [10, 0, 0, 10]
                size_hint: (None,None)
                width: dp(70)
                height: dp(62)

                Button:
                    size_hint: (None,None)
                    height: dp(52)
                    width: dp(60)
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


""")

class WarrantyScreen4(Screen):

    activationcode = ObjectProperty()
    activation_code_filepath = "/home/pi/smartbench_activation_code.txt"
    activation_code_from_file = 0
    check_activation_event = None

    def __init__(self, **kwargs):
        super(WarrantyScreen4, self).__init__(**kwargs)
        self.wm=kwargs['warranty_manager']
        self.m=kwargs['machine']
        
        self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#1976d2'

    def on_pre_enter(self):
        self.read_in_activation_code()

    def on_enter(self):
        self.check_activation_event = Clock.schedule_interval(lambda dt: self.next_screen(), 2)

    def read_in_activation_code(self):
        try: 
            file = open(self.activation_code_filepath, 'r')
            self.activation_code_from_file  = int(str(file.read()))
            file.close()

        except: 
            self.error_message_top.opacity = 1
            self.error_message_top.text = 'Could not check activation code!'
            self.error_message_bottom.opacity = 1

    def check_activation_code(self):

        if self.activation_code.text != '':
            if int(self.activation_code.text) == self.activation_code_from_file:
                if os.path.isfile(self.activation_code_filepath): os.remove(self.activation_code_filepath)
                return True
            else: 
                return False
        else:
            return False

    def next_screen(self, auto = True):

        if self.check_activation_code():
            if self.check_activation_event != None: Clock.unschedule(self.check_activation_event)
            self.activation_code.focus = False
            try: 
                self.wm.sm.current = 'warranty_5'
            except: 
                if self.check_activation_event != None: Clock.unschedule(self.check_activation_event)

        elif auto == True:
            pass

        else: 
            self.error_message_top.opacity = 1
            self.error_message_bottom.opacity = 1

    def go_back(self):
        self.wm.sm.current = 'warranty_3'

    def on_leave(self):
        if self.check_activation_event != None: Clock.unschedule(self.check_activation_event)
