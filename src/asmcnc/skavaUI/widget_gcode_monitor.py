# -*- coding: utf-8 -*-
'''
Created on 1 Feb 2018
@author: Ed
'''

from kivy.lang import Builder
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from asmcnc.skavaUI import popup_info

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
    scroll_y:1

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
        font_size: '12sp'
        text: root.text
        max_lines: 3

<GCodeMonitor>
    
    consoleScrollText:consoleScrollText
    consoleStatusText:consoleStatusText
    gCodeInput:gCodeInput

    enter_button: enter_button
    hide_ok_button: hide_ok_button
    settings_button: settings_button
    params_button: params_button
    state_button: state_button
    build_button: build_button
    check_button: check_button
    help_button: help_button
    clear_button: clear_button
    status_label: status_label
    
    BoxLayout: 
        size: self.parent.size
        pos: self.parent.pos
        orientation: "vertical"
        padding: 5
        spacing: 5
        
        canvas:
            Color:
                rgba: 0,0,0,0.2
            Rectangle:
                size: self.size
                pos: self.pos            

        BoxLayout:      
            size: self.parent.size
            pos: self.parent.pos      
            spacing: 5
            orientation: "horizontal"    
            
            BoxLayout:
                padding_horizontal: 5
                spacing: 5
                orientation: "vertical"
                size_hint_x: 0.9
                
                BoxLayout:
                    padding: 0
                    spacing: 2
                    orientation: 'horizontal'
                    size_hint_y: 0.1
     
                    TextInput:                      
                        id:gCodeInput
                        multiline: False
                        text: ''
                        on_text_validate: root.send_gcode_textinput()
                    
                    Button:
                        id: enter_button
                        text: "Enter"
                        on_press: root.send_gcode_textinput()
                        size_hint_x:0.3
                        background_color: .6, 1, 0.6, 1
      
                ScrollableLabelCommands:
                    size_hint_y: 0.8                     
                    id: consoleScrollText
                                         
            BoxLayout:
                padding_horizontal: 5
                spacing: 5
                orientation: "vertical"
                size_hint_x: 0.24
        
                ToggleButton:
                    id: hide_ok_button
                    state: root.hide_received_ok
                    markup: True
                    text: 'Hide oks'
                    on_state: root.hide_received_ok = self.state               
                    size_hint_y:0.1

# FOR USER
                    
                Button:
                    id: settings_button
                    text: "Settings"
                    on_press: root.send_gcode_preset("$$")
                    size_hint_y:0.1
                Button:
                    id: params_button
                    text: "Params"
                    on_press: root.send_gcode_preset("$#")
                    size_hint_y:0.1
                Button:
                    id: state_button
                    text: "State"
                    on_press: root.send_gcode_preset("$G")
                    size_hint_y:0.1
                Button:
                    id: build_button
                    text: "Build"
                    size_hint_y:0.1
                    on_press: root.send_gcode_preset("$I")
                Button:
                    id: check_button
                    text: "Check $C"
                    on_press: root.toggle_check_mode()
                    size_hint_y:0.1
                Button:
                    id: help_button
                    text: "Help"
                    on_press: root.send_gcode_preset("$")
                    size_hint_y:0.1

######### END ############
 
                Button:
                    id: clear_button
                    text: "Clear"
                    on_press: root.clear_monitor()
                    size_hint_y:0.1
                    background_color: 1, .8, 0, 1
        
        BoxLayout:
            padding: 5
            spacing: 0
            orientation: 'horizontal'
            size_hint_y: 0.09
            
            canvas:
                Color:
                    rgba: 0,0,0,0.2
                Rectangle:
                    size: self.size
                    pos: self.pos
                    
                      
            Label:
                id: status_label
                text: 'Status'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                    
    
        ScrollableLabelStatus:
            size_hint_y: 0.2        
            id: consoleStatusText
               
         
