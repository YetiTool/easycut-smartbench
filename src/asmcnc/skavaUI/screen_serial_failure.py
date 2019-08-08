'''
Created on 19 Feb 2019

Screen to show user errors and exceptions that arise from serial being disconnected, or failing to read/write. Called in serial_connection.

Currently forces user to reboot, as I'm not sure how to get a successful re-establish of the connection otherwise.

@author: Letty
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget

import sys, os

# Kivy UI builder:
Builder.load_string("""

<SerialFailureClass>:

    reboot_button:reboot_button
    #reestablish_button:reestablish_button 

    canvas:
        Color: 
            rgba: hex('#616161')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 60
        spacing: 30
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            spacing: 20
             
            Label:
                size_hint_y: 0.8
                text_size: self.size
                font_size: '24sp'
                text: '[b]SERIAL CONNECTION ERROR[/b]\\nThere\\'s a problem communicating with Smartbench'
                markup: True
                halign: 'left'
                vallign: 'top'
 
            BoxLayout:
                orientation: 'horizontal'
                padding: 30
                Label:
                    size_hint_y: 1.1
                    text_size: self.size
                    font_size: '18sp'
                    halign: 'left'
                    valign: 'middle'
                    text: root.error_description 
                
            Label:
                size_hint_y: 1
                font_size: '19sp'
                text_size: self.size
                halign: 'left'
                valign: 'top'
                text: root.user_instruction
                
#             BoxLayout:
#                 orientation: 'vertical'
#                 size_hint_x: 1
#                 spacing: 5
                    
            BoxLayout:
                orientation: 'horizontal'
                padding: 200, 0
                spacing: 40
            
#                     Button:
#                         size_hint_y:0.9
#                         id: reestablish_button
#                         size: self.texture_size
#                         valign: 'top'
#                         halign: 'center'
#                         disabled: False
#                         on_release:
#                             root.reestablish_button_press()
#                             
#                         BoxLayout:
#                             padding: 5
#                             size: self.parent.size
#                             pos: self.parent.pos
#                             
#                             Label:
#                                 #size_hint_y: 1
#                                 text_size: self.size
#                                 valign: 'middle'
#                                 halign: 'center'
#                                 font_size: '16sp'
#                                 text: 'Try to re-establish serial connection'
                        
                Button:
                    size_hint_y: 0.9
                    size_hint_x: 0.3
                    id: reboot_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    on_release:
                        root.reboot_button_press()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            valign: 'middle'
                            halign: 'center'
                            text_size: self.size
                            font_size: '25sp'
                            text: 'Reboot EasyCut'
#                 BoxLayout:
#                     orientation: 'horizontal'
#                     padding: 50, 0
#                     spacing: 40
#                 
#                     Button:
#                         size_hint_y:0.9
#                         id: home_button
#                         size: self.texture_size
#                         valign: 'top'
#                         halign: 'center'
#                         disabled: False
#                         on_release:
#                             root.quit_to_home()
#                             
#                         BoxLayout:
#                             padding: 5
#                             size: self.parent.size
#                             pos: self.parent.pos
#                             
#                             Label:
#                                 #size_hint_y: 1
#                                 text_size: self.size
#                                 valign: 'middle'
#                                 halign: 'center'
#                                 font_size: '20sp'
#                                 text: 'Return to home'
#                             
#                     Button:
#                         size_hint_y:0.9
#                         id: go_screen_button
#                         size: self.texture_size
#                         valign: 'top'
#                         halign: 'center'
#                         disabled: False
#                         on_release:
#                             root.return_to_go_screen()
#                             
#                         BoxLayout:
#                             padding: 5
#                             size: self.parent.size
#                             pos: self.parent.pos
#                             
#                             Label:
#                                 #size_hint_y: 1
#                                 valign: 'middle'
#                                 halign: 'center'
#                                 text_size: self.size
#                                 font_size: '20sp'
#                                 text: 'Return to Go Screen'
 
            
""")

class SerialFailureClass(Screen):

    # define error description to make kivy happy
    error_description = StringProperty()
    message = StringProperty()
    button_text = StringProperty()
    reboot_button = ObjectProperty()
    user_instruction = StringProperty()
    button_function = StringProperty()
    
    def __init__(self, **kwargs):
        super(SerialFailureClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']  
#         self.port=kwargs['win_port']

    def on_enter(self):
        # use the message to get the error description        
        #self.error_description = ERROR_CODES.get(self.message, "")
        
        if self.m.s.is_job_streaming == True and self.sm.get_screen('go').paused == False:
            self.sm.get_screen('go').pause_job()
            
        self.user_instruction = 'Please check that Z head is connected.\n' \
        'If connection with SmartBench has been interrupted, the machine may also need to be restarted.'
    
    def reboot_button_press(self):
        self.sm.current = 'rebooting'
            
#     def reestablish_button_press(self):
#         self.m.s.establish_connection(self.port)
#         self.m.s.initialise_grbl()
        
    def return_to_go_screen(self):
        self.sm.current = 'go'
        
    def quit_to_home(self):
        self.sm.current = 'home' 
        
