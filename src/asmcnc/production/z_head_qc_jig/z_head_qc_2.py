from asmcnc.comms.logging_system.logging_system import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
from asmcnc.production.z_head_qc_jig import popup_z_head_qc

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadQC2>:
    
    probe_check : probe_check
    spindle_speed_check:spindle_speed_check
    digital_spindle_check:digital_spindle_check

    console_status_text : console_status_text
    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            GridLayout:
                size_hint_y: 0.85
                cols: 3
                rows: 5

                Button:
                    text: '<<< Back'
                    on_press: root.enter_prev_screen()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Button:
                        text: '20. Test digital spindle (up to 45s)'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.run_digital_spindle_test()

                    Image:
                        id: digital_spindle_check
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
                    background_color: [1,0,0,1]
                    background_normal: ''
                    on_press: root.stop()

                GridLayout:
                    cols: 2

                    Label:
                        text: '16. Probe'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    Image:
                        id: probe_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                Label: 
                    text: '21. Remove digital spindle'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label:
                    text: '25. Remove USB "spindle"'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '17. Enable alarms'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.enable_alarms()

                Label: 
                    text: '22. Plug in USB "spindle"'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '26. CONFIRM COVER ON: START AUTO-CALIBRATE'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.enter_next_screen()

                Button:
                    text: '18. Set spindle to digital'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.set_spindle_digital()

                Button:
                    text: '23. Set spindle to analogue'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.set_spindle_analogue()

                Label

                Label:
                    text: '19. Plug in digital spindle'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Button:
                        text: '24. Test USB "spindle" (wait 45s)'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.run_analogue_spindle_check()

                    Image:
                        id: spindle_speed_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                Label

            ScrollableLabelStatus:
                size_hint_y: 0.15 
                id: console_status_text
                text: "status update" 
        
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")


