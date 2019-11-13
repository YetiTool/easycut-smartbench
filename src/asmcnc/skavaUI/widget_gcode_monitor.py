'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, StringProperty # @UnresolvedImport


Builder.load_string("""

<ScrollableLabelCommands>:
    scroll_y:0

    canvas.before:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: self.size
            pos: self.pos
    
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
        max_lines: 60
        
<ScrollableLabelStatus>:
    scroll_y:0

    canvas.before:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: self.size
            pos: self.pos
    
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
        max_lines: 60

<GCodeMonitor>
    
    consoleScrollText:consoleScrollText
    consoleStatusText:consoleStatusText
    gCodeInput:gCodeInput
    
    BoxLayout:
    
        size: self.parent.size
        pos: self.parent.pos      
        padding: 5
        spacing: 5
        orientation: "horizontal" 
        canvas:
            Color:
                rgba: 0,0,0,0.2
            Rectangle:
                size: self.size
                pos: self.pos


        
        BoxLayout:
            padding: 0
            spacing: 5
            orientation: "vertical"
            size_hint_x: 0.9
 
            TextInput:
                size_hint_y: 0.1                        
                id:gCodeInput
                multiline: False
                text: ''
                on_text_validate: root.send_gcode_textinput()
 
            BoxLayout:
                padding: 5
                spacing: 5
                orientation: 'horizontal'
                size_hint_y: 0.1
 
                canvas:
                    Color:
                        rgba: 0,0,0,0.2
                    Rectangle:
                        size: self.size
                        pos: self.pos
                Label:
                    text: 'Hide'
                ToggleButton:
                    state: root.hide_received_ok
                    text: 'oks'
                    on_state: root.hide_received_ok = self.state                              
                ToggleButton:
                    state: root.hide_received_status
                    on_state: root.hide_received_status = self.state
                    text: 'state'
 
            ScrollableLabelCommands:
                size_hint_y: 0.7                       
                id: consoleScrollText
            
            BoxLayout:
                padding: 5
                spacing: 5
                orientation: 'horizontal'
                size_hint_y: 0.1
 
                canvas:
                    Color:
                        rgba: 0,0,0,0.2
                    Rectangle:
                        size: self.size
                        pos: self.pos
            
                Label:
                    text: 'Status'
                    text_size: self.size
                    halign: 'left'
                    valign: 'bottom'
                    
            ScrollableLabelStatus:
                size_hint_y: 0.3                  
                id: consoleStatusText
 
        BoxLayout:
            padding: 0
            spacing: 5
            orientation: "vertical"
            size_hint_x: 0.17
 
            Button:
                text: "Enter"
                on_press: root.send_gcode_textinput()
                size_hint_y:0.1
                background_color: .6, 1, 0.6, 1
            Button:
                text: "Settings"
                on_press: root.send_gcode_preset("$$")
                size_hint_y:0.1
            Button:
                text: "Params"
                on_press: root.send_gcode_preset("$#")
                size_hint_y:0.1
            Button:
                text: "State"
                on_press: root.send_gcode_preset("$G")
                size_hint_y:0.1
            Button:
                text: "Build"
                size_hint_y:0.1
                on_press: root.send_gcode_preset("$I")
            Button:
                text: "StartUp"
                on_press: root.send_gcode_preset("$N")
                size_hint_y:0.1
            Button:
                text: "Check $C"
                on_press: root.toggle_check_mode()
                size_hint_y:0.1
            Button:
                text: "Help"
                on_press: root.send_gcode_preset("$")
                size_hint_y:0.1
            Button:
                text: "Clear"
                on_press: root.clear_monitor()
                size_hint_y:0.1
                background_color: 1, .8, 0, 1                        
         
""")

from kivy.clock import Clock

WIDGET_UPDATE_DELAY = 0.2
STATUS_UPDATE_DELAY = 0.3

class ScrollableLabelCommands(ScrollView):
    text = StringProperty('')
    
class ScrollableLabelStatus(ScrollView):
    text = StringProperty('')
    

class GCodeMonitor(Widget):

    hide_received_ok = StringProperty('down')
    hide_received_status = StringProperty('down')
    monitor_text_buffer = 'Welcome to the GCode console...\n'
    status_report_buffer = 'Welcome to the GCode console...\n'

    
    def __init__(self, **kwargs):
    
        super(GCodeMonitor, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        Clock.schedule_interval(self.update_display_text, WIDGET_UPDATE_DELAY)      # Poll for status
        Clock.schedule_interval(self.update_status_text, STATUS_UPDATE_DELAY)      # Poll for status    
    
    def update_monitor_text_buffer(self, input_or_output, content):
        
        # Don't update if content is to be hidden
        if content.startswith('<') and self.hide_received_status == 'down': 
            self.status_report_buffer += content + '\n'
            return
        if content == 'ok' and self.hide_received_ok == 'down': return
        
        # Update buffer with content
        if input_or_output == 'snd': self.monitor_text_buffer += '> ' + content + '\n'
        if input_or_output == 'rec': self.monitor_text_buffer += content + '\n'
        if input_or_output == 'debug': self.monitor_text_buffer += content + '\n'
            
    
    def update_display_text(self, dt):   
        
        self.consoleScrollText.text = self.monitor_text_buffer
        
    def update_status_text(self, dt):
        
        self.consoleStatusText.text = self.status_report_buffer
        
    def send_gcode_textinput(self): 
        
        self.m.send_any_gcode_command(str(self.gCodeInput.text))
    

    def send_gcode_preset(self, input):
        
        self.m.send_any_gcode_command(input)
    
    def toggle_check_mode(self):
        
        if self.m.is_check_mode_enabled:
            self.m.disable_check_mode()
        else:
            self.m.enable_check_mode()

    def clear_monitor(self): 
        
        self.monitor_text_buffer = ""


 