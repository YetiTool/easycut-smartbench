import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image


class PopupResetOffset(Widget):

    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        description = "You are resetting the laser datum offset. Please confirm that this is where you have made a reference mark with the spindle."
        
        img = Image(size_hint_y=2, source="./asmcnc/skavaUI/img/popup_stop_visual.png", allow_stretch=True)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description)
        resume_button = Button(text='Resume')
        cancel_button = Button(text='Cancel')
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, padding=0)
        btn_layout.add_widget(resume_button)
        btn_layout.add_widget(cancel_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Reset laser datum offset',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 400),
                      auto_dismiss= False)
        
        cancel_button.bind(on_press=popup.dismiss)
        resume_button.bind(on_press=self.reset_laser_datum_offset)
        resume_button.bind(on_press=popup.dismiss)
        
        popup.open()

    def reset_laser_datum_offset(self, *args):
        self.sm.get_screen('maintenance').laser_datum_buttons_widget.reset_laser_offset()