""")

from kivy.clock import Clock

WIDGET_UPDATE_DELAY = 0.2
STATUS_UPDATE_DELAY = 0.4

class ScrollableLabelCommands(ScrollView):
    text = StringProperty('')
    
class ScrollableLabelStatus(ScrollView):
    text = StringProperty('')

class GCodeMonitor(Widget):

    hide_received_ok = StringProperty('down')
    hide_received_status = StringProperty('down')
    monitor_text_buffer = []
    status_report_buffer = []

    def __init__(self, **kwargs):
        self.m = kwargs.pop('machine')
        self.sm = kwargs.pop('screen_manager')
        self.l = kwargs.pop('localization')

        super(GCodeMonitor, self).__init__(**kwargs)

        Clock.schedule_interval(self.update_display_text, WIDGET_UPDATE_DELAY)      # Poll for status
        Clock.schedule_interval(self.update_status_text, STATUS_UPDATE_DELAY)      # Poll for status    
    
        self.popup_flag = True
        self.update_strings()
    
    def update_monitor_text_buffer(self, input_or_output, content):

        # Try to chuck out any problem strings
        if isinstance(content, str):
            
            # Don't update if content is to be hidden
            if content.startswith('<') and self.hide_received_status == 'down':
                self.status_report_buffer.append(content)
                return
            if content == 'ok' and self.hide_received_ok == 'down': return

            # Update buffer with content
            if input_or_output == 'snd': self.monitor_text_buffer.append( '> ' + content)
            if input_or_output == 'rec': self.monitor_text_buffer.append(content)
            if input_or_output == 'debug': self.monitor_text_buffer.append(content)
        
    
    def update_display_text(self, dt):   

        self.consoleScrollText.text = '\n'.join(self.monitor_text_buffer)
        if len(self.monitor_text_buffer) > 61:
            del self.monitor_text_buffer[0:len(self.monitor_text_buffer)-60]

        
    def update_status_text(self, dt):
        # this needs fixing
        if self.m.state() == 'Alarm' and not any('Alarm' in s for s in self.status_report_buffer):
            self.status_report_buffer.append(self.l.get_str('Please reset for status update')) # this might work with RST can't be sure
        
        self.consoleStatusText.text = '\n'.join(self.status_report_buffer)
        if len(self.status_report_buffer) > 4:
            del self.status_report_buffer[0:len(self.status_report_buffer)-3]
        
    def send_gcode_textinput(self): 
        
        if self.popup_flag:
            description = (
                self.l.get_str("Sending commands directly to the machine can change how it operates.") + \
                "\n\n" + \
                self.l.get_str("Please exercise caution when using this feature.") + "\n\n"
                )

            popup_info.PopupWarning(self.sm, self.l, description)
            self.popup_flag = False
        else:
            if self.validate_gcode_textinput(self.gCodeInput.text):
                self.m.send_any_gcode_command(str(self.gCodeInput.text))
            else:
                message = (
                    self.l.get_str("This command is forbidden because it will alter the fundamental settings of the machine.") + \
                    "\n\n" + \
                    self.l.get_str("If you need to alter the fundamental settings of the machine please contact YetiTool support.")
                )
                popup_info.PopupWarning(self.sm, self.l, message)

    def validate_gcode_textinput(self, gcode_input):

        if "$50" in gcode_input:
            return False

        elif "$RST" in gcode_input:
            return False

        else: 
            return True
    
    def send_gcode_preset(self, gcode_input):
        
        self.m.send_any_gcode_command(gcode_input)
    
    def toggle_check_mode(self):
        
        if self.m.s.m_state == "Check":
            self.m.disable_check_mode()
        elif self.m.s.m_state == "Idle":
            self.m.enable_check_mode()
        else:
            self.update_monitor_text_buffer('debug', self.l.get_str('Could not enable check mode; please check machine is Idle.'))

    def clear_monitor(self): 
        
        self.monitor_text_buffer = [self.l.get_str('Welcome to the GCode console') + '...']


######### START/STOP DEBUG

    def send_grbl_reset(self):
        self.m._grbl_soft_reset()
        
    def send_grbl_door(self):    
        self.m._grbl_door()

    def send_grbl_resume(self):
        self.m._grbl_resume()

    def send_grbl_unlock(self):
        self.m._grbl_unlock()

    def send_led_red(self):
        self.m.set_led_red()

    def send_led_restore(self):
        self.m.led_restore()

## Localization
    def update_strings(self):
        self.enter_button.text = self.l.get_str('Enter')
        self.hide_ok_button.text = self.l.get_str('Hide oks')
        self.settings_button.text = self.l.get_str('Settings') 
        self.params_button.text = self.l.get_str('Params') 
        self.state_button.text = self.l.get_str('State') 
        self.build_button.text = self.l.get_str('Build')
        self.check_button.text = self.l.get_str('Check') + ' $C'
        self.help_button.text = self.l.get_str('Help')
        self.clear_button.text = self.l.get_str('Clear')
        self.status_label.text = self.l.get_str('Status')


