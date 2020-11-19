'''
Created on 18 November 2020
Beta testers screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<BetaTestersScreen>
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
                    text: "Beta Testing"
                    color: [0,0,0,1]
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(240)
                padding: [40,20]
                spacing: 20
                orientation: 'vertical'
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size

                Label
                    text: 'Run developer branch:'
                    color: [0,0,0,1]
                    font_size: 20
                    halign: "left"
                    markup: True
                    size_hint_y: 0.3
                    text_size: self.size

                TextInput:
                    id: user_branch
                    text: 'branch'
                    multiline: False
                    size_hint_y: 0.6
                    font_size: 20

                Button:
                    text: 'Checkout and pull'
                    on_press: root.checkout_branch()


            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(130)
                padding: 0
                spacing: 10
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
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
                    width: dp(375)
                    height: dp(130)
                    padding: 0
                    spacing: 0
                    orientation: 'vertical'
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                    GridLayout:
                        size_hint_y: 0.4
                        pos: self.parent.pos
                        cols: 2
                        rows: 0
                        padding: 10

                        Label:
                            text: 'Latest beta version:'
                            color: [0,0,0,1]
                            font_size: 20
                            markup: True

                        Label:
                            id: beta_version
                            text: 'beta_version_no'
                            color: [0,0,0,1]
                            font_size: 20
                            markup: True

                    BoxLayout:
                        padding: [30, 10]
                        Button:
                            text: 'Update to beta'



                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
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

class BetaTestersScreen(Screen):

    def __init__(self, **kwargs):
        super(BetaTestersScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.set = kwargs['settings']

        self.user_branch.text = (self.set.sw_branch).strip('*')

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def checkout_branch(self):
        if sys.platform != 'win32' and sys.platform != 'darwin':       
            os.system("cd /home/pi/easycut-smartbench/ && git fetch origin && git checkout " + str(self.user_branch.text))
            os.system("git pull")
            self.sm.current = 'rebooting'
