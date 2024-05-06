'''
Created on 03 August 2020
@author: Letty
'''

## Renumber all items after vac

import os, sys, subprocess
from datetime import datetime

from asmcnc.comms.logging_system.logging_system import Logger

try:
    import pigpio

except:
    pass

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

from asmcnc.comms import usb_storage
from asmcnc.skavaUI import popup_info
from asmcnc.production.z_head_qc_jig import popup_z_head_qc

from asmcnc.skavaUI import widget_status_bar
from asmcnc.core_UI import console_utils

Builder.load_string("""
<ZHeadQCWarrantyBeforeApr21>:
    fw_version_label : fw_version_label
    consoleStatusText : consoleStatusText
    # dust_shoe_check : dust_shoe_check
    x_home_check : x_home_check
    x_max_check : x_max_check
    z_home_check : z_home_check
    probe_check : probe_check
    spindle_toggle : spindle_toggle
    laser_toggle : laser_toggle
    vac_toggle : vac_toggle
    test_fw_update_button : test_fw_update_button
    status_container : status_container
    BoxLayout:
        orientation: 'vertical'
                
        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'
            GridLayout:
                size: self.parent.size
                pos: self.parent.pos
                cols: 3
                rows: 6
                cols_minimum: {0: 250, 1: 250, 2: 300}
        # Row 1
                GridLayout:
                    cols: 2
                    Label:
                        text: '  1. FW Version: '
                        color: color_provider.get_rgba("white")
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                    Label:
                        id: fw_version_label
                        text: 'fw version 1.etc.'
                        color: color_provider.get_rgba("white")
                GridLayout:
                    cols: 4
                    Label: 
                        text: '  9. Dust Shoe'
                        color: color_provider.get_rgba("white")
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                    Button: 
                        text: 'R'
                        on_press: root.dust_shoe_red()
                    Button: 
                        text: 'G'
                        on_press: root.dust_shoe_green()
                    Button:
                        text: 'B'
                        on_press: root.dust_shoe_blue()

                Button:
                    text: '  STOP'
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    on_press: root.stop()
                    background_color: [1,0,0,1]
                    background_normal: ''
        # Row 2
                GridLayout:
                    cols: 2
                    Button:
                        text: '  2. Bake GRBL Settings'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.bake_grbl_settings()
                    Button: 
                        text: '  2a. GRBL Monitor'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.open_monitor()
                Button:
                    text: '  10. DISABLE ALARMS'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    on_press: root.disable_alarms()

                Button:
                    text: '15. ENABLE ALARMS'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    on_press: root.enable_alarms()
                    padding: [dp(10),0]


        # Row 3
                GridLayout:
                    cols: 2
                    Button:
                        text: '  3a. HOME'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.home()
                    Button:
                        text: '  3b. RESET'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.resume_from_alarm()
                GridLayout:
                    cols: 2
                    Label: 
                        text: '  11. X Home'
                        color: color_provider.get_rgba("white")
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'        
                    Image:
                        id: x_home_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                Button: 
                    id: do_cycle
                    text: '  16. Cycle'
                    on_press: root.do_cycle()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'

        # Row 4
                GridLayout:
                    cols: 3
                    Label: 
                        text: ' 4. X motors'
                        color: color_provider.get_rgba("white")
                    Button: 
                        text: 'Up'
                        on_press: root.x_motor_up()
                        on_release: root.quit_jog()
                    Button: 
                        text: 'Down'
                        on_press: root.x_motor_down()
                        on_release: root.quit_jog()
                GridLayout:
                    cols: 2
                    Label: 
                        text: '  12. X Max'
                        color: color_provider.get_rgba("white")
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'       
                    Image:
                        id: x_max_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                Button: 
                    id: test_fw_update_button
                    text: '  17. Test FW Update'
                    on_press: root.test_fw_update()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
        # Row 5
                GridLayout:
                    cols: 3
                    Label: 
                        text: ' 5. Z motors'
                        color: color_provider.get_rgba("white")
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                    Button: 
                        text: 'Down'
                        on_press: root.z_motor_down()
                        on_release: root.quit_jog()
                    Button: 
                        text: 'Up'
                        on_press: root.z_motor_up()
                        on_release: root.quit_jog()
                GridLayout:
                    cols: 2
                    Label: 
                        text: '  13. Z Home'
                        color: color_provider.get_rgba("white")
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'      
                    Image:
                        id: z_home_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                Button: 
                    text: '  <<< Back'
                    on_press: root.back_to_choice()
                    color: color_provider.get_rgba("white")
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'  

        # Row 6
                GridLayout:
                    cols: 3
                    ToggleButton: 
                        id: spindle_toggle
                        text: '  6. Spindle'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.set_spindle()
                    ToggleButton: 
                        id: laser_toggle
                        text: '  7. Laser'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.set_laser()
                    ToggleButton: 
                        id: vac_toggle
                        text: '  8. Vac'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.set_vac()
                GridLayout:
                    cols: 2
                    Label: 
                        text: '  14. Probe'
                        color: color_provider.get_rgba("white")
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'    
                    Image:
                        id: probe_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                ScrollableLabelStatus:
                    size_hint_y: 0.2        
                    id: consoleStatusText
                    text: "status update" 
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")

STATUS_UPDATE_DELAY = 0.4
TEMP_POWER_POLL = 5

class ScrollableLabelStatus(ScrollView):
    text = StringProperty('')

class ZHeadQCWarrantyBeforeApr21(Screen):

    def __init__(self, **kwargs):

        super(ZHeadQCWarrantyBeforeApr21, self).__init__(**kwargs)
        self.m=kwargs['m']
        self.sm=kwargs['sm']
        self.l=kwargs['l']

        self.z_limit_set = False
        self.spindle_pass_fail = True
        self.string_overload_summary = ''
        self.spindle_test_counter = 0

        # Status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)
        # self.status_bar_widget.cheeky_color = '#1976d2'

    def on_enter(self, *args):
        self.string_overload_summary = ''
        Clock.schedule_interval(self.scrape_fw_version, 1)
        self.m.is_laser_enabled = True
        self.poll_for_status = Clock.schedule_interval(self.update_status_text, STATUS_UPDATE_DELAY)      # Poll for status
        self.poll_for_limits = Clock.schedule_interval(self.update_checkboxes, STATUS_UPDATE_DELAY)      # Poll for limit switches being triggered

    def on_leave(self, *args):
        Clock.unschedule(self.poll_for_status)
        Clock.unschedule(self.poll_for_limits)
        self.m.s.write_command('$21 = 1')

    def scrape_fw_version(self, dt):
        self.fw_version_label.text = str((str(self.m.s.fw_version)).split('; HW')[0])

    def bake_grbl_settings(self):
        grbl_settings = [
                    '$0=10',          #Step pulse, microseconds
                    '$1=255',         #Step idle delay, milliseconds
                    '$2=4',           #Step port invert, mask
                    '$3=1',           #Direction port invert, mask
                    '$4=0',           #Step enable invert, boolean
                    '$5=1',           #Limit pins invert, boolean
                    '$6=0',           #Probe pin invert, boolean
                    '$10=3',          #Status report, mask <----------------------
                    '$11=0.010',      #Junction deviation, mm
                    '$12=0.002',      #Arc tolerance, mm
                    '$13=0',          #Report inches, boolean
                    '$20=1',          #Soft limits, boolean <-------------------
                    # '$21=1',          #Hard limits, boolean <------------------
                    '$22=1',          #Homing cycle, boolean <------------------------
                    '$23=3',          #Homing dir invert, mask
                    '$24=600.0',      #Homing feed, mm/min
                    '$25=3000.0',     #Homing seek, mm/min
                    '$26=250',        #Homing debounce, milliseconds
                    '$27=15.000',     #Homing pull-off, mm
                    '$30=25000.0',    #Max spindle speed, RPM
                    '$31=0.0',        #Min spindle speed, RPM
                    '$32=0',          #Laser mode, boolean
                    # '$100=56.649',    #X steps/mm
                    # '$101=56.665',    #Y steps/mm
                    # '$102=1066.667',  #Z steps/mm
                    '$110=8000.0',    #X Max rate, mm/min
                    '$111=6000.0',    #Y Max rate, mm/min
                    '$112=750.0',     #Z Max rate, mm/min
                    '$120=130.0',     #X Acceleration, mm/sec^2
                    '$121=130.0',     #Y Acceleration, mm/sec^2
                    '$122=200.0',     #Z Acceleration, mm/sec^2
                    '$130=1300.0',    #X Max travel, mm TODO: Link to a settings object
                    '$131=2503.0',    #Y Max travel, mm
                    '$132=150.0',     #Z Max travel, mm
                    '$$',             # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#'              # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd
            ]

        self.m.s.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters

    def open_monitor(self):
        self.sm.get_screen('monitor').parent_screen = 'qcW112'
        self.sm.current = "monitor"

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('qcW112','qcW112')

    def resume_from_alarm(self):
        self.m.resume_from_alarm()

    def x_motor_up(self):
        self.m.jog_relative('X', 50, 6000)

    def x_motor_down(self):
        self.m.jog_relative('X', -50, 6000)

    def z_motor_up(self):
        self.m.jog_relative('Z', 20, 750)

    def z_motor_down(self):
        self.m.jog_relative('Z', -20, 750)

    def set_spindle(self):
        if self.m.s.spindle_on:
            self.m.turn_off_spindle()
        else:
            self.m.turn_on_spindle()

    def set_laser(self):
        if self.laser_toggle.state == 'normal':
            self.m.laser_off()
        else:
            self.m.laser_on()

    def set_vac(self):
        if self.m.s.vacuum_on:
            self.m.turn_off_vacuum()
        else:
            self.m.turn_on_vacuum()

    def dust_shoe_red(self):
        self.m.set_led_colour('RED')

    def dust_shoe_green(self):
        self.m.set_led_colour('GREEN')

    def dust_shoe_blue(self):
        self.m.set_led_colour('BLUE')

    def disable_alarms(self):
        self.m.s.write_command('$21 = 0')

    def enable_alarms(self):
        self.m.s.write_command('$21 = 1')

    def update_checkboxes(self, dt):
        # self.dust_shoe_switch()
        self.x_home_switch()
        self.x_max_switch()
        self.z_home_switch()
        self.probe()

    # def dust_shoe_switch(self):
    #     if self.m.s.dust_shoe_cover:
    #         self.dust_shoe_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    #     else:
    #         self.dust_shoe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def x_home_switch(self):
        if self.m.s.limit_x:
            self.x_home_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.x_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def x_max_switch(self):
        if self.m.s.limit_X:
            self.x_max_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.x_max_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def z_home_switch(self):
        if self.m.s.limit_z:
            self.z_home_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.z_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def probe(self):
        if self.m.s.probe:
            self.probe_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.probe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def cycle_limit_switch(self):
        if self.m.s.limit_z:
            self.cycle_limit_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.z_limit_set = True
        else:
            self.cycle_limit_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def quit_jog(self):
        self.m.quit_jog()

    def do_cycle(self):

        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')


    # TEST FIRMWARE UPDATE
    def test_fw_update(self):

        self.test_fw_update_button.text = "  Updating..."

        def disconnect_and_update():
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.m.close_serial_connection, 0.1)
            Clock.schedule_once(nested_do_fw_update, 1)

        def nested_do_fw_update(dt):
            pi = pigpio.pi()
            pi.set_mode(17, pigpio.ALT3)
            Logger.info(pi.get_mode(17))
            pi.stop()

            cmd = "grbl_file=/media/usb/GRBL*.hex && avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:$(echo $grbl_file):i"
            proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
            self.stdout, stderr = proc.communicate()
            self.exit_code = int(proc.returncode)

            connect()

        def connect():
            self.m.starting_serial_connection = True
            Clock.schedule_once(do_connection, 0.1)

        def do_connection(dt):
            self.m.reconnect_serial_connection()
            self.poll_for_reconnection = Clock.schedule_interval(try_start_services, 0.4)

        def try_start_services(dt):
            if self.m.s.is_connected():
                Clock.unschedule(self.poll_for_reconnection)
                Clock.schedule_once(self.m.s.start_services, 1)
                # hopefully 1 second should always be enough to start services
                Clock.schedule_once(update_complete, 2)

        def update_complete(dt):
            if self.exit_code == 0:
                did_fw_update_succeed = "Success!"

            else:
                did_fw_update_succeed = "Update failed."

            popup_z_head_qc.PopupFWUpdateDiagnosticsInfo(self.sm, did_fw_update_succeed, str(self.stdout))
            self.test_fw_update_button.text = '  17. Test FW Update'

            self.sm.get_screen('qc1').reset_checkboxes()
            self.sm.get_screen('qc2').reset_checkboxes()
            self.sm.get_screen('qcW136').reset_checkboxes()
            self.sm.get_screen('qcW112').reset_checkboxes()
            self.sm.get_screen('qc3').reset_timer()

        disconnect_and_update()


    def update_status_text(self, dt):
        self.consoleStatusText.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text

    def back_to_choice(self):
        self.sm.current = 'qcWC'

    def reset_checkboxes(self):
        self.x_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.x_max_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.z_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.probe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
