from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.skavaUI import widget_status_bar
from asmcnc.skavaUI import popup_info

Builder.load_string("""
<ZHeadQC1>:
    status_container:status_container
    console_status_text:console_status_text
    home_button:home_button
    reset_button:reset_button
    spindle_toggle:spindle_toggle
    laser_toggle:laser_toggle
    vac_toggle:vac_toggle
    temp_voltage_power_check:temp_voltage_power_check
    motor_chips_check:motor_chips_check
    x_home_check:x_home_check
    x_max_check:x_max_check

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            GridLayout:
                cols: 3
                rows: 5
                size_hint_y: 0.85

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

                    Label:
                        text: '5. X Motors'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    GridLayout:
                        cols: 2

                        Button:
                            text: 'Up'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.x_motor_up()
                            on_release: root.quit_jog()
                        
                        Button: 
                            text: 'Down'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.x_motor_down()
                            on_release: root.quit_jog()

                Button:
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    padding: [dp(10),0]
                    text: 'STOP'
                    background_color: [1,0,0,1]
                    background_normal: ''

                Label:
                    text: 'FW Version: ...'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Label:
                        text: '6. Z Motors'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    GridLayout:
                        cols: 2

                        Button:
                            text: 'Up'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.z_motor_up()
                            on_release: root.quit_jog()

                        Button: 
                            text: 'Down'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]
                            on_press: root.z_motor_down()
                            on_release: root.quit_jog()

                Button:
                    text: '12. Disable alarms'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.disable_alarms()

                Button:
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    text: '1. Bake GRBL Settings'
                    on_press: root.bake_grbl_settings()

                GridLayout:
                    cols: 3

                    ToggleButton: 
                        id: spindle_toggle
                        text: '7. Spindle'
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
                        text: '8. Laser'
                        on_press: root.set_laser()

                    ToggleButton:
                        id: vac_toggle
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        text: '9. Vac'
                        on_press: root.set_vac()

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

                GridLayout:
                    cols: 2

                    Button:
                        text: '2. Test motor chips'
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

                GridLayout:
                    cols: 2

                    Label:
                        text: '10. Dust shoe'
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
                        text: '11. Temp/power'
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

                Button:
                    text: '15. >>> Next screen'
                    on_press: root.enter_next_screen()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

            ScrollableLabelStatus:
                size_hint_y: 0.15
                id: console_status_text
                text: "status update" 
        
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

        self.m.is_laser_enabled = True
        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4) 
        self.poll_for_limits = Clock.schedule_interval(self.update_checkboxes, 0.4)
        self.poll_for_temps_power = Clock.schedule_interval(self.temp_power_check, 5) 
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        # Placeholder
        self.m.s.ac_loss = False

    def enter_next_screen(self):
        self.sm.current = 'qc2'

    def back_to_home(self):
        self.sm.current = 'qchome'

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except: 
            pass

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
                    '$131=2502.0',    #Y Max travel, mm
                    '$132=150.0',     #Z Max travel, mm
                    '$$',             # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#'              # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd
            ]

        self.m.s.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters

    def test_motor_chips(self):
        self.m.jog_relative('X', 30000, 6000)
        test = Clock.schedule_once(self.check_sg_values, 3)

    def check_sg_values(self, dt):
        if 200 <= self.m.s.x_motor_axis <= 800:
            self.motor_chips_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            popup_info.PopupTempPowerDiagnosticsInfo(self.sm, "SG value: " + str(self.m.s.x_motor_axis) + "\nShould be between 200 and 800.")
            self.motor_chips_check.source = "./asmcnc/skavaUI/img/template_cancel.png"

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

    def quit_jog(self):
        self.m.quit_jog()

    def set_spindle(self):
        if self.spindle_toggle.state == 'normal': 
            self.m.spindle_off()
        else: 
            self.m.spindle_on()

    def set_laser(self):
        if self.laser_toggle.state == 'normal': 
            self.m.laser_off()
        else: 
            self.m.laser_on()

    def set_vac(self):
        if self.vac_toggle.state == 'normal': 
            self.m.vac_off()
        else: 
            self.m.vac_on()

    def dust_shoe_red(self):
        self.m.set_led_colour('RED')

    def dust_shoe_green(self):
        self.m.set_led_colour('GREEN')

    def dust_shoe_blue(self):
        self.m.set_led_colour('BLUE')

    def disable_alarms(self):
        self.m.s.write_command('$21 = 0')

    def temp_power_check(self, dt):
        # pcb_temp
        # motor_driver_temp
        # transistor_heatsink_temp
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
            fail_report.append("Should be greater than 10 and less than 50 deg C.")

        if (self.m.s.motor_driver_temp > 10) and (self.m.s.motor_driver_temp < 50):
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("Motor Driver Temperature: " + str(self.m.s.motor_driver_temp) + " degrees C")
            fail_report.append("Should be greater than 10 and less than 50 deg C.")

        if 0 < self.m.s.transistor_heatsink_temp < 100:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("Transistor Heatsink Temperature: " + str(self.m.s.transistor_heatsink_temp) + "degrees C")
            fail_report.append("Should be greater than 0 and less than 100 deg C.")

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

        if self.m.s.ac_loss == True:
            pass_fail = pass_fail*(True)

        else:
            pass_fail = pass_fail*(False)
            fail_report.append("AC Loss: " + str(self.m.s.ac_loss))
            fail_report.append("AC should be reported as lost (True) on diagnostics jig.")

        if pass_fail == 0:
            Clock.unschedule(self.poll_for_temps_power)
            fail_report_string = "\n".join(fail_report)
            popup_info.PopupTempPowerDiagnosticsInfo(self.sm, fail_report_string)
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"

        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def update_checkboxes(self, dt):
        # self.dust_shoe_switch()
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
