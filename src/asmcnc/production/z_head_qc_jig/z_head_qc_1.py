from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime

from asmcnc.skavaUI import widget_status_bar
from asmcnc.skavaUI import popup_info
from asmcnc.production.z_head_qc_jig import popup_z_head_qc
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<ZHeadQC1>:

    fw_version_label : fw_version_label

    motor_chips_check : motor_chips_check
    home_button : home_button
    reset_button : reset_button

    spindle_toggle : spindle_toggle
    laser_toggle : laser_toggle
    vac_toggle : vac_toggle

    temp_voltage_power_check : temp_voltage_power_check

    x_home_check : x_home_check
    x_max_check : x_max_check
    
    console_status_text : console_status_text
    status_container : status_container

    bake_grbl_check: bake_grbl_check

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            GridLayout:
                cols: 3
                rows: 5
                size_hint_y: 0.85

                # ROW 1

                Button:
                    text: '<<< Back'
                    on_press: root.back_to_home()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Button:
                        text: '5. Test motor chips'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.test_motor_chips()

                    Image:
                        id: motor_chips_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                Button:
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    padding: [dp(10),0]
                    text: 'STOP'
                    background_color: color_provider.get_rgba("monochrome_red")
                    background_normal: ''
                    on_press: root.stop()

                # ROW 2

                Label:
                    id: fw_version_label
                    text: 'FW Version: ...'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Label:
                        text: '6. X Motors'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    GridLayout:
                        cols: 2

                        Button: 
                            text: 'Down'
                            text_size: self.size
                            markup: 'True'
                            halign: 'center'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.x_motor_down()
                            on_release: root.quit_jog()

                        Button:
                            text: 'Up'
                            text_size: self.size
                            markup: 'True'
                            halign: 'center'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.x_motor_up()
                            on_release: root.quit_jog()

                Button:
                    text: '12. Disable alarms'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.disable_alarms()

                # ROW 3

                GridLayout:
                    cols: 2

                    Label:
                        text: '1. Temp/power'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    Image:
                        id: temp_voltage_power_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                BoxLayout:
                    orientation: "horizontal"

                    Label:
                        text: '7. Z Motor'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        size_hint_x: 1.6

                    Button: 
                        text: 'Down'
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                        valign: 'middle'
                        padding: [dp(5),0]
                        on_press: root.z_motor_down()
                        on_release: root.quit_jog()
                        size_hint_x: 1

                    Button:
                        text: 'Up'
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.z_motor_up()
                        on_release: root.quit_jog()
                        size_hint_x: 1

                    Button: 
                        text: 'Cycle'
                        text_size: self.size
                        markup: 'True'
                        halign: 'center'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.mini_cycle()
                        size_hint_x: 1

                GridLayout:
                    cols: 2

                    Label:
                        text: '13. X Home'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    Image:
                        id: x_home_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                # ROW 4

                GridLayout:
                    cols: 2

                    Button:
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        text: '2. Bake GRBL Settings'
                        on_press: root.bake_grbl_settings()

                    Image:
                        id: bake_grbl_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                GridLayout:
                    cols: 3

                    ToggleButton: 
                        id: spindle_toggle
                        text: '8. Spindle'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.set_spindle()

                    ToggleButton:
                        id: laser_toggle
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        text: '9. Laser'
                        on_press: root.set_laser()

                    ToggleButton:
                        id: vac_toggle
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        text: '10. Vac'
                        on_press: root.set_vac()

                GridLayout:
                    cols: 2

                    Label:
                        text: '14. X Max'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    Image:
                        id: x_max_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                # ROW 5

                GridLayout:
                    cols: 2

                    Button:
                        id: home_button
                        text: '3. HOME'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.home()

                    Button: 
                        id: reset_button
                        text: '4. RESET'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.resume_from_alarm()

                GridLayout:
                    cols: 2

                    Label:
                        text: '11. Dust shoe'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    GridLayout:
                        cols: 3

                        Button: 
                            text: 'R'
                            text_size: self.size
                            markup: 'True'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.dust_shoe_red()

                        Button:
                            text: 'G'
                            text_size: self.size
                            markup: 'True'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.dust_shoe_green()

                        Button:
                            text: 'B'
                            on_press: root.dust_shoe_blue()

                Button:
                    text: '15. >>> Next screen'
                    on_press: root.enter_next_screen()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

            # RECIEVED STATUS MONITOR

            ScrollableLabelStatus:
                size_hint_y: 0.15
                id: console_status_text
                text: "status update" 
        
        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos

