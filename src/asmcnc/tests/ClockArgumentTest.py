from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.clock import Clock

from functools import partial

# Set the Kivy "Clock" fps.
# Clock usually used to establish consistent framerate for animations
# Note that *app needs restarting* before config.write (fps value) takes effect
from kivy.config import Config
Config.set('graphics', 'maxfps', '30')
Config.write()

Builder.load_string("""

<ClockArgTest>:
    
    button:button
    
    FloatLayout:

        Button:
            id: button
            text: 'dog'
            pos_hint: {'center_x':0.5, 'center_y': .5}
            size_hint: None, None            
            height: 200
            width: 200

""")


class ClockArgTest(Screen):

    class_variable = "poo"
    count = 0

    def __init__(self, **kwargs):
        super(ClockArgTest, self).__init__(**kwargs)
        Clock.schedule_once(partial(self.change_text, 'cat', self.class_variable), 3)

    def change_text(self, local_variable, class_var, *largs):
        self.button.text = local_variable + " " + class_var + "\n" + str(self.count)
        self.count += 1
        Clock.schedule_once(partial(self.change_text, 'cat', self.class_variable), 0) #unnecessary sending of object, just to demonstrate loop


runTouchApp(ClockArgTest())