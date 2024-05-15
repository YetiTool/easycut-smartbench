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
<ZHeadQCWarrantyAfterApr21>:
    fw_version_label : fw_version_label
    consoleStatusText : consoleStatusText
    # dust_shoe_check : dust_shoe_check
    x_home_check : x_home_check
    x_max_check : x_max_check
    z_home_check : z_home_check
    probe_check : probe_check
    temp_voltage_power_check : temp_voltage_power_check
    spindle_toggle : spindle_toggle
    laser_toggle : laser_toggle
    vac_toggle : vac_toggle
    spindle_speed_check : spindle_speed_check
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
                    Button: 
                        size_hint_x: 0.3
                        text: '  <<< Back'
                        on_press: root.back_to_choice()
                        color: 1,1,1,1
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                    Label:
                        id: fw_version_label
                        size_hint_x: 0.6
                        text: 'fw version 1.etc.'
                        color: 1,1,1,1
                GridLayout:
                    cols: 4
                    Label: 
                        text: '  9. Dust Shoe'
                        color: 1,1,1,1
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
                GridLayout:
                    cols: 2
                    Button:
                        text: '15. ENABLE ALARMS'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.enable_alarms()
                        padding: app.get_scaled_tuple([10, 0])
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
                GridLayout:
                    cols: 2
                    Label: 
                        text: '  16. Temp/Power'
                        color: 1,1,1,1
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                    Image:
                        id: temp_voltage_power_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
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
                        color: 1,1,1,1
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
                    text: '  17. Cycle'
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
                        color: 1,1,1,1
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
                        color: 1,1,1,1
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
                GridLayout:
                    cols: 2
                    Button: 
                        text: '18. Spindle Speed Check (wait 45 seconds)'
                        color: 1,1,1,1
                        on_press: root.run_spindle_check()
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                        valign: 'middle'
                    Image:
                        id: spindle_speed_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
        # Row 5
                GridLayout:
                    cols: 3
                    Label: 
                        text: ' 5. Z motors'
                        color: 1,1,1,1
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
                        color: 1,1,1,1
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
                    id: test_fw_update_button
                    text: '  19. Test FW Update'
                    on_press: root.test_fw_update()
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
                        color: 1,1,1,1
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

