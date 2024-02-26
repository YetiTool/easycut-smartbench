# -*- coding: utf-8 -*-
"""
Created Feb 2024

@author: Benji
"""
import sys
from datetime import datetime

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
                on_press: root.windows_cheat_to_procede()
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

def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime("%H:%M:%S.%f")[:12] + " " + str(message))


class ProbingScreen(Screen):
    button_reference = None

    def __init__(self, **kwargs):
        super(ProbingScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]

        self.debug = True

    def update_text(self, string):
        self.probing_label.text = self.l.get_str(string) + "..."      

    def on_enter(self):
        if self.debug:
            Clock.schedule_interval(lambda dt: self.debug_log(), 1)

        self.not_probing = False
        self.alarm_triggered = False
        delay_time = [0]

        self.update_text("Please wait")

        if self.m.reason_for_machine_pause == "Resuming":
            # In this scenario, the user has hit resume after stop bar was pressed
            # Screen is not aware that the machine has resumed probing
            self.update_text("Probing")
            self.m.reason_for_machine_pause = None

        if self.m.is_spindle_on():
            # Spindle is on, need to turn it off
            log("Spindle is on, turning off")
            self.m.turn_off_spindle()
            delay_time.append(8)

        if self.m.state().lower() == "run" or self.m.state().lower() == "jog":
            # Machine is running, need to stop it
            log("Machine is running, pausing")
            self.m._grbl_feed_hold()
            Clock.schedule_once(lambda dt: self.m._grbl_soft_reset(), 3.5) # Wait before reseting to avoid alarm
            delay_time.append(4)

        # Probe once machine is ready
        Clock.schedule_once(lambda dt: self.probe(), max(delay_time))
        
        # Start watchdog 1 sec after probe requested to give machine time to respond before interigating
        log("Has watchdog been scheduled? " + str(hasattr(self, "watchdog_event")))
        if not hasattr(self, "watchdog_event"):
            Clock.schedule_once(lambda dt: self.watchdog_clock(), max(delay_time) + 1)

    def probe(self):
        if self.m.state().lower() == "idle":
            self.m.probe_z()
            self.update_text("Probing")
        else:
            log("Machine state is {}, not idle. Cannot probe".format(self.m.state()))
            # Watchdog should handle exiting the screen
    
    def watchdog_clock(self):
        self.watchdog_event = Clock.schedule_interval(lambda dt: self.watchdog(), 0.1)

    def watchdog(self):
        machine_state = self.m.state().lower()
        screen = self.sm.current.lower()
        not_probing = self.not_probing
        alarm_triggered = self.alarm_triggered

        if machine_state != "run":
            # Machine isn't or is no longer probing
            not_probing = True
        if "alarm" in machine_state or "alarm" in screen:
            # Alarm occured
            alarm_triggered = True

        # Stop watchdog if screen closed
        if screen != 'probing':
            Clock.unschedule(self.watchdog_event)
        
        if screen == 'probing' and (not_probing or alarm_triggered):
            log("Probing screen exited due to alarm or incorrect machine state: " + str(machine_state))
            self.cancel_probing() # Just in case
            self.exit()

        if self.debug:
            log(("Watchdog:\nMachine state: " + machine_state, "Not probing: " + str(not_probing), "Alarm triggered: " + str(alarm_triggered)))

    def stop_button_press(self):
        log("Probing cancelled by user")
        self.cancel_probing()
        self.exit()

    def cancel_probing(self):
        self.m._grbl_feed_hold()
        Clock.schedule_once(lambda dt: self.m._grbl_soft_reset(), 0.5) # Wait before reseting to avoid alarm

    def exit(self):
        # Should only be called if sm.current == 'probing'
        if self.sm.current != 'probing':
            log("Probing screen exited but current screen may not be as expected")
        # If watchdog is scheduled, stop it
        if hasattr(self, "watchdog_event"):
            if self.watchdog_event.is_triggered:
                Clock.unschedule(self.watchdog_event)
        self.sm.current = self.sm.return_to_screen

    def debug_log(self):
        log(("Current screen: " + self.sm.current, "Machine state: " + self.m.state(), "Not probing: " + str(self.not_probing), "Alarm triggered: " + str(self.alarm_triggered), "Watchdog scheduled: " + str(self.watchdog_event.is_triggered)if hasattr(self, "watchdog_event") else "No watchdog event") )

