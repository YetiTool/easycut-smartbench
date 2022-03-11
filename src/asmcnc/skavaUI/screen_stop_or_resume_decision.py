# -*- coding: utf-8 -*-
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
from kivy.properties import ObjectProperty


Builder.load_string("""

<StopOrResumeDecisionScreen>:

    pause_reason_label:pause_reason_label
    pause_description_label:pause_description_label

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


        BoxLayout:
            orientation: 'vertical'
            spacing: 00
            padding: (0,10,0,20)
            size_hint_y: 5
            

            Label:
                id: pause_reason_label
                size_hint_y: 0.6
                markup: True
                font_size: '30px' 
                valign: 'center'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
         
            Label:
                id: pause_description_label
                size_hint_y: 2.4
                markup: True
                font_size: '18px' 
                valign: 'center'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
     
        BoxLayout:
            orientation: 'horizontal'
            spacing: 0
            size_hint_y: 3

            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.cancel_job()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/cancel_from_pause.png"
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
                        source: "./asmcnc/skavaUI/img/help_btn_yellow_round.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.resume_job()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/resume_from_pause.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
        Label:
            size_hint_y: .5                

""")


def log(message):
    timestamp = datetime.now()
    print((timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message)))


class StopOrResumeDecisionScreen(Screen):
    
    
    reason_for_pause = None
    return_screen = 'lobby'

    screen_manager = ObjectProperty()
    machine = ObjectProperty()
    job = ObjectProperty()
    database = ObjectProperty()
    localization = ObjectProperty()
    
    def __init__(self, **kwargs):
        
        super(StopOrResumeDecisionScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.jd = kwargs['job']
        self.db = kwargs['database']
        self.l=kwargs['localization']
    
    def popup_help(self):

        info = (
            self.localization.get_bold('Cancel') + \
            "\n" + \
            self.localization.get_str("Pressing cancel will cancel the job. If the job is restarted, it will restart from the beginning of the job.") + \
            "\n\n" + \
            self.localization.get_bold('Resume') + \
            "\n" + \
            self.localization.get_str("Pressing resume will continue the job from the point at which it was paused.")
        )

        popup_info.PopupInfo(self.sm, self.l, 500, info)
 
    
    def on_enter(self):

        if self.reason_for_pause == 'spindle_overload':
            self.pause_reason_label.text = self.localization.get_str("Spindle motor was overloaded!").replace(self.localization.get_str('overloaded'), self.localization.get_bold('overloaded'))

            self.pause_description_label.text = (

                self.localization.get_str('SmartBench has automatically stopped the job because it detected the spindle was starting to overload.') + \
                "\n" + \
                self.localization.get_str(
                    'You may resume, but we recommend you allow the spindle to cool off first.'
                    ).replace(self.localization.get_str('You may resume'),self.localization.get_bold('You may resume')) + \
                "\n" + \
                self.localization.get_str('Try adjusting the speeds and feeds to reduce the load on the spindle, or adjust the job to reduce chip loading.') + " " + \
                self.localization.get_str('Check extraction, air intake, exhaust, worn brushes, work-holding, blunt cutters or anything else which may strain the spindle.')
                )
        
        if self.reason_for_pause == 'job_pause':
            self.pause_reason_label.text = self.localization.get_str("SmartBench is paused.")
            self.pause_description_label.text = self.localization.get_str("You may resume, or cancel the job at any time.")

    
    def cancel_job(self):
        popup_info.PopupConfirmJobCancel(self.sm, self.l)

    def confirm_job_cancel(self):
        self.machine.stop_from_soft_stop_cancel()
        self.machine.s.is_ready_to_assess_spindle_for_shutdown = True # allow spindle overload assessment to resume
        
        self.screen_manager.get_screen('job_incomplete').prep_this_screen('cancelled', event_number=False)
        self.screen_manager.current = 'job_incomplete'

    def resume_job(self):

        self.machine.resume_after_a_stream_pause()

        # Job resumed, send event
        self.database.send_event(0, 'Job resumed', 'Resumed job: ' + self.job.job_name, 4)

        self.machine.s.is_ready_to_assess_spindle_for_shutdown = True # allow spindle overload assessment to resume
        self.screen_manager.current = self.return_screen
