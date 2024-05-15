"""
Created on 18 November 2020
GRBL settings screen for system tools app

@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

<GRBLSettingsScreen>
    BoxLayout:
        height: app.get_scaled_height(800.0)
        width: app.get_scaled_width(480.0)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing: app.get_scaled_width(10.0)
            orientation: "vertical"
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: app.get_scaled_height(60.0)
                    width: app.get_scaled_width(800.0)
                    text: "GRBL settings"
                    color: hex('#f9f9f9ff')
                    font_size: app.get_scaled_width(30.0)
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(320.0)
                padding: app.get_scaled_tuple([20.0, 20.0])
                spacing: 0
                orientation: 'vertical'

                GridLayout: 
                    size: self.size
                    pos: self.parent.pos
                    cols: 3
                    rows: 3
                    size_hint_y: 0.67

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Download to USB'
                        on_press: root.download_grbl_settings()
                                
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Save to file'
                        on_press: root.save_grbl_settings()
                                   
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''
                        
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Restore from USB'
                        on_press: root.restore_grbl_settings_from_usb()

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Restore from file'
                        on_press: root.restore_grbl_settings_from_file()

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Bake defaults'
                        on_press: root.bake_default_settings()

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: '$RST=$'
                        on_press: root.send_rst_dollar()
                                   
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: '$RST=*'
                        on_press: root.send_rst_star()
                        
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: '$RST=#'
                        on_press: root.send_rst_hash()

            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(80.0)
                padding: 0
                spacing: app.get_scaled_width(10.0)
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(80.0)
                    height: app.get_scaled_height(80.0)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: app.get_scaled_height(80.0)
                        width: app.get_scaled_width(80.0)
                        padding: app.get_scaled_tuple([10.0, 10.0, 10.0, 10.0])
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(52.0)
                            width: app.get_scaled_width(60.0)
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
                    width: app.get_scaled_width(620.0)
                    height: app.get_scaled_height(80.0)
                    padding: app.get_scaled_tuple([10.0, 10.0])
                    spacing: 0
                    orientation: 'vertical'

                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(80.0)
                    height: app.get_scaled_height(80.0)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: app.get_scaled_height(80.0)
                        width: app.get_scaled_width(80.0)
                        padding: app.get_scaled_tuple([19.0, 10.0, 10.0, 10.0])
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(60.0)
                            width: app.get_scaled_width(51.0)
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


class GRBLSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(GRBLSettingsScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs["system_tools"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

# ADD A BUNCH OF WARNING POPUPS 

    def download_grbl_settings(self):
        self.systemtools_sm.download_grbl_settings_to_usb()

    def save_grbl_settings(self):
        self.m.save_grbl_settings()

    def restore_grbl_settings_from_usb(self):
        self.systemtools_sm.restore_grbl_settings_from_usb()

    def restore_grbl_settings_from_file(self):
        self.systemtools_sm.restore_grbl_settings_from_file()

    def bake_default_settings(self):
        if not self.m.bake_default_grbl_settings():
            popup_info.PopupError(
                self.systemtools_sm.sm,
                self.l,
                "X current read in as 0! Can't set correct Z travel.",
            )

    def send_rst_dollar(self):
        self.m.send_any_gcode_command("$RST=$")

    def send_rst_star(self):
        self.m.send_any_gcode_command("$RST=*")

    def send_rst_hash(self):
        self.m.send_any_gcode_command("$RST=#")
