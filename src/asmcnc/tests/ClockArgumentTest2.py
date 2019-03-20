##################################################
# Investigation into pure loop Hz using triggers #
##################################################

from kivy.config import Config
# Config.set('postproc', 'maxfps', '0')
# Config.set('graphics', 'maxfps', '0')
# Config.write()

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from kivy.app import runTouchApp
from kivy.uix.widget import Widget
from kivy.clock import Clock
from time import clock


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

    trigger = None
    t = clock()
    f = []
    last_t = t
    count = 0

    def __init__(self, **kwargs):
        super(ClockArgTest, self).__init__(**kwargs)
        print self.t
        self.f = []
        self.trigger = Clock.create_trigger(
            self.callback, timeout=0.001)
        self.trigger()

    def callback(self, *l):
        #print self.f
        t = clock()
        self.f.append(1 / (t - self.t))
        if t - self.last_t >= 1.0:
            print('fps', sum(self.f) / max(1, len(self.f)), len(self.f), t, self.last_t, self.count)
            self.f = []
            self.last_t = t 
        self.t = t
        self.count += 1
#         self.button.text = str(self.count)
        self.trigger()

runTouchApp(ClockArgTest())