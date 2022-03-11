from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from asmcnc.tests.gauges.widget_gauge import Gauge

Builder.load_string("""
<GaugeScreen>:
    BoxLayout:
        orientation: 'vertical'

        size: self.parent.size
        pos: self.parent.pos    

""")

class GaugeScreen(Screen):
    def __init__(self, **kwargs):
        super(GaugeScreen, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.sm = kwargs['sm']

    def add_gauge(self, gauge):
        self.add_widget(gauge)
        self.start_overnight_test()
    
    # ddef jog_absolute_single_axis(self, axis, target, speed):
    def start_overnight_test(self):

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        Clock.schedule_once(self.stream_overnight_file, 5)

    def stream_overnight_file(self, dt):

        if self.m.state().startswith('Idle') and not self.overnight_running:

            self.overnight_running = True

            filename = './asmcnc/apps/systemTools_app/files/overnight_test.gc'
            # filename = './asmcnc/apps/systemTools_app/files/mini_run.gc'

            with open(filename) as f:
                overnight_gcode_pre_scrubbed = f.readlines()

            overnight_gcode = [self.m.quick_scrub(line) for line in overnight_gcode_pre_scrubbed]

            print("Running overnight test...")

            self.m.s.run_skeleton_buffer_stuffer(overnight_gcode)
            self.poll_end_of_overnight_file_stream = Clock.schedule_interval(self.post_overnight_file_stream, 60)

        else:
            Clock.schedule_once(self.stream_overnight_file, 3)