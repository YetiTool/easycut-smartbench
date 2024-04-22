from kivy.clock import Clock
import sys, os

from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
import serial
import time
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator
from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<DrywallCutterScreen>:
    status_container:status_container
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            Button:
                on_press: root.start_test()
                text: "Start Test"
            Image:
                id: graph
                source: "tabletop.png"
            Button:
                on_press: root.exit()
                text: "Exit"
        BoxLayout:
            size_hint_y: 0.08
            id: status_container
""")


class DrywallCutterScreen(Screen):


    def __init__(self, **kwargs):
        self.name = 'drywall_cutter'
        super(DrywallCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']
        self.jd = kwargs['job']
        self.pm = kwargs['popup_manager']
        self.cs = self.m.cs

        self.PORT = 'COM10'
        self.x_max = 1200
        self.y_max = 2400
        self.grid_points_x = 4
        self.grid_points_y = 5
        self.y_increment = self.y_max/self.grid_points_y
        self.x_increment = self.x_max/self.grid_points_x
        self.z_vals = []
        self.y_row = []
        self.x_range = np.arange(0, self.y_max, self.y_increment)
        self.y_range = np.arange(0, self.x_max, self.x_increment)
        self.ser = serial.Serial(self.PORT, 9600, timeout=5)

        self.m.s.bind(m_state=lambda i, value: self.on_state_change(value))

        self.test_running = False

        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

    def on_state_change(self, value):
        if self.test_running and value.lower() == 'dwell':
            self.z_vals.append(self.get_reading())

        if value == "idle":
            self.generate_graph()
            self.test_running = False
    def start_test(self):
        self.test_running = True
        with open('probing_gcode.gcode') as gcode_file:
            gcode = gcode_file.readlines()

        self.m.s.run_skeleton_buffer_stuffer(gcode)
        
    def get_reading(self):
        raw_reading = self.ser.read(20)
        reading = str(raw_reading)
        try:
            reading = float(str(reading[10:11]) + str(float(reading[13:21])/(1000)))
        except:
            reading = 0
        return reading

    def generate_graph(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        # Make data.
        X = self.x_range
        Y = self.y_range
        X, Y = np.meshgrid(X, Y)
        Z = self.z_vals

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.savefig('tabletop.png')
        self.graph.source = 'tabletop.png'  # Update displayed graph


    def exit(self):
        self.sm.current = "lobby"