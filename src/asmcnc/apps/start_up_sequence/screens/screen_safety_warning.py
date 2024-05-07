# -*- coding: utf-8 -*-
"""
Created on 30 March 2019

Screen to give a safety warning to the user when they switch on SmartBench.

@author: Letty
"""
from datetime import datetime

from kivy.app import App

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.core_UI.new_popups import software_crashed_popup
from asmcnc.skavaUI import widget_status_bar

Builder.load_string(
    """

<SafetyScreen>:

    status_container:status_container

    header_label : header_label
    confirm_button : confirm_button

    label_r1_c1 : label_r1_c1
    label_r2_c1 : label_r2_c1
    label_r3_c1 : label_r3_c1
    label_r4_c1 : label_r4_c1 
    label_r1_c2 : label_r1_c2
    label_r2_c2 : label_r2_c2
    label_r3_c2 : label_r3_c2
    label_r4_c2 : label_r4_c2 


    canvas:
        Color:
            rgba: hex('#E5E5E5FF')
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
    
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos  
                
        BoxLayout:
            size_hint_y: 0.9
            orientation: 'vertical'
            padding:[dp(0.05)*app.width, dp(0.0833333333333)*app.height, dp(0.05)*app.width, dp(0.0416666666667)*app.height]
            size: self.parent.size
            pos: self.parent.pos
      
            BoxLayout:
                size_hint_y: .7
    
                orientation: 'vertical'
                size: self.parent.size
                pos: self.parent.pos
            
                Label:
                    id: header_label
                    text: '[color=333333][b]Safety Warning[/b][/color]'
                    markup: True
                    font_size: str(0.03625*app.width) + 'sp' 
                    valign: 'middle'
                    halign: 'center'
                    size:self.texture_size
                    text_size: self.size
                    color: hex('#333333ff')
                
            BoxLayout:
                size_hint_y: 4.1
    
                padding:[dp(0.01875)*app.width, 0]
                orientation: 'vertical'
                BoxLayout:
                    orientation: 'horizontal'    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r1_c1
                            size_hint_x: 6
                            halign: 'left'
                            text: '[color=333333]Improper use of SmartBench can cause serious injury[/color]'
                            markup: True
                            size:self.size
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
                            
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r1_c2
                            size_hint_x: 6
                            text: '[color=333333]Always wear ear defenders, eye protection and a dust mask[/color]'
                            markup: True    
                            halign: 'left' 
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
        
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r2_c1
                            size_hint_x: 6
                            text: '[color=333333]Risk of injury from rotating tools and axis motion[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r2_c2
                            size_hint_x: 6
                            text: '[color=333333]Never put hands into moving machinery[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
    
                            
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r3_c1
                            size_hint_x: 6
                            text: '[color=333333]Danger to life by magnetic fields - do not use near a pacemaker[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r3_c2
                            size_hint_x: 6
                            text: '[color=333333]Ensure the machine is powered from an earthed supply[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'
                            color: hex('#333333ff')

                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r4_c1
                            size_hint_x: 6
                            text: '[color=333333]Never leave the machine unattended while power is on[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.025*app.width
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: label_r4_c2
                            size_hint_x: 6
                            text: '[color=333333]Ensure all plugs are fully inserted and secured[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'
                            color: hex('#333333ff')
  

            BoxLayout:
                size_hint_y: 1.2
                orientation: 'horizontal'

                Button:
                    id: confirm_button
                    width: dp(0.875*app.width)
                    height: dp(0.1875*app.height)
                    on_press: root.next_screen()
                    markup: True
                    font_size: str(0.03*app.width) + 'sp'
                    text_size: self.size
                    valign: "middle"
                    halign: "center"
                    background_normal: "./asmcnc/skavaUI/img/blank_long_button.png"
                    background_down: "./asmcnc/skavaUI/img/blank_long_button.png"
                    border: [dp(30.0/800)*app.width, dp(30.0/480)*app.height, dp(30.0/800)*app.width, dp(30.0/480)*app.height]
              

"""
)


class SafetyScreen(Screen):
    user_has_confirmed = False

    def __init__(self, **kwargs):
        super(SafetyScreen, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.status_bar_widget = widget_status_bar.StatusBar(
            machine=self.m, screen_manager=self.sm
        )
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = "#1976d2"
        self.update_strings()
        self.m.s.bind(setting_50=self.open_crash_popup)
        self.user_settings_manager = App.get_running_app().user_settings_manager

    def on_enter(self):
        Logger.info("Safety screen UP")

    def open_crash_popup(self, *args):
        if software_crashed_popup.check_for_crash() and self.m.sett.wifi_available:
            software_crashed_popup.SoftwareCrashedPopup(self.m.serial_number(), size_hint=(0.8, 0.8)).open()
        elif not self.m.sett.wifi_available:
            Logger.info("No wifi available, not opening crash popup and deleting crash file")
            software_crashed_popup.delete_crash_log()

    def next_screen(self):
        self.user_has_confirmed = True
        self.sm.current = "squaring_decision"

    def on_leave(self):
        self.start_seq.exit_sequence(self.user_has_confirmed)

    def update_strings(self):
        self.header_label.text = self.l.get_str("Safety Warning")
        self.label_r1_c1.text = self.l.get_str(
            "Improper use of SmartBench can cause serious injury"
        )
        self.label_r2_c1.text = self.l.get_str(
            "Always wear ear defenders, eye protection and a dust mask"
        )
        self.label_r3_c1.text = self.l.get_str(
            "Risk of injury from rotating tools and axis motion"
        )
        self.label_r4_c1.text = self.l.get_str("Never put hands into moving machinery")
        self.label_r1_c2.text = self.l.get_str(
            "Danger to life by magnetic fields - do not use near a pacemaker"
        )
        self.label_r2_c2.text = self.l.get_str(
            "Ensure the machine is powered from an earthed supply"
        )
        self.label_r3_c2.text = self.l.get_str(
            "Never leave the machine unattended while power is on"
        )
        self.label_r4_c2.text = self.l.get_str(
            "Ensure all plugs are fully inserted and secured"
        )
        self.confirm_button.text = self.l.get_str(
            "I have read and understood the instruction manual"
        )
