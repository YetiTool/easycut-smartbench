from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_status_bar
from kivy.clock import Clock
from math import ceil, sqrt
from asmcnc.production.spindle_test_jig.popups.post_test_summary_popup import PostTestSummaryPopup
from asmcnc.production.spindle_test_jig.popups.popup_confirm_shutdown import ConfirmShutdownPopup
from os import system

Builder.load_string("""
<SpindleTestJig1>:
    status_container:status_container
    console_status_text:console_status_text
    pass_fail_img:pass_fail_img
    target_rpm_value:target_rpm_value
    measured_rpm_value:measured_rpm_value
    voltage_value:voltage_value
    load_value:load_value
    temp_value:temp_value
    kill_time_value:kill_time_value
    serial_number_value:serial_number_value
    mains_value:mains_value
    production_date_value:production_date_value
    up_time_value:up_time_value
    firmware_version_value:firmware_version_value
    brush_time_value:brush_time_value
    run_test_button:run_test_button

    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.8
            
            GridLayout:
                cols: 3
                rows: 1
                
                GridLayout:
                    cols: 1
                    rows: 3
                    size_hint_x: 0.4
                    
                    Button:
                        id: run_test_button
                        text: 'Begin Test'
                        bold: True
                        background_color: [0, 1, 0, 1]
                        on_press: root.run_spindle_test()
                        
                    Button:
                        text: 'Open Terminal'
                        bold: True
                        background_color: [0.62, 0.12, 0.94, 1]
                        on_press: root.open_console()
                        
                    Button:
                        text: 'Shutdown'
                        bold: True
                        on_press: root.shutdown()
                        background_color: [1, 0, 0, 1]
                        
                GridLayout:
                    cols: 1
                    rows: 3
                    
                    GridLayout:
                        cols: 2
                        rows: 1
                        size_hint_y: 0.15
                        
                        GridLayout:
                            cols: 2
                            rows: 1
                            
                            Label:
                                text: 'Target RPM:'
                                bold: True
                            
                            Label:
                                id: target_rpm_value
                        
                        GridLayout:
                            cols: 2
                            rows: 1
                            
                            Label:
                                text: 'Measured RPM:'
                                bold: True
                            
                            Label:
                                id: measured_rpm_value
                    
                    GridLayout:
                        cols: 4
                        rows: 1
                        size_hint_y: 0.35
                        
                        GridLayout:
                            cols: 1
                            rows: 2
                            
                            Label:
                                text: 'Voltage'
                                bold: True
                                
                            Label:
                                id: voltage_value
                        
                        GridLayout:
                            cols: 1
                            rows: 2
                            
                            Label:
                                text: 'Load'
                                bold: True
                                
                            Label:
                                id: load_value
                                
                        GridLayout:
                            cols: 1
                            rows: 2
                            
                            Label:
                                text: 'Temp'
                                bold: True
                                
                            Label:
                                id: temp_value
                        
                        GridLayout:
                            cols: 1
                            rows: 2
                            
                            Label:
                                text: 'Kill time'
                                bold: True
                                
                            Label:
                                id: kill_time_value
                    
                    BoxLayout:
                        orientation: 'vertical'
                        
                        Label:
                            size_hint_y: 0.2
                            text: 'Spindle Info'
                            bold: True
                            
                        GridLayout:
                            cols: 2
                            rows: 3
                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Serial Number'
                                    bold: True
                                    
                                Label:
                                    id: serial_number_value
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Mains'
                                    bold: True
                                    
                                Label:
                                    id: mains_value
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Production Date'
                                    bold: True
                                    
                                Label:
                                    id: production_date_value
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Up Time'
                                    bold: True
                                    
                                Label:
                                    id: up_time_value
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Firmware Version'
                                    bold: True
                                    
                                Label:
                                    id: firmware_version_value
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Brush Time'
                                    bold: True
                                    
                                Label:
                                    id: brush_time_value
                            
                GridLayout:
                    cols: 1
                    rows: 4
                    size_hint_x: 0.4
                    
                    Button:
                        text: 'STOP'
                        on_press: root.stop()
                        background_color: [1, 0, 0, 1]
                        
                    GridLayout:
                        cols: 2
                        rows: 1
                        
                        Label:
                            text: 'Pass:'
                            bold: True
                            
                        Image:
                            id: pass_fail_img
                            source: 'asmcnc/skavaUI/img/checkbox_inactive.png'
                    
                    BoxLayout:
                        orientation: 'vertical'
                        
                        canvas:
                            Color:
                                rgba: 0.62, 0.12, 0.94, 1
                            Rectangle:
                                pos: self.pos
                                size: self.size
                        
                        Label:
                            text: 'Unlock Code:'
                            bold: True
                            
                        Label:
                            text: '123456'
                        
                    Button:
                        text: 'Print'    
                        bold: True
                        background_color: [1, 0.64, 0, 1]
                        on_press: root.print_receipt()
                        
        ScrollableLabelStatus:
            size_hint_y: 0.12
            id: console_status_text
            text: "status update" 
                        
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")


def ld_qda_to_w(voltage, ld_qda):
    return voltage * 0.1 * sqrt(ld_qda)


def unschedule(clock):
    if clock is not None:
        Clock.unschedule(clock)
        clock = None


class SpindleTestJig1(Screen):
    fail_reasons = []
    clocks = []
    spindle_load_samples = []

    def __init__(self, **kwargs):
        super(SpindleTestJig1, self).__init__(**kwargs)

        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)

    def add_spindle_load(self):
        if len(self.spindle_load_samples) == 5:
            self.spindle_load_samples.pop(0)

        load = ld_qda_to_w(self.m.s.digital_spindle_mains_voltage,
                           self.m.s.digital_spindle_ld_qdA)
        self.spindle_load_samples.append(load)

    def generate_unlock_code(self):
        spindle_serial = self.m.s.spindle_serial_number

        return spindle_serial * 2 + 42

    def print_receipt(self):
        unlock_code = self.generate_unlock_code()
        system("python3 printer/receipt_printer.py " + str(unlock_code))

    def on_enter(self):
        self.send_get_digital_spindle_info()

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except:
            pass

    def stop(self):
        self.m.s.write_command('M5')
        [unschedule(clock) for clock in self.clocks]
        self.run_test_button.disabled = False

    def shutdown(self):
        ConfirmShutdownPopup()

    def update_spindle_feedback(self):
        self.voltage_value.text = str(self.m.s.digital_spindle_mains_voltage) + 'V'
        self.load_value.text = str(ceil(ld_qda_to_w(self.m.s.digital_spindle_mains_voltage, self.m.s.digital_spindle_ld_qdA))) + 'W'
        self.temp_value.text = str(self.m.s.digital_spindle_temperature) + 'C'
        self.kill_time_value.text = str(self.m.s.digital_spindle_kill_time) + 'S'
        self.measured_rpm_value.text = str(self.m.s.spindle_speed)

    def toggle_run_button(self):
        if self.run_test_button.disabled:
            self.run_test_button.disabled = False
        else:
            self.run_test_button.disabled = True

    def open_console(self):
        self.sm.current = 'spindle_test_console'

    def send_get_digital_spindle_info(self):
        self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
        Clock.schedule_once(lambda dt: self.show_digital_spindle_info(), 1)

    def show_digital_spindle_info(self):
        def format_week_year(week, year):
            return str(week) + 'th wk ' + str(year)

        def format_seconds(seconds):
            days = seconds // 86400
            seconds = seconds % 86400
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            return str(days) + 'd, ' + str(hours) + 'h, ' + str(minutes) + 'm, ' + str(seconds) + 's'

        self.serial_number_value.text = str(self.m.s.spindle_serial_number)
        self.mains_value.text = ('230V' if self.m.s.spindle_mains_frequency_hertz == 50 else '120V') + '/ ' + \
                                str(self.m.s.spindle_mains_frequency_hertz) + "Hz"
        self.production_date_value.text = format_week_year(self.m.s.spindle_production_week,
                                                           self.m.s.spindle_production_year)
        self.up_time_value.text = format_seconds(self.m.s.spindle_total_run_time_seconds)
        self.firmware_version_value.text = str(self.m.s.spindle_firmware_version)
        self.brush_time_value.text = format_seconds(self.m.s.spindle_brush_run_time_seconds)

    def run_spindle_test(self):
        self.toggle_run_button()

        def check_spindle_data_valid(rpm):
            def fail_test(message):
                self.fail_reasons.append([rpm, message])

            measured_rpm = int(self.m.s.spindle_speed)
            measured_voltage = self.m.s.digital_spindle_mains_voltage
            measured_temp = self.m.s.digital_spindle_temperature
            measured_kill_time = self.m.s.digital_spindle_kill_time
            measured_load = sum(self.spindle_load_samples) / len(self.spindle_load_samples)

            if abs(rpm - measured_rpm) > 2000:
                fail_test("RPM out of range: " + str(measured_rpm))

            if abs(230 - measured_voltage) > 15:
                fail_test("Voltage out of range: " + str(measured_voltage))

            if measured_temp < 10 or measured_temp > 40:
                fail_test("Temperature out of range: " + str(measured_temp))

            if not (measured_kill_time > 254):
                fail_test("Kill time out of range: " + str(measured_kill_time))

            if measured_load < 100 or measured_load > 400:
                fail_test("Load out of range: " + str(measured_load))

        def run_full_test():
            def set_spindle_rpm(rpm):
                self.m.s.write_command('M3 S' + str(rpm))
                self.target_rpm_value.text = str(rpm)

            def test_rpm(rpm):
                set_spindle_rpm(rpm)
                Clock.schedule_once(lambda dt: check_spindle_data_valid(rpm), 5)

            def stop_spindle():
                self.m.s.write_command('M5')

            def check_pass():
                total_fails = len(self.fail_reasons)

                if total_fails > 0:
                    self.pass_fail_img.source = 'asmcnc/apps/start_up_sequence/data_consent_app/img/red_cross.png'
                    return

                self.pass_fail_img.source = 'asmcnc/skavaUI/img/green_tick.png'

            def show_post_test_summary():
                PostTestSummaryPopup(self.m, self.fail_reasons)

            self.clocks[:] = []
            test_rpm(10000)
            self.clocks.append(Clock.schedule_once(lambda dt: test_rpm(13000), 6))
            self.clocks.append(Clock.schedule_once(lambda dt: test_rpm(19000), 12))
            self.clocks.append(Clock.schedule_once(lambda dt: test_rpm(22000), 18))
            self.clocks.append(Clock.schedule_once(lambda dt: test_rpm(25000), 24))
            self.clocks.append(Clock.schedule_once(lambda dt: stop_spindle(), 30))
            self.clocks.append(Clock.schedule_once(lambda dt: check_pass(), 32))
            self.clocks.append(Clock.schedule_once(lambda dt: self.toggle_run_button(), 34))
            self.clocks.append(Clock.schedule_once(lambda dt: show_post_test_summary(), 35))

        self.clocks.append(Clock.schedule_once(lambda dt: run_full_test(), 2))
