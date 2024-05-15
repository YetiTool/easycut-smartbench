# -*- coding: utf-8 -*-
"""
Created July 2020

@author: Letty

Spindle cooldown screen
"""
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """

<SpindleCooldownScreen>:

    countdown: countdown
    cool_down_label : cool_down_label

    BoxLayout: 
        spacing: 0
        padding: app.get_scaled_tuple([20.0, 20.0])
        orientation: 'vertical'
        size_hint: (None, None)
        height: app.get_scaled_height(480.0)
        width: app.get_scaled_width(800.0)
        canvas:
            Color: 
                rgba: hex('#E5E5E5FF')
            Rectangle: 
                size: self.size
                pos: self.pos         

        BoxLayout: 
            spacing: 0
            padding: 
            orientation: 'vertical'
            canvas:
                Color: 
                    rgba: [1,1,1,1]
                RoundedRectangle:
                    size: self.size
                    pos: self.pos    
            
            Label:
                id: cool_down_label
                size_hint_y: 1
                # text: 'Cooling down spindle...'
                color: [0,0,0,1]
                markup: True
                font_size: str(0.0375*app.width) + 'px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size

            BoxLayout: 
                spacing: 0
                padding: app.get_scaled_tuple([100.0, 0, 100.0, 130.0])
                orientation: 'horizontal'          
                size_hint: (None, None)
                height: app.get_scaled_height(251.0)
                width: app.get_scaled_width(800.0)
                pos: self.parent.pos


                BoxLayout: 
                    spacing: 0
                    padding: app.get_scaled_tuple([8.0, 0, 57.0, 0])
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: app.get_scaled_height(121.0)
                    width: app.get_scaled_width(180.0)
                    Image:
                        id: spindle_icon
                        source: "./asmcnc/skavaUI/img/spindle_cooldown_on.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: app.get_scaled_height(121.0)
                        width: app.get_scaled_width(115.0)

                BoxLayout: 
                    spacing: 0
                    padding: app.get_scaled_tuple([0, 0, 0, 0])
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: app.get_scaled_height(121.0)
                    width: app.get_scaled_width(200.0)
                    Label:
                        id: countdown
                        markup: True
                        font_size: str(0.125*app.width) + 'px' 
                        valign: 'middle'
                        halign: 'center'
                        size:self.texture_size
                        text_size: self.size  
                        text: '10'
                        color: [0,0,0,1]

                BoxLayout: 
                    spacing: 0
                    padding: app.get_scaled_tuple([70.0, 0, 10.0, 3.0])
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: app.get_scaled_height(121.0)
                    width: app.get_scaled_width(180.0)
                    Image:
                        id: countdown_icon
                        source: "./asmcnc/skavaUI/img/countdown_big.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: app.get_scaled_height(118.0)
                        width: app.get_scaled_width(100.0)


"""
)


class SpindleCooldownScreen(Screen):
    return_screen = "job_feedback"
    seconds = "10"
    update_timer_event = None

    def __init__(self, **kwargs):
        super(SpindleCooldownScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.seconds = self.m.spindle_cooldown_time_seconds
        self.cool_down_label.text = self.l.get_str("Cooling down spindle") + "..."

    def on_pre_enter(self):
        self.m.cooldown_zUp_and_spindle_on()
        self.seconds = self.m.spindle_cooldown_time_seconds
        self.countdown.text = str(self.seconds)

    def on_enter(self):
        Clock.schedule_once(self.exit_screen, self.seconds)
        self.update_timer_event = Clock.schedule_interval(self.update_timer, 1)

    def exit_screen(self, dt):
        self.sm.current = self.return_screen

    def update_timer(self, dt):
        if self.seconds >= 0:
            self.seconds = self.seconds - 1
            self.countdown.text = str(self.seconds)

    def on_leave(self):
        self.m.turn_off_spindle()
        self.m.turn_off_vacuum()
        if self.update_timer_event != None:
            Clock.unschedule(self.update_timer_event)
        self.seconds = self.m.spindle_cooldown_time_seconds
        self.countdown.text = str(self.seconds)