class ZHeadQC2(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC2, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']

        self.test_successful_image = "./asmcnc/skavaUI/img/file_select_select.png"
        self.test_unsuccessful_image = "./asmcnc/skavaUI/img/checkbox_inactive.png"

        self.string_overload_summary = ''
        self.spindle_pass_fail = True
        self.digital_spindle_pass_fail = True

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        # Status monitor widget
        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)

    def on_enter(self):
        self.poll_for_limits = Clock.schedule_interval(self.update_checkboxes, 0.4)

    def enter_prev_screen(self):
        self.sm.current = 'qc1'

    def enter_next_screen(self):
        self.m.resume_from_alarm()
        self.sm.current = 'qc3'

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except:
            pass

    def update_checkboxes(self, dt):
        self.probe()

    def probe(self):
        if self.m.s.probe:
            self.probe_check.source = self.test_successful_image
        else:
            self.probe_check.source = self.test_unsuccessful_image

    def enable_alarms(self):
        self.m.s.write_command('$20 = 1')
        self.m.s.write_command('$21 = 1')

    def run_digital_spindle_test(self):

        if self.m.s.m_state == "Idle":
            Logger.info('testing')
            self.brush_reset_test_count = 0
            self.initial_run_time = None
            self.spindle_brush_reset()

        else:
            popup_info.PopupError(self.sm, self.l, "Machine should be in idle state for this test")

    def spindle_brush_reset(self):
        def read_info(dt):
            self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
            Clock.schedule_once(get_info, 1)

        def get_info(dt):
            self.initial_run_time = self.m.s.spindle_brush_run_time_seconds
            if self.initial_run_time == 0:
                fail_report.append("Spindle brush run time was 0 before reset.")
            self.m.s.write_protocol(self.m.p.ResetDigitalSpindleBrushTime(), "RESET DIGITAL SPINDLE BRUSH TIME")
            Clock.schedule_once(read_info_again, 3)

        def read_info_again(dt):
            self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
            Clock.schedule_once(compare_info, 1)

        def compare_info(dt):
            if self.m.s.spindle_brush_run_time_seconds == 0:
                self.m.turn_off_spindle()
                self.test_rpm(fail_report)
            else:
                fail_report.append("Spindle brush time after reset was " + str(self.m.s.spindle_brush_run_time_seconds) + ". Should be 0")
                self.m.turn_off_spindle()
                self.test_rpm(fail_report)

        fail_report = []
        self.brush_reset_test_count += 1
        self.m.turn_on_spindle_for_data_read()  # Turn on spindle to read info (at 0 rpm)

        Clock.schedule_once(read_info, 1)

    def test_rpm(self, fail_report):
        def read_rpm(dt):
            spindle_rpm = int(self.m.s.spindle_speed)

            Logger.info('Spindle RPM: %s' % spindle_rpm)

            if spindle_rpm < 8000 or spindle_rpm > 12000:
                fail_report.append("Spindle RPM was " + str(spindle_rpm) + ". Should be 8000-12000")

            self.m.turn_off_spindle()
            self.continue_digital_spindle_test(fail_report)

        rpm_to_run = 10000

        self.m.turn_on_spindle(rpm_to_run)

        Clock.schedule_once(read_rpm, 3)

    def continue_digital_spindle_test(self, fail_report):

        temperature = self.m.s.digital_spindle_temperature
        Logger.info('Digital Spindle Temperature: %s' % temperature)
        if temperature < 0 or temperature > 50:
            fail_report.append("Temperature was " + str(temperature) + ". Should be 0-50")

        load = self.m.s.digital_spindle_ld_qdA
        Logger.info('Digital Spindle Load: %s' % load)
        if load < 50 or load > 10000:
            fail_report.append("Load was " + str(load) + ". Should be 50-10000")

        killtime = self.m.s.digital_spindle_kill_time
        Logger.info('Digital Spindle KillTime: %s' % killtime)
        if killtime != 255:
            fail_report.append("KillTime was " + str(killtime) + ". Should be 255")

        voltage = self.m.s.digital_spindle_mains_voltage
        Logger.info('Digital Spindle Voltage: %s' % voltage)
        if voltage < 100 or voltage > 255:
            fail_report.append("Voltage was " + str(voltage) + ". Should be 100-255")

        if not fail_report:
            Logger.info('Test passed')
            self.digital_spindle_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            if self.brush_reset_test_count < 5 and (self.initial_run_time == 0 or self.m.s.spindle_brush_run_time_seconds != 0):
                self.spindle_brush_reset()
            else:
                Logger.info('Test failed')
                fail_report_string = "\n".join(fail_report)
                popup_z_head_qc.PopupTempPowerDiagnosticsInfo(self.sm, fail_report_string)
                self.digital_spindle_check.source = "./asmcnc/skavaUI/img/template_cancel.png"

    def run_analogue_spindle_check(self):
        
        # Send command:
        # 5000 RPM = 1.2 V
        self.analogue_spindle_check('M3 S5000', 2000, 2000)

        # 10000 RPM = 3.4 - 3.6 V 
        Clock.schedule_once(lambda dt: self.analogue_spindle_check('M3 S10000', 4000, 4000), 9)

        # 15000 RPM = 5.6 - 5.8 V
        Clock.schedule_once(lambda dt: self.analogue_spindle_check('M3 S15000', 6000, 6000), 18)

        # 20000 RPM = 7.8 V
        Clock.schedule_once(lambda dt: self.analogue_spindle_check('M3 S20000', 7800, 8000), 27)

        # # 250000 RPM = 10 V
        Clock.schedule_once(lambda dt: self.analogue_spindle_check('M3 S25000', 8500, 10000), 36)

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
                Logger.info("Could not show outcome")


        Clock.schedule_once(lambda dt: show_outcome(), 45)


    def analogue_spindle_check(self, M3_command, ld_expected_mV, speed_expected_mV):

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

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def set_spindle_digital(self):
        self.m.s.write_command('$51 = 1')

    def set_spindle_analogue(self):
        self.m.s.write_command('$51 = 0')

    def reset_checkboxes(self):
        self.digital_spindle_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.probe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
        self.spindle_speed_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"
