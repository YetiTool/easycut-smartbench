from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation


from functools import partial


Builder.load_string("""

<PopTest>:
    
    button:button
    

    Button:
        id: button
        text: 'pop'
        size_hint: None, None            
        height: 200
        width: 200
        center: self.parent.center
        on_release: root.make_pop()

    Button:
        text: 'stop'
        size_hint: None, None            
        height: 200
        width: 200
        on_release: root.make_stop()

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
        
        print 'start'
        anim = Animation(height=180, width=180, t='in_out_sine', center=self.parent.center) + Animation(height=200, width=200, t='in_out_sine',center=self.parent.center)
        anim.repeat = True
        anim.start(self.button)


    def make_stop(self):
        
        print 'stop'
        Animation.stop_all(self.button)



runTouchApp(PopTest())