'''
Created on 8 June 2020
Tabbed maintenance screen, for setting the laser datum; monitoring brush life. 

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

from asmcnc.apps.shapeCutter_app.screens import popup_info
from __builtin__ import False

Builder.load_string("""

<MaintenanceScreenClass>

    BoxLayout:
        size_hint: (None,None)
        width: dp(800)
        height: dp(480)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(800)
            height: dp(90)
            padding: 0
            spacing: 0

            TabbedPanel:
                id: tab_panel
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                do_default_tab: False
                tab_pos: 'left_top'
                tab_height: 90
                tab_width: 142

                TabbedPanelItem:
                    background_normal: 'asmcnc/maintenance_app/img/laser_datum_tab_blue.png'
                    background_down: 'asmcnc/maintenance_app/img/laser_datum_tab_grey.png'
                    BoxLayout:
                        orientation: "horizontal" 
                        padding: 0
                        spacing: 10
                        canvas:
                            Color:
                                rgba: hex('#E5E5E5FF')
                            Rectangle:
                                size: self.size
                                pos: self.pos

                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(360)
                            width: dp(280)
                            orientation: "vertical"
                            id: left_panel
                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(70)
                                width: dp(280)
                                id: title
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(280)
                                width: dp(280)
                                id: button_container
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(360)
                            width: dp(270)
                            orientation: "vertical"
                            id: middle_panel
                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(70)
                                width: dp(270)
                                id: on_off_toggle
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(280)
                                width: dp(270)
                                id: xy_move_container
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(360)
                                width: dp(210)
                                id: z_move_container
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos            

""")

class MaintenanceScreenClass(Screen):
    
    info_button = ObjectProperty()
    
    screen_number = StringProperty("[b]I[/b]")
    title_label = StringProperty("[b]Using the app[/b]")
#     user_instructions = StringProperty()
    
    instructions_list = ["Use the Back and Next buttons to move through each section.\n\n",
                                       "Use the navigation tabs to move between sections.\n\n",
                                       "Press the [b]i[/b] if you need more information.\n\n",
                                       "For more help, see the video at www.yetitool.com/support"]