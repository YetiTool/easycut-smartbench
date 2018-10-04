import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image


class PopupAlarm(Widget):


    def __init__(self, machine, screen_manager, message):
        
        alarm_description = ALARM_CODES.get(message, "")
        
        img = Image(size_hint_y=2, source="./asmcnc/skavaUI/img/popup_alarm_visual.png", allow_stretch=True)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=alarm_description)
        continue_button = Button(text='Continue...')
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(continue_button)
        
        popup = Popup(title='Stop! Something has gone wrong...',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 400),
                      auto_dismiss= False)
        
        continue_button.bind(on_release=popup.dismiss)
        popup.open()


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