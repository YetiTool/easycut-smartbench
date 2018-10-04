from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

from functools import partial


Builder.load_string("""

<PopTest>:
    
    button:button
    
    FloatLayout:

        Button:
            id: button
            text: 'pop'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: None, None            
            height: 200
            width: 200
            on_release: root.make_pop()

""")


from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.label import Label
from kivy.uix.button import  Button

class PopTest(Screen):

    other = "poo"

    def __init__(self, **kwargs):
        super(PopTest, self).__init__(**kwargs)
        
    def make_pop(self):


        box = BoxLayout()
        box.add_widget(Label(text='Hello world'))
        box.add_widget(TextInput(text='Hi'))
        btn1 = Button(text='Close me!')
        box.add_widget(btn1)
        
        popup = Popup(title='Test popup',
                      content=box,
                      size_hint=(None, None),
                      size=(400, 400),
                      auto_dismiss= False)
        
        btn1.bind(on_release=popup.dismiss)

        popup.open()

    
    def _on_answer(self, instance, answer):
        print "USER ANSWER: " , repr(answer)
        self.popup.dismiss()



runTouchApp(PopTest())