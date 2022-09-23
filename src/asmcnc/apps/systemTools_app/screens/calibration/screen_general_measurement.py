from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.skavaUI import popup_info

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

Builder.load_string("""
<GeneralMeasurementScreen>:

    load_graph:load_graph

    BoxLayout: 
        orientation: "horizontal"

        Image:
            id: load_graph
            size_hint: None, None
            height: dp(355)
            width: dp(700)
            x: dp(5)
            y: dp(5)
            allow_stretch: True
            opacity: 0

        BoxLayout: 
            orientation: "vertical"
            size_hint_x: None
            width: dp(100)
            
            GridLayout: 
                size_hint_y: None
                height: dp(100)
                cols: 2

                Button:
                    text: "BACK"
                    on_press: root.back_to_fac_settings()

                Button:
                    text: "Start"
                    on_press: root.start_measurment()

                Button:
                    text: "Stop"
                    on_press: root.stop_measurement()

                Button:
                    text: "Clear"
                    on_press: root.clear_measurement()

            GridLayout: 
                cols: 2

                Label:
                    text: "x axis"

                Label:
                    text: "y axis"

                Button:
                    text: "t"
                    on_press: root.set_index("Y", self)

                Button:
                    text: "SG X"
                    on_press: root.set_index("X", self)

                Button:
                    text: "F"
                    on_press: root.set_index("Y", self)

                Button:
                    text: "SG Y"
                    on_press: root.set_index("X", self)

                Button:
                    text: "x pos"
                    on_press: root.set_index("Y", self)

                Button:
                    text: "SG Z"
                    on_press: root.set_index("X", self)

                Button:
                    text: "y pos"
                    on_press: root.set_index("Y", self)

                Button:
                    text: "SG Y1"
                    on_press: root.set_index("X", self)

                Button:
                    text: "z pos"
                    on_press: root.set_index("Y", self)

                Button:
                    text: "SG Y2"
                    on_press: root.set_index("X", self)

            Button:
                size_hint_y: None
                height: dp(40)
                text: "PLOT"
                on_press: root.display_results()

""")

class GeneralMeasurementScreen(Screen):

    x_idx = 0
    y_idx = 0


    descriptors = {

        1: "x pos",
        2: "y pos",
        3: "z pos",
        4: "SG X",
        5: "SG Y",
        6: "SG Y1",
        7: "SG Y2",
        8: "SG Z",
        12: "t",
        13: "F"
    }

    def __init__(self, **kwargs):
        super(GeneralMeasurementScreen, self).__init__(**kwargs)

        self.systemtools_sm = kwargs['systemtools']
        self.m=kwargs['machine']

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def start_measurment(self):
        self.m.start_measuring_running_data('999')

    def stop_measurement(self):
        self.m.stop_measuring_running_data()

    def clear_measurement(self):
        self.m.clear_measured_running_data()

    def get_x_axis(self):
        new_list = [i[self.x_idx] for i in self.m.measured_running_data]
        return new_list

    def get_y_axis(self):
        new_list = [i[self.y_idx] for i in self.m.measured_running_data]
        return new_list

    def set_index(self, axis, label):
        value = [i for i in self.descriptors if self.descriptors[i]==label.text][0]
        if axis == "X": self.x_idx = value
        if axis == "Y": self.y_idx = value

    def display_results(self):
        plt.rcParams["figure.figsize"] = (7,3.55)
        plt.plot(self.get_x_axis(), self.get_y_axis(), 'b')
        plt.xlabel(self.descriptors[self.x_idx])
        plt.ylabel(self.descriptors[self.y_idx])
        plt.title(self.descriptors[self.x_idx] + "vs" + self.descriptors[self.y_idx])
        plt.tight_layout()
        plt.grid()
        plt.savefig('./asmcnc/production/z_head_mechanics_jig/z_head_mechanics_jig_graph.png')
        plt.close()
        self.load_graph.source = './asmcnc/production/z_head_mechanics_jig/z_head_mechanics_jig_graph.png'
        self.load_graph.reload()
        self.load_graph.opacity = 1