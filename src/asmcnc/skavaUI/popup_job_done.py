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


class PopupJobDone(Widget):

    def __init__(self, machine, screen_manager, message):
        
        img = Image(size_hint_y=2, source="./asmcnc/skavaUI/img/job_done.png", allow_stretch=True)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=message)
        continue_button = Button(text='Continue...')
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(continue_button)
        
        popup = Popup(title='Job done!',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 400),
                      auto_dismiss= False)
        
        continue_button.bind(on_release=popup.dismiss)
        popup.open()

