import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image


class PopupStop(Widget):


    def __init__(self, machine, screen_manager):
        
        self.m = machine
        self.sm = screen_manager
        
        self.m.stop_for_a_stream_pause()
        
        stop_description = "Is everything OK? You can resume the job, or cancel it completely."
        
        img = Image(size_hint_y=2, source="./asmcnc/skavaUI/img/popup_stop_visual.png", allow_stretch=True)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=stop_description)
        resume_button = Button(text='Resume')
        cancel_button = Button(text='Cancel')
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, padding=0)
        btn_layout.add_widget(resume_button)
        btn_layout.add_widget(cancel_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='You pressed the stop button...',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 400),
                      auto_dismiss= False)
        
        cancel_button.bind(on_press=self.machine_reset)
        cancel_button.bind(on_press=popup.dismiss)
        resume_button.bind(on_press=self.machine_resume)
        resume_button.bind(on_press=popup.dismiss)
        
        popup.open()

    
    def machine_reset(self, *args):
        
        self.m.s.is_job_streaming = True # WARNING: This line makes no sense :-) but needed to reset_the_go_screen? Refactor!
        self.m.stop_from_soft_stop_cancel()


    def machine_resume(self, *args):
        self.m.resume_after_a_stream_pause()

