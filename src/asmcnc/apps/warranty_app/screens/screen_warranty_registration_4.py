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

    status_container : status_container
    enter_your_activation_code_label : enter_your_activation_code_label
    activation_code : activation_code
    error_message_top : error_message_top
    error_message_bottom : error_message_bottom
    next_button : next_button

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
                id: enter_your_activation_code_label
                font_size: '30sp'
                # text: "[color=333333ff]Enter your activation code:[/color]"
                text_size: self.size
                valign: 'bottom'
                halign: 'center'
                markup: 'true'
                bold: True
                color: hex('#333333ff')

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
                    color: hex('#333333ff')
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
                    opacity: 1 # EDITED!
                Label:
                    id: error_message_bottom
                    font_size: '20sp'
                    text: "Stuck on this screen? Contact us at https://www.yetitool.com/support"
                    text_size: self.size
                    valign: 'bottom'
                    halign: 'center'
                    markup: 'true'
                    color: hex('#e64a19ff')
                    opacity: 1 # EDITED!

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
                        id: next_button
                        background_normal: "./asmcnc/apps/warranty_app/img/next.png"
                        background_down: "./asmcnc/apps/warranty_app/img/next.png"
                        border: [dp(14.5)]*4
                        size_hint: (None,None)
                        width: dp(291)
                        height: dp(79)
                        on_press: root.next_screen(auto=True) # EDITED!
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

    default_font_size = '20sp'

    def __init__(self, **kwargs):
        super(WarrantyScreen4, self).__init__(**kwargs)
        self.wm=kwargs['warranty_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
        
        self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#1976d2'

        self.update_strings()
        self.update_font_size(self.error_message_bottom)

    def on_pre_enter(self):
        self.read_in_activation_code()

    def on_enter(self):
        self.check_activation_event = Clock.schedule_interval(lambda dt: self.next_screen(), 2)

    def read_in_activation_code(self):
        try: 
            file = open(self.activation_code_filepath, 'r')
            self.activation_code_from_file  = int(str(file.read()))
            file.close()

            if self.activation_code_from_file == '':
                self.backup_generate_activation_code()

        except: 
            # self.error_message_top.opacity = 1
            # self.error_message_top.text = 'Checking activation code...'
            self.backup_generate_activation_code()

    def backup_generate_activation_code(self):
        self.activation_code_from_file = self.generate_activation_code(self.wm.sm.get_screen('warranty_3').serial_number_label.text)
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

        self.wm.sm.current = 'warranty_5' # TESTING!

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

    def generate_activation_code(self, serial_number):
        ActiveTempNoOnly = int(''.join(filter(str.isdigit, serial_number)))
        print (str(ActiveTempNoOnly)+'\n')
        ActiveTempStart = str(ActiveTempNoOnly * 76289103623 + 20)
        print (ActiveTempStart+'\n')
        ActiveTempStartReduce = ActiveTempStart[0:15]
        print (ActiveTempStartReduce+'\n')
        Activation_Code_1 = int(ActiveTempStartReduce[0])*171350;
        Activation_Code_2 = int(ActiveTempStartReduce[3])*152740;
        Activation_Code_3 = int(ActiveTempStartReduce[5])*213431; 
        Activation_Code_4 = int(ActiveTempStartReduce[7])*548340;
        Activation_Code_5 = int(ActiveTempStartReduce[11])*115270;
        Activation_Code_6 = int(ActiveTempStartReduce[2])*4670334;
        Activation_Code_7 = int(ActiveTempStartReduce[7])*789190;
        Activation_Code_8 = int(ActiveTempStartReduce[6])*237358903;
        Activation_Code_9 = int(ActiveTempStartReduce[6])*937350;
        Activation_Code_10 = int(ActiveTempStartReduce[6])*105430;
        Activation_Code_11 = int(ActiveTempStartReduce[6])*637820;
        Activation_Code_12 = int(ActiveTempStartReduce[6])*67253489;
        Activation_Code_13 = int(ActiveTempStartReduce[6])*53262890;
        Activation_Code_14 = int(ActiveTempStartReduce[6])*89201233;
        Final_Activation_Code = Activation_Code_1 + Activation_Code_2 + Activation_Code_3 +Activation_Code_4 + Activation_Code_5 + Activation_Code_6 + Activation_Code_7 + Activation_Code_8 + Activation_Code_9 + Activation_Code_10 + Activation_Code_11 + Activation_Code_12 + Activation_Code_13 + Activation_Code_14
        print(str(Final_Activation_Code)+'\n')
        return Final_Activation_Code

    def update_strings(self):
        self.enter_your_activation_code_label.text = self.l.get_str("Enter your activation code:")
        self.error_message_top.text = self.l.get_str("Please check your activation code.")
        self.error_message_bottom.text = self.l.get_str("Stuck on this screen? Contact us at https://www.yetitool.com/support")
        self.next_button.text = self.l.get_str("Next") + "..."

    def update_font_size(self, value):
        if len(value.text) < 85: value.font_size = self.default_font_size
        else: value.font_size = '18sp'
