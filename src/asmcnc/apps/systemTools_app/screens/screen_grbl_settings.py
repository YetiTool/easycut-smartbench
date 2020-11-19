'''
Created on 18 November 2020
GRBL settings screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<GRBLSettingsScreen>
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
                    text: "GRBL Settings"
                    color: [0,0,0,1]
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
       
            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
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

                GridLayout: 
                    size: self.size
                    pos: self.parent.pos
                    cols: 3
                    rows: 3
                    size_hint_y: 0.67

                    Button:
                        text: 'Download to USB'
                        on_press: root.download_grbl_settings()
                                
                    Button:
                        text: 'Save to file'
                        on_press: root.save_grbl_settings()
                                   
                    Button:
                        text: ''
                        
                    Button:
                        text: 'Restore from USB'
                        on_press: root.restore_grbl_settings_from_usb()

                    Button:
                        text: 'Restore from file'
                        on_press: root.restore_grbl_settings_from_file()

                    Button:
                        text: 'Bake defaults'
                        on_press: root.bake_default_settings()

                    Button:
                        text: '$RST=$'
                        on_press: root.send_rst_dollar()
                                   
                    Button:
                        text: '$RST=*'
                        on_press: root.send_rst_star()
                        
                    Button:
                        text: '$RST=#'
                        on_press: root.send_rst_hash()

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
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_back.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(385)
                    height: dp(130)
                    padding: 0
                    spacing: 0
                    orientation: 'vertical'

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
                                    source: "./asmcnc/apps/wifi_app/img/quit.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True



""")

class GRBLSettingsScreen(Screen):

    def __init__(self, **kwargs):
        super(GRBLSettingsScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

# ADD A BUNCH OF WARNING POPUPS 


    def download_grbl_settings(self):
        self.systemtools_sm.download_grbl_settings()

    def save_grbl_settings(self):
        self.m.save_grbl_settings()

    def restore_grbl_settings_from_usb(self):
        self.systemtools_sm.restore_grbl_settings_from_usb()

    def restore_grbl_settings_from_file(self):
        self.systemtools_sm.restore_grbl_settings_from_file()    

    def bake_default_settings(self):
        self.bake_default_grbl_settings()

    def send_rst_dollar(self):
        self.m.send_any_gcode_command("$RST=$")

    def send_rst_star(self):
        self.m.send_any_gcode_command("$RST=*")

    def send_rst_hash(self):
        self.m.send_any_gcode_command("$RST=#")































