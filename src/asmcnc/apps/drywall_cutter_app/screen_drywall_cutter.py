from kivy.clock import Clock
import sys, os

from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
import serial
import time
import numpy as np
from asmcnc.skavaUI import widget_status_bar
from asmcnc.comms.coordinate_system import CoordinateSystem as cs
import threading

Builder.load_string("""
<DrywallCutterScreen>:
    status_container:status_container
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            Button:
                on_press: root.start_test()
                text: "Start Test"
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
        self.z_vals = []

        self.m.s.bind(m_state=lambda i, value: self.on_state_change(value))

        self.test_running = False

        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

        self.setup_serial()


        # dti_thread = threading.Thread(target=self.setup_serial)
        # dti_thread.daemon = True
        # dti_thread.start()

        reading_thread = threading.Thread(target=self.get_reading)
        reading_thread.daemon = True
        reading_thread.start()

    def setup_serial(self):
        self.PORT = 'COM14'
        self.ser = serial.Serial(self.PORT, 9600, timeout=5)
        time.sleep(1)
        self.ser.flushInput()

    def on_state_change(self, value):
        if self.test_running and value.lower() == 'idle':
            self.z_vals.append(self.get_reading())
            print(self.z_vals)


    def start_test(self):
        self.test_running = True
        with open('probing_gcode.gcode') as gcode_file:
            gcode = gcode_file.readlines()

        self.m.s.run_skeleton_buffer_stuffer(gcode)
        
  
    def get_reading(self):
        try:
            while True:
                raw_reading = self.ser.read_until(b'\r', 20)
                reading = float(raw_reading[3:])
                reading /= 1000.0
                print(reading)
                return reading
        except Exception as e:
            print(e)

    def exit(self):
        self.sm.current = "lobby"