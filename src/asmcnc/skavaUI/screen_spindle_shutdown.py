"""
Created March 2019

@author: Ed

Prepare to home
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock
from datetime import datetime
Builder.load_string(
    """

<SpindleShutdownScreen>:

    pausing_label : pausing_label
    label_wait : label_wait

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: 40
        orientation: 'vertical'

        Label:
            size_hint_y: 1 
            
        Label:
            id: pausing_label
            size_hint_y: 1
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: hex('#333333ff')

        Label:
            id: label_wait
            size_hint_y: 1
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: hex('#333333ff')

        Label:
            size_hint_y: 1                        

        Button:
            size_hint_y: 4
            background_color: hex('#FFFFFF00')
            BoxLayout:
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/spindle_shutdown_wait.png"
                    size: self.parent.width, self.parent.height
                    allow_stretch: True 
                        
        Label:
            size_hint_y: 1                

"""
    )


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


class SpindleShutdownScreen(Screen):
    reason_for_pause = None
    return_screen = 'lobby'
    time_to_allow_spindle_to_rest = 2
    poll_interval_between_checking_z_rest = 0.5
    last_z_pos = 0
    spindle_decel_poll = None
    z_rest_poll = None

    def __init__(self, **kwargs):
        super(SpindleShutdownScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.jd = kwargs['job']
        self.db = kwargs['database']
        self.l = kwargs['localization']
        self.label_wait.text = self.l.get_str('Please wait') + '.'

    def on_pre_enter(self):
        if self.m.stylus_router_choice == 'router':
            self.pausing_label.text = self.l.get_str(
                'SmartBench is pausing the spindle motor.')
        elif self.m.stylus_router_choice == 'stylus':
            self.pausing_label.text = self.l.get_str(
                'SmartBench is raising the Z axis.')

    def on_enter(self):
        log('Pausing job...')
        if self.reason_for_pause == 'spindle_overload':
            self.db.send_event(1, 'Job paused', 
                'Paused job (Spindle overload): ' + self.jd.job_name, 3)
        elif self.reason_for_pause == 'job_pause':
            self.db.send_event(0, 'Job paused', 'Paused job (User): ' +
                self.jd.job_name, 3)
        self.z_rest_poll = None
        self.spindle_decel_poll = Clock.schedule_once(self.
            start_polling_for_z_rest, self.time_to_allow_spindle_to_rest)

    def start_polling_for_z_rest(self, dt):
        self.z_rest_poll = Clock.schedule_interval(self.poll_for_z_rest,
            self.poll_interval_between_checking_z_rest)

    def poll_for_z_rest(self, dt):
        current_z_pos = self.m.z_pos_str()
        if current_z_pos == self.last_z_pos:
            self.sm.get_screen('stop_or_resume_job_decision'
                ).reason_for_pause = self.reason_for_pause
            self.sm.get_screen('stop_or_resume_job_decision'
                ).return_screen = self.return_screen
            self.sm.current = 'stop_or_resume_job_decision'
        else:
            self.last_z_pos = current_z_pos

    def on_leave(self):
        if self.spindle_decel_poll != None:
            self.spindle_decel_poll.cancel()
        if self.z_rest_poll != None:
            self.z_rest_poll.cancel()
        self.return_screen = 'lobby'
