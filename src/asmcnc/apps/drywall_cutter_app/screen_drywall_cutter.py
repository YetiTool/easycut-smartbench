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

Builder.load_string("""
<DrywallCutterScreen>:
    BoxLayout:
        Button:
            on_press: root.start_test
            text: "Start Test"
        Image:
            source: "tabletop.png"
        Button:
            on_press: root.exit
            text: "Exit"
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

        self.PORT = 'COM14'
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

        self.m.s.bind(m_state=lambda i, value: self.set_machine_state(value))

    def set_machine_state(self, value):
        self.machine_status = value.lower()

    def start_test(self):
        
        def get_reading():
            raw_reading = self.ser.read(20)
            reading = str(raw_reading)
            try:
                reading = float(str(reading[10:11]) + str(float(reading[13:21])/(1000)))
            except:
                reading = 0
            return reading

        for i in self.x_range:
            for n in self.y_range:
                while self.machine_status == 'jog':
                    pass
                self.m.jog_absolute_xy(n, i, 4000)
                while self.machine_status == 'jog':
                    pass
                self.m.jog_absolute_single_axis('z', -10, 300)  # move to Z measure
                while self.machine_status == 'jog':
                    pass
                time.sleep(0.5)
                self.y_row.append(get_reading())
                time.sleep(0.5)
                self.m.jog_absolute_single_axis('z', 10, 300)  # move to Z clearance
                while self.machine_status == 'jog':
                    pass
            self.z_vals.append(self.y_row)
            self.y_row = []  # clear list "y_row"

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

        # plt.show()
        plt.savefig('tabletop.png')


    def exit(self):
        self.sm.current = "lobby"