""")


class ZHeadQC1(Screen):

    def __init__(self, **kwargs):
        super(ZHeadQC1, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)


    # If polling starts while screens are being initialised, risks causing an instant fail! 
    # (as machine comms won't have started properly, causing nonsense value reads!)
    def on_enter(self):

        self.m.is_laser_enabled = True
        self.poll_for_fw = Clock.schedule_once(self.scrape_fw_version, 1)
        self.poll_for_limits = Clock.schedule_interval(self.update_checkboxes, 0.4)
        self.poll_for_temps_power = Clock.schedule_interval(self.temp_power_check, 5)
        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)

    def on_leave(self):
        Clock.unschedule(self.poll_for_status)
        Clock.unschedule(self.poll_for_limits)
        Clock.unschedule(self.poll_for_temps_power) # Otherwise a load of popups appear at once on failure

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text

        except: 
            pass

    # SCREEN GRID FUNCTIONS: 

    def back_to_home(self):
        self.sm.current = 'qchome'

    def scrape_fw_version(self, dt):
        try:
            self.fw_version_label.text = "FW: " + str((str(self.m.s.fw_version)).split('; HW')[0])
            if self.poll_for_fw != None: Clock.unschedule(self.poll_for_fw)
        
        except:
            pass

    def bake_grbl_settings(self):     

        if self.m.bake_default_grbl_settings(z_head_qc_bake=True):
            self.bake_grbl_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

        else: 
            self.bake_grbl_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            popup_info.PopupError(self.sm, self.l, "X current read in as 0! Can't set correct Z travel.")

    def test_motor_chips(self):

        # I think its fine to run both at the same time, but check on HW
        # self.m.jog_relative('Z', -63, 750) # move for 5 seconds at 750 mm/min
        # self.m.jog_relative('X', -700, 8000) # move for 5 seconds at 8000 mm/min
        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)
        # self.m.jog_absolute_single_axis('X', self.m.x_min_jog_abs_limit, 6000)
        # self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)
        Clock.schedule_once(self.try_start_motor_chips_test, 0.4)

    def try_start_motor_chips_test(self, dt):
        if self.m.s.m_state == "Idle":
            self.m.send_command_to_motor("REPORT RAW SG SET", command=REPORT_RAW_SG, value=1)
            self.m.s.write_command('$J=G91 X700 Z-63 F8035') # move for 5 seconds in x and z directions at max speed
            Clock.schedule_once(self.check_sg_values, 3)
        elif self.m.s.m_state == "Jog":
            Clock.schedule_once(self.try_start_motor_chips_test, 0.4)

    def check_sg_values(self, dt):

        pass_fail = True
        fail_report = []

        lower_sg_limit = 200
        upper_sg_limit = 800

        # If X motors are controlled by 2 drivers, don't measure combined X value
        if self.m.s.sg_x1_motor != None and self.m.s.sg_x2_motor != None:
            if lower_sg_limit <= self.m.s.sg_x1_motor <= upper_sg_limit:
                pass_fail = pass_fail*(True)

            else:
                pass_fail = pass_fail*(False)
                fail_report.append("X1 motor SG value: " + str(self.m.s.sg_x1_motor))
                fail_report.append("Should be between %s and %s." % (lower_sg_limit, upper_sg_limit))

            if lower_sg_limit <= self.m.s.sg_x2_motor <= upper_sg_limit:
                pass_fail = pass_fail*(True)

            else:
                pass_fail = pass_fail*(False)
                fail_report.append("X2 motor SG value: " + str(self.m.s.sg_x2_motor))
                fail_report.append("Should be between %s and %s." % (lower_sg_limit, upper_sg_limit))

        # If X motors are controlled by 1 driver, only measure combined X value
        else:
            if lower_sg_limit <= self.m.s.sg_x_motor_axis <= upper_sg_limit:
                pass_fail = pass_fail*(True)

            else:
                pass_fail = pass_fail*(False)
                fail_report.append("X motor/axis SG value: " + str(self.m.s.sg_x_motor_axis))
                fail_report.append("Should be between %s and %s." % (lower_sg_limit, upper_sg_limit))

        # Measure Z value
        if lower_sg_limit <= self.m.s.sg_z_motor_axis <= upper_sg_limit:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("Z motor/axis SG value: " + str(self.m.s.sg_z_motor_axis))
            fail_report.append("Should be between %s and %s." % (lower_sg_limit, upper_sg_limit))

        if not pass_fail:
            fail_report_string = "\n".join(fail_report)
            popup_z_head_qc.PopupTempPowerDiagnosticsInfo(self.sm, fail_report_string)
            self.motor_chips_check.source = "./asmcnc/skavaUI/img/template_cancel.png"

        else:
            self.motor_chips_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

        self.m.send_command_to_motor("REPORT RAW SG UNSET", command=REPORT_RAW_SG, value=0)


    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('qc1','qc1')

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

    def mini_cycle(self):
        self.m.s.write_command('G53 G0 Z-' + str(self.m.grbl_z_max_travel))
        self.m.s.write_command('G53 G0 Z-1')

    def quit_jog(self):
        self.m.quit_jog()

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

    def temp_power_check(self, dt):

        # Poll for all the temperatures, voltages, and power loss pin reported from the FW 
        # If one of them fails, polling will stop and report will be triggered.

        # pcb_temp
        # motor_driver_temp
        # transistor_heatsink_temp
        # microcontroller_mV 
        # LED_mV 
        # PSU_mV
        # ac_loss

        # note: spindle voltage monitor is tested with analogue spindle, 
        # despite being reported with these temps & voltages 

        pass_fail = True
        fail_report = []

        if 10 < self.m.s.pcb_temp < 70:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("PCB Temperature: " + str(self.m.s.pcb_temp) + " degrees C")
            fail_report.append("Should be greater than 10 and less than 70 deg C.")

        if 15 < self.m.s.motor_driver_temp < 100:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("Motor Driver Temperature: " + str(self.m.s.motor_driver_temp) + " degrees C")
            fail_report.append("Should be greater than 15 and less than 100 deg C.")

        if 0 < self.m.s.transistor_heatsink_temp < 100:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)

            fail_report.append("Transistor Heatsink Temperature: " + str(self.m.s.transistor_heatsink_temp) + " degrees C")
            fail_report.append("Should be greater than 0 and less than 100 deg C.")

        if 4500 < self.m.s.microcontroller_mV < 5500:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("Microcontroller voltage: " + str(self.m.s.microcontroller_mV) + " mV")
            fail_report.append("Should be greater than 4500 and less than 5500 mV.")

        if 4500 < self.m.s.LED_mV < 5500:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("LED (dust shoe) voltage: " + str(self.m.s.LED_mV) + " mV")
            fail_report.append("Should be greater than 4500 and less than 5500 mV.")

        if 22000 < self.m.s.PSU_mV < 26000:
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

        if not pass_fail:
            Clock.unschedule(self.poll_for_temps_power)
            fail_report_string = "\n".join(fail_report)
            popup_z_head_qc.PopupTempPowerDiagnosticsInfo(self.sm, fail_report_string)
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"

        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def disable_alarms(self):
        self.m.s.write_command('$20 = 0') # disable soft limit, to allow jog for motor chips test
        self.m.s.write_command('$21 = 0')

    def update_checkboxes(self, dt):
        self.x_home_switch()
        self.x_max_switch()

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

    def enter_next_screen(self):
        self.sm.current = 'qc2'

    def reset_checkboxes(self):
        self.motor_chips_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.x_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.bake_grbl_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.x_max_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