class ZHeadQCWarrantyAfterApr21(Screen):

    def __init__(self, **kwargs):

        super(ZHeadQCWarrantyAfterApr21, self).__init__(**kwargs)
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
        self.poll_for_temps_power = Clock.schedule_interval(self.temp_power_check, TEMP_POWER_POLL)      # Poll for status

    def on_leave(self, *args):
        Clock.unschedule(self.poll_for_status)
        Clock.unschedule(self.poll_for_limits)
        Clock.unschedule(self.poll_for_temps_power)
        self.m.s.write_command('$21 = 1')

    def scrape_fw_version(self, dt):
        self.fw_version_label.text = "FW: " + str((str(self.m.s.fw_version)).split('; HW')[0])

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
        self.sm.get_screen('monitor').parent_screen = 'qcW136'
        self.sm.current = "monitor"

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('qcW136','qcW136')

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
        if self.spindle_toggle.state == 'normal': 
            self.m.turn_off_spindle()
        else: 
            self.m.turn_on_spindle()

    def set_laser(self):
        if self.laser_toggle.state == 'normal': 
            self.m.laser_off()
        else: 
            self.m.laser_on()

    def set_vac(self):
        if self.vac_toggle.state == 'normal': 
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


    def temp_power_check(self, dt):
        # pcb_temp
        # motor_driver_temp
        # microcontroller_mV 
        # LED_mV 
        # PSU_mV
        # ac_loss

        pass_fail = True
        fail_report = []

        # Poll for all the temperatures, voltages, and power loss pin reported from the FW 
        # If one of them fails, polling will stop and report will be triggered.

        if (self.m.s.pcb_temp > 10) and (self.m.s.pcb_temp < 70):
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("PCB Temperature: " + str(self.m.s.pcb_temp) + " degrees C")
            fail_report.append("Should be greater than 10 and less than 70 deg C.")

        if (self.m.s.motor_driver_temp > 10) and (self.m.s.motor_driver_temp < 60):
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("Motor Driver Temperature: " + str(self.m.s.motor_driver_temp) + " degrees C")
            fail_report.append("Should be greater than 10 and less than 60 deg C.")

        if (self.m.s.microcontroller_mV > 4800) and (self.m.s.microcontroller_mV < 5200):
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("Microcontroller voltage: " + str(self.m.s.microcontroller_mV) + " mV")
            fail_report.append("Should be greater than 4800 and less than 5200 mV.")

        if (self.m.s.LED_mV > 4800) and (self.m.s.LED_mV < 5200):
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("LED (dust shoe) voltage: " + str(self.m.s.LED_mV) + " mV")
            fail_report.append("Should be greater than 4800 and less than 5200 mV.")

        if (self.m.s.PSU_mV > 22000) and (self.m.s.PSU_mV < 26000):
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("24V PSU Voltage: " + str(self.m.s.PSU_mV) + " mV")
            fail_report.append("Should be greater than 22000 and less than 26000 mV.")

        if self.m.s.power_loss_detected == True:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("AC Loss: " + str(self.m.s.power_loss_detected))
            fail_report.append("AC should be reported as lost (True) on diagnostics jig.")

        if pass_fail == 0:
            Clock.unschedule(self.poll_for_temps_power)
            fail_report_string = "\n".join(fail_report)
            popup_z_head_qc.PopupTempPowerDiagnosticsInfo(self.sm, fail_report_string)
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"

        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def cycle_limit_switch(self):
        if self.m.s.limit_z:
            self.cycle_limit_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.z_limit_set = True
        else:
            self.cycle_limit_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"        

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


    # SPINDLE OVERLOAD VOLTAGE AND SPEED VOLTAGE CHECKING FUNCTIONS

    def run_spindle_check(self):
        
        # Send command:
        # 5000 RPM = 1.2 V
        self.spindle_check('M3 S5000', 2000, 2000)

        # 10000 RPM = 3.4 - 3.6 V 
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S10000', 4000, 4000), 9)

        # 15000 RPM = 5.6 - 5.8 V
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S15000', 6000, 6000), 18)

        # 20000 RPM = 7.8 V
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S20000', 7800, 8000), 27)

        # # 250000 RPM = 10 V
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S25000', 8500, 10000), 36)

        # Spindle off
        Clock.schedule_once(lambda dt: self.m.turn_off_spindle(), 45)


        def show_outcome():

            try: 
                self.spindle_test_counter = 0

                if self.spindle_pass_fail == 0:
                    self.spindle_speed_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
                    test = self.string_overload_summary.split("**")
                    popup_z_head_qc.PopupSpindleDiagnosticsInfo(self.sm, test[1], test[2], test[3], test[4],test[5])

                else: 
                    self.spindle_speed_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

                self.spindle_pass_fail = True

            except:
                Logger.exception("Could not show outcome")


        Clock.schedule_once(lambda dt: show_outcome(), 45)


    def spindle_check(self, M3_command, ld_expected_mV, speed_expected_mV):

        self.spindle_test_counter = 1

        def overload_check(ld_mid_range_mV, speed_mid_range_mV):

            # 5000 RPM = 1.7V - 2.3V
            # 10000 RPM = 3.3V - 4.5V
            # 15000 RPM = 5.0V - 6.5V

            if speed_mid_range_mV < 10000:

                speed_V_tolerance = int(0.2*speed_mid_range_mV)

                if ld_mid_range_mV == 7800: 
                    ld_tolerance = 1800

                else:
                    ld_tolerance = int(0.2*ld_mid_range_mV)

            else: 
                ld_tolerance = 2500
                speed_V_tolerance = int(0.1*speed_mid_range_mV)

            if self.spindle_test_counter == 1:
                self.string_overload_summary = self.string_overload_summary + '\n' + 'Ld range: ' + '\n' + str(ld_mid_range_mV - ld_tolerance) + " - " + str(ld_mid_range_mV + ld_tolerance) + " mV"
                self.string_overload_summary = self.string_overload_summary + '\n' + 'Speed V range: ' + '\n' + str(speed_mid_range_mV - speed_V_tolerance) + " - " + str(speed_mid_range_mV + speed_V_tolerance) + " mV"
            elif self.spindle_test_counter > 3:
                return

            overload_value = self.m.s.spindle_load_voltage
            spindle_speed_value = self.m.s.spindle_speed_monitor_mV

            self.string_overload_summary = self.string_overload_summary + '\n' + "Test " + str(self.spindle_test_counter) + ":\n  V_Ld: " + str(overload_value) + " mV" + "\n  V_s: " + str(spindle_speed_value) + " mV"

            self.is_it_within_tolerance(overload_value, ld_mid_range_mV, ld_tolerance)
            self.is_it_within_tolerance(spindle_speed_value, speed_mid_range_mV, speed_V_tolerance)

            self.spindle_test_counter+=1

            # end of inner function

        Clock.schedule_once(lambda dt: self.m.s.write_command(M3_command), 0.1)

        self.string_overload_summary = self.string_overload_summary + "**" + "[b]" + str(M3_command).strip("M3 S") + " RPM[/b]"

        overload_check_event = Clock.schedule_interval(lambda dt: overload_check(ld_expected_mV, speed_expected_mV), 2.5)

        Clock.schedule_once(lambda dt: Clock.unschedule(overload_check_event), 8)
        
    def is_it_within_tolerance(self, value, expected, tolerance):

        if (value >= (expected - tolerance)) and (value <= (expected + tolerance)):
            self.spindle_pass_fail = self.spindle_pass_fail*(True)
        else: 
            self.spindle_pass_fail = self.spindle_pass_fail*(False)


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
            self.test_fw_update_button.text = "  19. Test FW Update"

            self.sm.get_screen('qc1').reset_checkboxes()
            self.sm.get_screen('qc2').reset_checkboxes()
            self.sm.get_screen('qcW136').reset_checkboxes()
            self.sm.get_screen('qcW112').reset_checkboxes()
            self.sm.get_screen('qc3').reset_timer()
            Clock.unschedule(self.poll_for_temps_power)
            self.poll_for_temps_power = Clock.schedule_interval(self.temp_power_check, TEMP_POWER_POLL)

        disconnect_and_update()

    def update_status_text(self, dt):
        self.consoleStatusText.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text

    def back_to_choice(self):
        self.sm.current = 'qcWC'

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def reset_checkboxes(self):
        self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.x_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.x_max_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.spindle_speed_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.z_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.probe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
