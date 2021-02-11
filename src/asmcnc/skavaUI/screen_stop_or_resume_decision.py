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
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class StopOrResumeDecisionScreen(Screen):
    
    
    reason_for_pause = None
    return_screen = 'lobby'
    
    def __init__(self, **kwargs):
        
        super(StopOrResumeDecisionScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
 
    
    def popup_help(self):
        
        # info = "[b]Cancel[/b]\n" \
        #         "Pressing cancel will cancel the job. If the job is restarted, it will restart from the beginning of the job.\n\n" \
        #         "[b]Resume[/b]\n" \
        #         "Pressing resume will continue the job from the point at which it was paused."

        info = (
            self.l.get_bold('Cancel') + \
            "\n" + \
            self.l.get_str("Pressing cancel will cancel the job. If the job is restarted, it will restart from the beginning of the job.") + \
            "\n\n" + \
            self.l.get_bold('Resume') + \
            "\n" + \
            self.l.get_str("Pressing resume will continue the job from the point at which it was paused.")
        )

        popup_info.PopupInfo(self.sm, self.l, 500, info)
 
    
    def on_enter(self):

        if self.reason_for_pause == 'spindle_overload':
            self.pause_reason_label.text = self.l.get_str("Spindle motor was overloaded!").replace(self.l.get_str('overloaded'), self.l.get_bold('overloaded'))

            self.pause_description_label.text = (

                self.l.get_str('SmartBench has automatically stopped the job because it detected the spindle was starting to overload.') + \
                "\n" + \
                self.l.get_str(
                    'You may resume, but we recommend you allow the spindle to cool off first.'
                    ).replace(self.l.get_str('You may resume'),self.l.get_bold('You may resume')) + \
                "\n" + \
                self.l.get_str('Try adjusting the speeds and feeds to reduce the load on the spindle, or adjust the job to reduce chip loading.') + " " + \
                self.l.get_str('Check extraction, air intake, exhaust, worn brushes, work-holding, blunt cutters or anything else which may strain the spindle.')
                )

            # self.pause_description_label.text = "[color=333333]SmartBench has automatically stopped the job because it detected the spindle was starting to overload. " \
            #                                 "This is calculated on motor temperature, spindle load and RPM. " \
            #                                 "[b]You may resume[/b], but we recommend you allow the spindle to cool off a bit first. " \
            #                                 "If resuming, try adjusting the speeds and feeds to reduce the load on the spindle. " \
            #                                 "Or adjust the job to reduce the chip loading. " \
            #                                 "Also, check other factors like extraction, air intake, exhaust, worn brushes, work-holding, blunt cutters or anything else which may give the spindle a hard time.[/color]"
        
        if self.reason_for_pause == 'job_pause':
            self.pause_reason_label.text = self.l.get_str("SmartBench is paused.")
            self.pause_description_label.text = self.l.get_str("You may resume, or cancel the job at any time.")

    
    def cancel_job(self):
        popup_info.PopupConfirmJobCancel(self.sm, self.l)

    def confirm_job_cancel(self):
        self.m.stop_from_soft_stop_cancel()

        self.m.s.is_ready_to_assess_spindle_for_shutdown = True # allow spindle overload assessment to resume
        
        if self.return_screen == 'go':
            self.sm.get_screen('go').is_job_started_already = False
            self.sm.get_screen('go').temp_suppress_prompts = True
        self.sm.current = self.return_screen

    
    def resume_job(self):

        self.m.resume_after_a_stream_pause()
        self.m.s.is_ready_to_assess_spindle_for_shutdown = True # allow spindle overload assessment to resume
        self.sm.current = self.return_screen
