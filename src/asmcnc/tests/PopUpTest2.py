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

<ConfirmPopup>:
    cols:1
    Label:
        text_size: self.size
        halign: 'center'
        valign: 'middle'
        text: root.text
    GridLayout:
        cols: 4
        size_hint_y: None
        height: '44sp'
        Button:
            text: 'Yes'
            on_release: root.dispatch('on_answer','yes')
        Button:
            text: 'No'
            on_release: root.dispatch('on_answer', 'no')
#         Button:
#             text: '1'
#             on_release: root.push_1()
#         Button:
#             text: '2'
#             on_release: root.push_2()

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

class ConfirmPopup(GridLayout):
    text = StringProperty()
    
    def __init__(self,**kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup,self).__init__(**kwargs)
        
    def on_answer(self, *args):
        print 'Answered'

    

class PopTest(Screen):

    other = "poo"

    def __init__(self, **kwargs):
        super(PopTest, self).__init__(**kwargs)
        
    def make_pop(self):
        content = ConfirmPopup(text='Do You Love Kivy?')
        content.bind(on_answer=self._on_answer)

        self.popup = Popup(title="Answer Question",
                            content=content,
                            size_hint=(None, None),
                            size=(480,400),
                            auto_dismiss= False
                            )
        self.popup.open()
    
    def _on_answer(self, instance, answer):
        print "USER ANSWER: " , repr(answer)
        self.popup.dismiss()



runTouchApp(PopTest())