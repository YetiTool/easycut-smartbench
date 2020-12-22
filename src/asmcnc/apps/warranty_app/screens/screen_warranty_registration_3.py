'''
Created on nov 2020
@author: Ollie
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar
Builder.load_string("""

<WarrantyScreen3>:

    status_container:status_container
    serial_number_label:serial_number_label

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
                text: "[color=333333ff]Your serial number is[/color]"
                text_size: self.size
                valign: 'bottom'
                halign: 'center'
                markup: 'true'
                bold: True

            BoxLayout:
                orientation: 'vertical'
                width: dp(800)
                height: dp(200)
                padding: 20
                size_hint: (None,None)
                Label:
                    id: serial_number_label
                    size_hint_y: 1
                    font_size: '30sp'
                    text_size: self.size
                    valign: 'middle'
                    halign: 'center'
                    markup: 'true'
                    color: hex('#333333ff')

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
                        on_press: root.next_screen()
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

class WarrantyScreen3(Screen):

    def __init__(self, **kwargs):
        super(WarrantyScreen3, self).__init__(**kwargs)
        self.wm=kwargs['warranty_manager']
        self.m=kwargs['machine']
        
        self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#1976d2'

        self.serial_number_label.text = self.get_serial_number()

    def get_serial_number(self):
        serial_number_filepath = "/home/pi/smartbench_serial_number.txt"
        serial_number_from_file = ''

        try: 
            file = open(serial_number_filepath, 'r')
            serial_number_from_file  = str(file.read())
            file.close()

        except: 
            print 'Could not get serial number! Please contact YetiTool support!'

        return str(serial_number_from_file)

    def next_screen(self):
        self.wm.sm.current = 'warranty_4'

    def go_back(self):
        self.wm.sm.current = 'warranty_2'
    

