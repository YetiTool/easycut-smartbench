##########################################################
# Investigation to loop Hz, internal vs. graphics update #
##########################################################

from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.clock import Clock

from functools import partial

from kivy.config import Config
# Config.set('graphics', 'maxfps', '10000')
# Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
# Config.write()

#################
# CLOCK LESSONS #
#################

# Clock configured in kivy's config.ini file
# WATCHOUT! The above "config.write <>" only takes effect after second running of the app.
# For dev, better therefore to edit the file direct... "C:\Users\Ed Sells\.kivy\config.ini"
# ... or <HOME_DIRECTORY>/.kivy/config.ini
# Type 'kivy_clock' MUST be set in the [kivy] section. Call in other locations will get ignored! Worth checking you're not looking at the wrong 'un.
# kivy_clock = default means that all scheduled events are limited by fps
# kivy_clock = interrupt means that scheduled events are NOT limited by fps... and so fast, but very hungry on processor resource
# ... UNLESS the event is coupled with a display event (e.g. updating a label) in which case it gets throttled to 60 fps, regardless of maxfps
# (assuming that the dt of the event is quicker than 60 fps e.g. 0.01)
# The realtionship between maxfps and real fps is kinda weird and needs investigating.


Builder.load_string("""

<ClockArgTest>:
    
    button:button
    
    FloatLayout:

        Button:
            id: button
            text: 'Toggle count display'
            pos_hint: {'center_x':0.5, 'center_y': .5}
            size_hint: None, None            
            height: 200
            width: 200
            on_press: root.toggle_text_on_button()

""")


class ClockArgTest(Screen):

    class_variable = "poo"
    count = 0
    last_count = 0
    show_text_on_button = False

    def __init__(self, **kwargs):
        super(ClockArgTest, self).__init__(**kwargs)
        Clock.schedule_once(partial(self.change_text, 'cat', self.class_variable), 1)
        Clock.schedule_interval(self.show_count, 1)

    def change_text(self, local_variable, class_var, *largs):
        if self.show_text_on_button:
            self.button.text = local_variable + " " + class_var + "\n" + str(self.count)
        self.count += 1
        Clock.schedule_once(partial(self.change_text, 'cat', self.class_variable), 0.00001) #unnecessary sending of object, just to demonstrate loop

    def show_count(self, dt):
        print ("Total: ", self.count, "Hz:",  str(self.count - self.last_count))
        self.last_count = self.count

    def toggle_text_on_button(self):
        self.show_text_on_button = not self.show_text_on_button

runTouchApp(ClockArgTest())