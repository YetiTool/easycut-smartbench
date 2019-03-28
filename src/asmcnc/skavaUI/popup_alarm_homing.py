import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
# from asmcnc.comms import serial_connection
# from asmcnc.comms.serial_connection import SerialConnection
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.widget import Widget


Builder.load_string('''
<ConfirmPopupAlarmHome>:
    
    orientation: 'vertical'
    padding: 20
    spacing: 20
    Image:
        size_hint_y: 2
        source: "./asmcnc/skavaUI/img/popup_alarm_visual.png"
        allow_stretch: True    
    Label:
        size_hint_y: 1
        text_size: self.size
        halign: 'center'
        valign: 'middle'
        text: root.text
    GridLayout:
        cols: 2
        size_hint_y: 1
        Button:
            text: 'Re-home'
            on_release: root.dispatch('on_answer','rehome')
        Button:
            text: 'Cancel'
            on_release: root.dispatch('on_answer', 'cancel')
''')


class ConfirmPopupAlarmHome(BoxLayout):
    text = StringProperty()
    
    def __init__(self,**kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopupAlarmHome,self).__init__(**kwargs)
        
    def on_answer(self, *args):
        pass    
   

class PopupAlarmHome(Widget):


    def __init__(self, machine, screen_manager, message):
        self.m = machine
        self.sm = screen_manager
        self.alarm_message = message
        self.alarm_description = ALARM_CODES.get(self.alarm_message, "")
        content = ConfirmPopupAlarmHome(text=self.alarm_description)
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title="Homing Alarm",
                            content=content,
                            size_hint=(None, None),
                            size=(640,384),
                            auto_dismiss= False)
        self.popup.open()
        
    def _on_answer(self, instance, answer):
        print "USER ANSWER: " , repr(answer)
        if answer == 'rehome':
            self.m.home_all()
            self.sm.current = 'homing'
        if answer == 'cancel':
            self.m.unlock_after_alarm()        
        self.popup.dismiss()


ALARM_CODES = {

    "ALARM:1" : "Hard limit triggered. Machine position is likely lost due to sudden and immediate halt. Re-homing is highly recommended.",
    "ALARM:2" : "G-code motion target exceeds machine travel. Machine position safely retained. Alarm may be unlocked.",
    "ALARM:3" : "Reset while in motion. Grbl cannot guarantee position. Lost steps are likely. Re-homing is highly recommended.",
    "ALARM:4" : "Probe fail. The probe is not in the expected initial grbl_state before starting probe cycle, where G38.2 and G38.3 is not triggered and G38.4 and G38.5 is triggered.",
    "ALARM:5" : "Probe fail. Probe did not contact the workpiece within the programmed travel for G38.2 and G38.4.",
    "ALARM:6" : "Homing fail. Reset during active homing cycle.",
    "ALARM:7" : "Homing fail. Safety door was opened during active homing cycle.",
    "ALARM:8" : "Homing fail. Cycle failed to clear limit switch when pulling off. Try increasing pull-off setting or check wiring.",
    "ALARM:9" : "Homing fail. Could not find limit switch within search distance. Defined as 1.5 * max_travel on search and 5 * pulloff on locate phases.",

}