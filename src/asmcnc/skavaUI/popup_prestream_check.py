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


class PopupPrestream(Widget):

    def __init__(self, machine, screen_manager, message):
        
        self.m = machine
        self.sm = screen_manager
        
        img = Image(size_hint_y=2, source="./asmcnc/skavaUI/img/popup_prestream_check_visual.png", allow_stretch=True)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=message)
        resume_button = Button(text='Continue anyway')
        cancel_button = Button(text='Cancel')
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, padding=0)
        btn_layout.add_widget(resume_button)
        btn_layout.add_widget(cancel_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Before you start the job, we found an error...',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 400),
                      auto_dismiss= False)
        
        cancel_button.bind(on_release=self.cancel)
        cancel_button.bind(on_release=popup.dismiss)        
        resume_button.bind(on_release=self.carry_on)
        resume_button.bind(on_release=popup.dismiss)
        
        popup.open()
    
    def cancel(self, *args):
        pass
        
    def carry_on(self, *args):
        self.sm.current = 'go'

