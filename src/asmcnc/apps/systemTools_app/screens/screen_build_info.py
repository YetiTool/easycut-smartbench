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
                    text: "Build Information"
                    color: [0,0,0,1]
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(240)
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size

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
                        id: SW_version
                        text: 'SW_version'
                        color: [0,0,0,1]
                    Label: 
                        id: PL_version
                        text: 'PL_version'
                        color: [0,0,0,1]
                    Label: 
                        id: FW_version
                        text: 'FW_version'
                        color: [0,0,0,1]
                    Label: 
                        id: ZH_version
                        text: 'ZH_version'
                        color: [0,0,0,1]
                    Label: 
                        id: HW_version
                        text: 'HW_version'
                        color: [0,0,0,1]
                    Label: 
                        text: 'Branch'
                        color: [0,0,0,1]
                    Label: 
                        id: SW_branch
                        text: 'SW_branch'
                        color: [0,0,0,1]
                    Label: 
                        id: PL_branch
                        text: 'PL_branch'
                        color: [0,0,0,1]
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
                        id: SW_commit
                        text: 'SW_commit'
                        color: [0,0,0,1]
                    Label: 
                        id: PL_commit
                        text: 'PL_commit'
                        color: [0,0,0,1]
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
                width: dp(780)
                height: dp(130)
                padding: 0
                spacing: 10
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(385)
                    height: dp(130)
                    padding: 0
                    spacing: 0
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(385)
                    height: dp(130)
                    padding: 0
                    spacing: 0
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size


""")

class BuildInfoScreen(Screen):

    def __init__(self, **kwargs):
        super(BuildInfoScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']

    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()