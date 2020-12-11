'''
Created on 18 November 2020
Build info screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<BuildInfoScreen>

    sw_version_label: sw_version_label
    pl_version_label: pl_version_label
    sw_hash_label: sw_hash_label
    sw_branch_label: sw_branch_label
    pl_hash_label: pl_hash_label  
    pl_branch_label: pl_branch_label
    fw_version_label: fw_version_label
    hw_version_label: hw_version_label
    zh_version_label: zh_version_label
    machine_serial_number_label: machine_serial_number_label

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing: 10
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
                    height: dp(60)
                    width: dp(800)
                    text: "Build Information"
                    color: hex('#f9f9f9ff')
                    # color: hex('#333333ff') #grey
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(320)
                padding: 0
                spacing: 0

                GridLayout: 
                    size: self.parent.size
                    pos: self.parent.pos
                    cols: 6
                    rows: 4

                    Label: 
                        text: ''
                    Label: 
                        text: 'Software'
                        color: [0,0,0,1]
                    Label: 
                        text: 'Platform'
                        color: [0,0,0,1]
                    Label: 
                        text: 'Firmware'
                        color: [0,0,0,1]
                    Label: 
                        text: 'Z head'
                        color: [0,0,0,1]
                    Label: 
                        text: 'Hardware'
                        color: [0,0,0,1]
                    Label: 
                        text: 'Version'
                        color: [0,0,0,1]
                    Label:
                        id: sw_version_label
                        text: 'SW_version'
                        color: [0,0,0,1]
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        id: pl_version_label
                        text: 'PL_version'
                        color: [0,0,0,1]
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        id: fw_version_label
                        text: 'FW_version'
                        color: [0,0,0,1]
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        id: zh_version_label
                        text: 'ZH_version'
                        color: [0,0,0,1]
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        id: hw_version_label
                        text: 'HW_version'
                        color: [0,0,0,1]
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        text: 'Branch'
                        color: [0,0,0,1]
                    Label: 
                        id: sw_branch_label
                        text: 'SW_branch'
                        color: [0,0,0,1]
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        id: pl_branch_label
                        text: 'PL_branch'
                        color: [0,0,0,1]
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        text: '-'
                        color: [0,0,0,1]
                    Label: 
                        text: '-'
                        color: [0,0,0,1]
                    Label: 
                        text: '-'
                        color: [0,0,0,1]
                    Label: 
                        text: 'Commit'
                        color: [0,0,0,1]
                    Label: 
                        id: sw_hash_label
                        text: 'SW_commit'
                        color: [0,0,0,1]
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        id: pl_hash_label
                        text: 'PL_commit'
                        color: [0,0,0,1]
                        markup: 'True'
                        halign: 'center'
                    Label: 
                        text: '-'
                        color: [0,0,0,1]
                    Label: 
                        text: '-'
                        color: [0,0,0,1]
                    Label: 
                        text: '-'
                        color: [0,0,0,1]

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding: 0
                spacing: 0
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    # width: dp(192.5)
                    # height: dp(130)
                    width: dp(80)
                    height: dp(80)
                    padding: 0
                    spacing: 0
                    # canvas:
                    #     Color:
                    #         rgba: [1,1,1,1]
                    #     RoundedRectangle:
                    #         pos: self.pos
                    #         size: self.size
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(80)
                        width: dp(80)
                        padding: [10, 10, 10, 10]
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

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(620)
                    height: dp(80)
                    padding: 10
                    spacing: 0
                    orientation: 'vertical'
                    # canvas:
                    #     Color:
                    #         rgba: [1,1,1,1]
                    #     RoundedRectangle:
                    #         pos: self.pos
                    #         size: self.size
                    Label:
                        text: 'Machine Info'
                        color: [0,0,0,1]
                        size_hint_y: 0.2

                    GridLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        cols: 2
                        rows: 3

                        Label:
                            text: 'Serial number:'
                            color: [0,0,0,1]
                        Label:
                            id: machine_serial_number_label
                            text: ''
                            color: [0,0,0,1]
                        Label:
                            text: 'Model:'
                            color: [0,0,0,1]
                        Label:
                            text: '-'
                            color: [0,0,0,1]
                        Label:
                            text: 'Console serial number:'
                            color: [0,0,0,1]
                        Label:
                            text: '-'
                            color: [0,0,0,1]

                BoxLayout:
                    size_hint: (None,None)
                    # width: dp(192.5)
                    # height: dp(130)
                    width: dp(80)
                    height: dp(80)
                    padding: 0
                    spacing: 0
                    # canvas:
                    #     Color:
                    #         rgba: [1,1,1,1]
                    #     RoundedRectangle:
                    #         pos: self.pos
                    #         size: self.size
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(130)
                        width: dp(80)
                        padding: [19, 10, 10, 10]
                        Button:
                            size_hint: (None,None)
                            height: dp(60)
                            width: dp(51)
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

class BuildInfoScreen(Screen):

    def __init__(self, **kwargs):
        super(BuildInfoScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']
        self.set = kwargs['settings']

        self.sw_version_label.text = self.set.sw_version
        self.pl_version_label.text = self.set.platform_version
        self.latest_sw_version = self.set.latest_sw_version
        self.latest_platform_version = self.set.latest_platform_version
        self.sw_hash_label.text = self.set.sw_hash
        self.sw_branch_label.text = self.set.sw_branch
        self.pl_hash_label.text = self.set.pl_hash
        self.pl_branch_label.text = self.set.pl_branch

        self.hw_version_label.text = self.m.s.hw_version
        self.zh_version_label.text = str(self.m.z_head_version())
        try: self.machine_serial_number_label.text = 'YS6' + str(self.m.serial_number())[0:4]
        except: self.machine_serial_number_label.text = 'YS6'


    ## EXIT BUTTONS
    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    ## GET BUILD INFO
    def on_pre_enter(self, *args):
        self.m.send_any_gcode_command('$I')

    def on_enter(self, *args):
        self.scrape_fw_version()

    def scrape_fw_version(self):
        self.fw_version_label.text = str((str(self.m.s.fw_version)).split('; HW')[0])
