'''
Created March 2019

@author: Ed

Squaring decision: manual or auto?
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import popup_info
from datetime import datetime


Builder.load_string("""

<LiftZOnPauseDecisionScreen>:


    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: 20
        orientation: 'vertical'




        Label:
            id: pause_reason_label
            size_hint_y: 3
            markup: True
            text: "[color=333333]If the job pauses, should SmartBench automatically lift the Z axis away from the job?[/color]"
            font_size: '30px' 
            valign: 'center'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
    
        BoxLayout:
            orientation: 'horizontal'
            padding: [20,0,20,0]
            spacing: 40
            size_hint_y: 3

            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.decision_no()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/decision_no.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Button:
                size_hint_x: 0.3
                background_color: hex('#FFFFFF00')
                on_press: root.popup_help()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/help_btn_orange_round.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.decision_yes()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/decision_yes.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
        Label:
            size_hint_y: .5                

""")


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class LiftZOnPauseDecisionScreen(Screen):
    
    
    def __init__(self, **kwargs):
        
        super(LiftZOnPauseDecisionScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
 
    
    def popup_help(self):
        
        info = "[b]Automatic lifting during a pause... (recommended for most tools)[/b]\n\n" \
                "If paused during a job, SmartBench can be set to automatically lift the Z axis, moving the tool away from the job. " \
                "This can be useful to inspect the work or clear any blockages. " \
                "Also, it allows the spindle to decelerate away from the job, avoiding burn marks. " \
                "On resuming, SmartBench automatically handles returning the tool to the correct position before continuing. " \
                "[b]Do not[/b] allow this feature if the tool has any inverted horizontal features which would rip through the job if the tool were to be lifted (e.g. a biscuit cutter tool profile). " 
        popup_info.PopupInfo(self.sm, 700, info)
 
    
    def on_enter(self):

        pass
    
    
    def decision_no(self):
        
        if self.m.fw_can_operate_zUp_on_pause():  # precaution (this screen shouldn't appear if fw not capable)
            self.sm.get_screen('go').lift_z_on_job_pause = False
        self.sm.current = 'go'

    
    def decision_yes(self):

        if self.m.fw_can_operate_zUp_on_pause():  # precaution (this screen shouldn't appear if fw not capable)
            self.sm.get_screen('go').lift_z_on_job_pause = True
        self.sm.current = 'go'