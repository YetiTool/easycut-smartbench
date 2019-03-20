############################################################
# Investigation into loop Hz and CPU resources when on/off #
############################################################

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

###########
# LESSONS #
###########

# On PC:
# To achieve 2.5-4 kHz loop , low intensity processor use:
# set kivy_clock = default 
# maxfps = 10000
# interval dt = 0.00001

# To achieve 20 kHz loop on PC, high intensity processor use:
# set kivy_clock = interrupt 
# maxfps = 10000
# interval dt = 0.0001

# On Pi:
# To achieve 3.1kHz @ 100% CPU, during loop, but then drop back to 12% idle when no loop
# set kivy_clock = interrupt 
# maxfps = 60
# interval dt = 0.0001



# not tested on pi

Builder.load_string("""

<ClockArgTest>:
    
    button:button
    
    FloatLayout:

        Button:
            id: button
            text: 'Toggle count run'
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
    run_count = False

    def __init__(self, **kwargs):
        super(ClockArgTest, self).__init__(**kwargs)
        Clock.schedule_interval(self.show_count, 1)


    def change_text(self, local_variable, class_var, *largs):
        self.count += 1
        if self.run_count:
            Clock.schedule_once(partial(self.change_text, 'cat', self.class_variable), 0.00001) #unnecessary sending of object, just to demonstrate loop

    def show_count(self, dt):
        print ("Total: ", self.count, "Hz:",  str(self.count - self.last_count))
        self.last_count = self.count

    def toggle_text_on_button(self):
        self.run_count = not self.run_count
        if self.run_count:
            Clock.schedule_once(partial(self.change_text, 'cat', self.class_variable), 1)


runTouchApp(ClockArgTest())