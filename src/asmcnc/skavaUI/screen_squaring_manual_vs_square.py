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

Builder.load_string("""

<SquaringScreenDecisionManualVsSquare>:

    header_label: header_label
    subtitle_label: subtitle_label
    no_button: no_button
    yes_button: yes_button

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

        # Cancel button
        BoxLayout:
            size_hint: (None,None)
            height: dp(20)
            padding: (20,0,20,0)
            spacing: 680
            orientation: 'horizontal'
            pos: self.parent.pos

            Label:
                text: ""

            Button:
                size_hint: (None,None)
                height: dp(50)
                width: dp(50)
                background_color: hex('#FFFFFF00')
                opacity: 1
                on_press: root.cancel()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/cancel_btn_decision_context.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        Label:
            size_hint_y: 0.1

        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            padding: (0,20,0,20)
            size_hint_y: 3
            

            Label:
                id: header_label
                size_hint_y: 1
                markup: True
                font_size: '30px' 
                valign: 'bottom'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
         
            Label:
                id: subtitle_label
                size_hint_y: 1
                markup: True
                font_size: '18px' 
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
     
        BoxLayout:
            orientation: 'horizontal'
            spacing: 30
            size_hint_y: 3

            Button:
                id: no_button
                size_hint_x: 1
                on_press: root.already_square()
                # text: 'No, I manually squared already'
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding: [20, 20]
                        
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
                id: yes_button
                size_hint_x: 1
                on_press: root.needs_auto_squaring()
                # text: "Yes, enable auto-square"
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding: [20, 20]
                        
        Label:
            size_hint_y: .5                

""")


class SquaringScreenDecisionManualVsSquare(Screen):
    
    
    cancel_to_screen = 'lobby'   
    return_to_screen = 'lobby'   
    
    default_font_size = '30sp'
    
    def __init__(self, **kwargs):
        
        super(SquaringScreenDecisionManualVsSquare, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
    
        self.update_strings()

    def on_enter(self):
        self.update_strings()
    
    def already_square(self):
        self.m.is_squaring_XY_needed_after_homing = False
        self.proceed_to_next_screen()


    def needs_auto_squaring(self):
        self.m.is_squaring_XY_needed_after_homing = True
        self.proceed_to_next_screen()


    def proceed_to_next_screen(self):
        self.sm.get_screen('prepare_to_home').cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen('prepare_to_home').return_to_screen = self.return_to_screen
        self.sm.current = 'prepare_to_home'


    def popup_help(self):
        
        info =  self.l.get_bold("Manual squaring") + "\n"  + \
                self.l.get_str("Before power up, the user manually pushes the X beam up against the bench legs at the home end.") + " " + \
                self.l.get_str("The power is then switched on.") + " " + \
                self.l.get_str("The motor coils lock the lower beam into position with a high degree of reliability.") + " " + \
                self.l.get_str("Thus, mechanical adjustments to square the beam can be repeated.") + "\n\n" + \
                self.l.get_bold("Auto squaring") + "\n" + \
                self.l.get_str("No special preparation from the user is needed.") + " " + \
                self.l.get_str("When homing, the lower beam automatically drives into the legs to square the X beam against the bench legs.") + " " + \
                self.l.get_str("The stalling procedure can offer a general squareness.") + " " + \
                self.l.get_str("But at the end of the movement, the motor coils can bounce into a different step position.") + " " + \
                self.l.get_str("Thus, mechanical adjustments to square the beam can be repeated less reliably than manual squaring.")

        popup_info.PopupInfo(self.sm, self.l, 720, info)


    def cancel(self):
        self.sm.current = self.cancel_to_screen

    def update_strings(self):
        self.header_label.text = self.l.get_str("Does SmartBench need to auto-square the XY?").replace(self.l.get_str('auto-square'), self.l.get_bold('auto-square'))
        self.subtitle_label.text = self.l.get_str("Click on the question mark to learn more about this.")
        self.no_button.text = self.l.get_str("No, I manually squared already")
        self.yes_button.text = self.l.get_str("Yes, enable auto-square")
