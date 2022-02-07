from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadQC2>:
    
    probe_check : probe_check
    z_home_check : z_home_check

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

                Label:
                    text: '20. Plug in digital spindle'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

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

                GridLayout:
                    cols: 2

                    Button:
                        text: '21. Test digital spindle'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        on_press: root.run_digital_spindle_test()

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
                        text: '25. Test USB "spindle"'
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

                GridLayout:
                    cols: 2

                    Label:
                        text: '17. Z Home'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    Image:
                        id: z_home_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                Label: 
                    text: '22. Remove digital spindle'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label:
                    text: '26. Remove USB "spindle"'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '18. Enable alarms'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.enable_alarms()

                Label: 
                    text: '23. Plug in USB "spindle"'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label: 
                    text: '27. TAKE BELT OFF Z MOTOR'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '19. Set spindle to digital'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.set_spindle_digital()

                Button:
                    text: '24. Set spindle to analogue'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.set_spindle_analogue()

                Button:
                    text: '28. CONFIRM BELT OFF: START AUTO-CALIBRATE'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.enter_next_screen()

            ScrollableLabelStatus:
                size_hint_y: 0.15 
                id: console_status_text
                text: "status update" 
        
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

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
        self.sm.current = 'qc3'

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except:
            pass

    def update_checkboxes(self, dt):
        self.probe()
        self.z_home_switch()

    def probe(self):
        if self.m.s.probe:
            self.probe_check.source = self.test_successful_image
        else:
            self.probe_check.source = self.test_unsuccessful_image

    def z_home_switch(self):
        if self.m.s.limit_z:
            self.z_home_check.source = self.test_successful_image
        else:
            self.z_home_check.source = self.test_unsuccessful_image

    def enable_alarms(self):
        self.m.s.write_command('$21 = 1')

    def run_digital_spindle_test(self):

        log('testing')

        def test_rpm():
            def read_rpm(): 
                if self.m.s.spindle_speed > 9500 and self.m.s.spindle_speed < 10500:
                    self.digital_spindle_pass_fail = True
                else: 
                    self.digital_spindle_pass_fail = False

            self.m.s.write_command('M3 10000')

            Clock.schedule_once(read_rpm, 3)

        def test_temperature():
            temperature = self.m.s.digital_spindle_temperature

            return temperature >= 0 and temperature <= 50

        def test_load():
            load = self.m.s.digital_spindle_ld_qdA

            return load >= 100 or load <= 10000

        def test_killtime():
            killtime = self.m.s.digital_spindle_kill_time
            
            return killtime == 255

        def test_voltage():
            voltage = self.m.s.digital_spindle_mains_voltage

            return voltage >= 100 and voltage <= 255

        if test_temperature() and test_load() and test_killtime() and test_voltage() and self.digital_spindle_pass_fail:
            log('Test passed')

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
        Clock.schedule_once(lambda dt: self.m.s.write_command('M5'), 45)


        def show_outcome():

            try: 
                self.spindle_test_counter = 0

                if self.spindle_pass_fail == 0:
                    self.spindle_speed_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
                    test = self.string_overload_summary.split("**")
                    popup_info.PopupSpindleDiagnosticsInfo(self.sm, test[1], test[2], test[3], test[4],test[5])

                else: 
                    self.spindle_speed_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

                self.spindle_pass_fail = True

            except:
                log("Could not show outcome")


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