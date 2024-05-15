from kivy.core.window import Window

"""
Created on 19 Feb 2019

Screen to show user errors and exceptions that arise from serial being disconnected, or failing to read/write. Called in serial_connection.

Currently forces user to reboot, as I'm not sure how to get a successful re-establish of the connection otherwise.

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    ObjectProperty,
    StringProperty,
)

Builder.load_string(
    """

<SerialFailureClass>:

    title_string : title_string
    reboot_button : reboot_button
    reboot_string : reboot_string

    canvas:
        Color: 
            rgba: hex('#616161')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: app.get_scaled_tuple([50.0, 50.0])
        spacing: app.get_scaled_width(30.0)
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            spacing: app.get_scaled_width(20.0)
             
            Label:
                id: title_string
                size_hint_y: 1.2
                text_size: self.size
                font_size: app.get_scaled_sp('24.0sp')
                markup: True
                halign: 'left'
                vallign: 'top'
 
            BoxLayout:
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([20.0, 0, 0, 0])
                size_hint_y: 1
                Label:
                    text_size: self.size
                    font_size: app.get_scaled_sp('24.0sp')
                    halign: 'left'
                    valign: 'middle'
                    text: root.error_description 
                    markup: True

            Label:
                size_hint_y: 1
                font_size: app.get_scaled_sp('24.0sp')
                text_size: self.size
                halign: 'left'
                valign: 'top'
                text: root.user_instruction
                markup: True
                    
            BoxLayout:
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([200.0, 0])
                spacing: app.get_scaled_width(40.0)
                        
                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    size_hint_y: 0.9
                    size_hint_x: 0.3
                    id: reboot_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    on_press:
                        root.reboot_button_press()
                        
                    BoxLayout:
                        padding: app.get_scaled_tuple([5.0, 5.0])
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            id: reboot_string
                            valign: 'middle'
                            halign: 'center'
                            text_size: self.size
                            font_size: app.get_scaled_sp('30.0sp')
"""
)


class SerialFailureClass(Screen):
    error_description = StringProperty()
    reboot_button = ObjectProperty()
    user_instruction = StringProperty()

    def __init__(self, **kwargs):
        super(SerialFailureClass, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def on_enter(self):
        self.update_strings()

    def reboot_button_press(self):
        self.sm.current = "rebooting"

    def return_to_go_screen(self):
        self.sm.current = "go"

    def quit_to_home(self):
        self.sm.current = "home"

    def update_strings(self):
        self.title_string.text = (
            self.l.get_bold("SERIAL CONNECTION ERROR")
            + "\n"
            + self.l.get_str("There is a problem communicating with SmartBench.")
        )
        self.user_instruction = self.l.get_str(
            "Please check that Z head is connected, and then reboot the console."
        )
        self.reboot_string.text = self.l.get_str("Reboot")
        self.update_font_size(self.reboot_string)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length >= 20:
            value.font_size = str(0.03125 * Window.width) + "sp"
        else:
            value.font_size = str(0.0375 * Window.width) + "sp"
