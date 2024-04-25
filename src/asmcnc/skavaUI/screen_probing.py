# -*- coding: utf-8 -*-
"""
Created Feb 2024

@author: Benji
"""
import sys
from datetime import datetime

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


Builder.load_string("""
<ProbingScreen>:
    
    probing_label: probing_label

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding:[dp(0.05)*app.width, dp(0.0833333333333)*app.height]
        orientation: 'vertical'

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 1

        BoxLayout:
            orientation: 'horizontal'
            spacing:0.025*app.width
            size_hint_y: 1.5

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.probe_button_press()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_probe_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Label:
                id: probing_label
                size_hint_x: 1.1
                markup: True
                font_size: str(0.0375*app.width) + 'px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                        
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.stop_button_press()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/stop_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 1                

"""
) # Based on src/asmcnc/skavaUI/screen_homing_active.py


class ProbingScreen(Screen):
    parent_button = None

    def __init__(self, **kwargs):
        super(ProbingScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.fp = kwargs["fast_probe"]

        self.not_probing = False
        self.alarm_triggered = False

        self.variable_debug = False
        self.function_debug = False

    def update_text(self, string):
        self.probing_label.text = self.l.get_str(string) + "..."

    def on_enter(self):
        if self.function_debug:
            Logger.debug("**** on_enter called")
        if self.variable_debug:
            Clock.schedule_interval(lambda dt: self.debug_log(), 1)

        delay_time = [0]

        self.update_text("Please wait")

        if self.m.reason_for_machine_pause == "Resuming":
            # In this scenario, the user has hit resume after stop bar was pressed
            # Screen is not aware that the machine has resumed probing
            self.update_text("Probing")
            self.m.reason_for_machine_pause = None

        if self.m.is_spindle_on():
            # Spindle is on, need to turn it off
            Logger.warning("Spindle is on, turning off before probing")
            self.m.turn_off_spindle()
            delay_time.append(8)

        if self.m.state().lower() == "run" or self.m.state().lower() == "jog":
            # Machine is running, need to stop it
            Logger.warning("Machine is running, pausing before probing")
            self.m._grbl_feed_hold()
            Clock.schedule_once(lambda dt: self.m._grbl_soft_reset(), 3.5) # Wait before reseting to avoid alarm
            delay_time.append(4)

        # Probe once machine is ready
        self.probing_event =  Clock.schedule_once(lambda dt: self.probe(), max(delay_time))
        
        if not hasattr(self, "watchdog_event"):
            # Start watchdog 1 sec after probe requested to give machine time to respond before interigating
            Clock.schedule_once(lambda dt: self.watchdog_clock(), max(delay_time) + 1)
        elif not self.watchdog_event.is_triggered:
            # Watchdog not scheduled, schedule it in 1 sec
            Clock.schedule_once(lambda dt: self.watchdog_clock(), max(delay_time) + 1)

        if self.alarm_triggered:
            Logger.warning("Probing screen exited due to alarm")
            self.exit()

    def probe(self):
        if self.function_debug:
            Logger.debug("**** probing called")
        if self.m.state().lower() == "idle":
            self.m.probe_z(self.fp)
            self.update_text("Probing")
        else:
            Logger.error("Machine state is {}, not idle. Cannot probe".format(self.m.state()))
            # Watchdog should handle exiting the screen
    
    def watchdog_clock(self):
        if self.function_debug:
            Logger.debug("**** watchdog_clock called")
        self.watchdog_event = Clock.schedule_interval(lambda dt: self.watchdog(), 0.1)

    def watchdog(self):
        if self.function_debug:
            Logger.debug("**** watchdog called")
        machine_state = self.m.state().lower()
        screen = self.sm.current
        screen = str(screen).lower()

        self.not_probing =  machine_state != "run"
        self.alarm_triggered = "alarm" in machine_state or "alarm" in screen            

        if screen != 'probing':
            Clock.unschedule(self.watchdog_event)
        
        if screen == 'probing' and self.alarm_triggered:
            Logger.warning("Probing screen exited due to alarm")
            self.exit()
        if screen == 'probing' and self.not_probing:
            Clock.unschedule(self.watchdog_event)
            Clock.schedule_once(lambda dt:self.exit(), 2)

        if self.variable_debug:
            Logger.debug(("Watchdog:\nMachine state: " + machine_state, "Not probing: " + str(self.not_probing), "Alarm triggered: " + str(self.alarm_triggered)))

    def probe_button_press(self):
        pass
    
    def stop_button_press(self):
        if self.function_debug:
            Logger.debug("**** stop_button_press called")
        Logger.info("Probing cancelled by user")
        self.cancel_probing()
        self.exit()

    def cancel_probing(self):
        if self.function_debug:
            Logger.debug("**** cancel_probing called")
        Clock.unschedule(self.probing_event)
        self.m._grbl_feed_hold()
        Clock.schedule_once(lambda dt: self.m._grbl_soft_reset(), 0.5) # Wait before reseting to avoid alarm

    def exit(self):
        if self.function_debug:
            Logger.debug("**** exit called")
        # Should only be called if sm.current == 'probing'
        if self.sm.current != 'probing':
            Logger.warning("Probing screen exited but current screen may not be as expected")
        # If watchdog is scheduled, stop it
        if hasattr(self, "watchdog_event"):
            if self.watchdog_event.is_triggered:
                Clock.unschedule(self.watchdog_event)

        # Reset flags
        self.not_probing = False
        self.alarm_triggered = False

        # Call parent button's close_screen method
        self.parent_button.close_screen()
        
    def debug_log(self):
        Logger.debug(("Current screen: " + self.sm.current, "Machine state: " + self.m.state(), "Not probing: " + str(self.not_probing), "Alarm triggered: " + str(self.alarm_triggered), "Watchdog scheduled: " + str(self.watchdog_event.is_triggered)if hasattr(self, "watchdog_event") else "No watchdog event") )