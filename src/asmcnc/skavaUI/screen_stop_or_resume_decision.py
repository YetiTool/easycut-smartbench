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
        self.jd = kwargs['job']
        self.db = kwargs['database']
        self.l=kwargs['localization']
    
    def popup_help(self):

        info = (
            self.l.get_bold('Cancel')  + '[b]' +  " (X)" +'[/b]' + \
            "\n" + \
            self.l.get_str("Pressing cancel will cancel the job.") + \
            "\n\n" + \
            self.l.get_bold('Resume') + '[b]' +  " (>)" +'[/b]' + \
            "\n" + \
            self.l.get_str("Pressing resume will continue the job from the point at which it was paused.")
        )

        if 'yetipilot' not in self.reason_for_pause:
            popup_info.PopupInfo(self.sm, self.l, 500, info)
        else:
            info += (
                "\n\n" + \
                self.l.get_bold('Scan the QR code to learn more about this error.') + \
                "\n" + \
                self.l.get_bold("Or visit <URL>").replace('<URL>', 'www.yetitool.com/support > Knowledge Base')
            )

            popup_info.PopupQRInfo(self.sm, self.l, 500, info, "./asmcnc/skavaUI/img/qr_yetipilot_info.png")
 
    
    def on_enter(self):

        # Update go screen button in case this screen was called from outside go screen (e.g. spindle overload)
        try: self.sm.get_screen('go').start_or_pause_button_image.source = "./asmcnc/skavaUI/img/resume.png"
        except: pass

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
        
        if self.reason_for_pause == 'job_pause':
            self.pause_reason_label.text = self.l.get_str("SmartBench is paused.")
            self.pause_description_label.text = self.l.get_str("You may resume, or cancel the job at any time.")

        if self.reason_for_pause == 'yetipilot_low_feed':
            self.pause_reason_label.text = self.l.get_str("Feed rate too slow!")

            self.pause_description_label.text = (

                self.l.get_str('YetiPilot has tried to reduce the feed rate to less than 10% of the feed rate in the job file.') + \
                "\n\n" + \
                self.l.get_str("This may be because the chosen feed rate in the job file was set too high, or because of a problem with the cut which means the Spindle motor's target power cannot be reached.") + \
                " " + \
                self.l.get_str('Press "?" for more information.') + "\n\n" + \
                self.l.get_bold('We recommend that you cancel the job and correct the issue.') + " " + \
                self.l.get_str('Or, you may resume the job with YetiPilot initially disabled.').replace(self.l.get_str('Or, you may resume'),self.l.get_bold('Or, you may resume')) + " " + \
                self.l.get_str('If you choose to resume, SmartBench may struggle.')
                )

        if self.reason_for_pause == 'yetipilot_spindle_data_loss':
            self.pause_reason_label.text = self.l.get_str("Can't read spindle data!")

            self.pause_description_label.text = (

                self.l.get_str('Cannot read the data from the SC2 Spindle motor, which is needed to measure the load.') + \
                "\n\n" + \
                self.l.get_str("Please check that you are using your SC2 Spindle motor, and check that your data cable is connected.") + \
                " " + \
                self.l.get_str('Press "?" for more information.') + "\n\n" + \
                self.l.get_str('You may resume the job with YetiPilot disabled, or cancel the job altogether.').replace(self.l.get_str('You may resume'),self.l.get_bold('You may resume'))
                )

    
    def cancel_job(self):
        popup_info.PopupConfirmJobCancel(self.sm, self.l)

    def confirm_job_cancel(self):
        self.m.stop_from_soft_stop_cancel()
        self.m.s.is_ready_to_assess_spindle_for_shutdown = True # allow spindle overload assessment to resume
        
        self.sm.get_screen('job_incomplete').prep_this_screen('cancelled', event_number=False)
        self.sm.current = 'job_incomplete'

    def resume_job(self):

        if self.reason_for_pause == 'yetipilot_low_feed':
            self.sm.get_screen('go').yp_widget.disable_yeti_pilot()

        self.sm.current = self.return_screen
