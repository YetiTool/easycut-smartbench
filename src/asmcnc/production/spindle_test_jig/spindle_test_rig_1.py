from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_status_bar
from kivy.clock import Clock

Builder.load_string("""
<SpindleTestRig1>:
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
                        text: 'Begin Test'
                        bold: True
                        background_color: [0, 1, 0, 1]
                        on_press: root.run_spindle_test()
                        
                    Button:
                        text: 'Open Terminal'
                        bold: True
                        background_color: [0.62, 0.12, 0.94, 1]
                        
                    Button:
                        text: 'Shutdown'
                        bold: True
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
                                text: '10,000'
                        
                        GridLayout:
                            cols: 2
                            rows: 1
                            
                            Label:
                                text: 'Measured RPM:'
                                bold: True
                            
                            Label:
                                id: measured_rpm_value
                                text: '10,510'
                    
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
                                text: '231V'
                        
                        GridLayout:
                            cols: 1
                            rows: 2
                            
                            Label:
                                text: 'Load'
                                bold: True
                                
                            Label:
                                id: load_value
                                text: '250W'
                                
                        GridLayout:
                            cols: 1
                            rows: 2
                            
                            Label:
                                text: 'Temp'
                                bold: True
                                
                            Label:
                                id: temp_value
                                text: '30C'
                        
                        GridLayout:
                            cols: 1
                            rows: 2
                            
                            Label:
                                text: 'Kill time'
                                bold: True
                                
                            Label:
                                id: kill_time_value
                                text: '255 S'
                    
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
                                    text: '16959'
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Mains'
                                    bold: True
                                    
                                Label:
                                    id: mains_value
                                    text: '235V/50Hz'
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Production Date'
                                    bold: True
                                    
                                Label:
                                    id: production_date_value
                                    text: '15th wk 2022'
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Up Time'
                                    bold: True
                                    
                                Label:
                                    id: up_time_value
                                    text: '1wk, 1d, 9h, 33m, 52s'
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Firmware Version'
                                    bold: True
                                    
                                Label:
                                    id: firmware_version_value
                                    text: '10'
                                    
                            GridLayout:
                                cols: 1
                                rows: 2
                                
                                Label:
                                    text: 'Brush Time'
                                    bold: True
                                    
                                Label:
                                    id: brush_time_value
                                    text: '2d, 7h, 45m, 34s'
                            
                GridLayout:
                    cols: 1
                    rows: 4
                    size_hint_x: 0.4
                    
                    Button:
                        text: 'STOP'
                        background_color: [1, 0, 0, 1]
                        
                    GridLayout:
                        cols: 2
                        rows: 1
                        
                        Label:
                            id: pass_fail_img
                            text: 'Pass:'
                            bold: True
                            
                        Image:
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
                        
        ScrollableLabelStatus:
            size_hint_y: 0.12
            id: console_status_text
            text: "status update" 
                        
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")

from math import sqrt


def ld_qda_to_w(voltage, ld_qda):
    return voltage * 0.1 * sqrt(ld_qda)


def unschedule(clock):
    if clock is not None:
        Clock.unschedule(clock)
        clock = None


class SpindleTestRig1(Screen):
    rpm_13000_clock = None
    rpm_19000_clock = None
    rpm_22000_clock = None
    rpm_25000_clock = None
    stop_spindle_clock = None

    fail_reasons = []

    def __init__(self, **kwargs):
        super(SpindleTestRig1, self).__init__(**kwargs)

        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except:
            pass

    def update_spindle_feedback(self):
        self.voltage_value.text = str(self.m.s.digital_spindle_mains_voltage) + 'V'
        self.load_value.text = str(ld_qda_to_w(self.m.s.digital_spindle_ld_qdA)) + 'W'
        self.temp_value.text = str(self.m.s.digital_spindle_temperature) + 'C'
        self.kill_time_value.text = str(self.m.s.digital_spindle_kill_time) + 'S'

    def run_spindle_test(self):
        def send_get_digital_spindle_info():
            self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
            Clock.schedule_once(lambda dt: show_digital_spindle_info(), 1)

        def show_digital_spindle_info():
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
            self.mains_value.text = str(self.m.s.digital_spindle_mains_voltage) + '/ ' + \
                                    str(self.m.s.spindle_mains_frequency_hertz)
            self.production_date_value.text = format_week_year(self.m.s.spindle_production_week,
                                                               self.m.s.spindle_production_year)
            self.up_time_value.text = format_seconds(self.m.s.spindle_total_run_time_seconds)
            self.firmware_version_value.text = str(self.m.s.spindle_firmware_version)
            self.brush_time_value.text = format_seconds(self.m.s.spindle_brush_run_time_seconds)

        def check_spindle_data_valid(rpm):
            def fail_test(message):
                self.fail_reasons.append([rpm, message])

            measured_rpm = int(self.m.s.spindle_speed)
            measured_voltage = self.m.s.digital_spindle_mains_voltage
            measured_temp = self.m.s.digital_spindle_temperature
            measured_kill_time = self.m.s.digital_spindle_kill_time
            measured_load = ld_qda_to_w(measured_voltage, self.m.s.digital_spindle_ld_qdA)

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
                if len(self.fail_reasons) == 0:
                    self.pass_fail_img.source = 'asmcnc/skavaUI/img/green_tick.png'
                else:
                    print("SPINDLE FAIL")
                    self.pass_fail_img.source = 'asmcnc/skavaUI/img/red_cross.png'

                    for item in self.fail_reasons:
                        print(str(item[0]) + ' RPM: ' + item[1])

            test_rpm(10000)
            Clock.schedule_once(lambda dt: test_rpm(13000), 6)
            Clock.schedule_once(lambda dt: test_rpm(19000), 12)
            Clock.schedule_once(lambda dt: test_rpm(22000), 18)
            Clock.schedule_once(lambda dt: test_rpm(25000), 24)
            Clock.schedule_once(lambda dt: stop_spindle(), 30)
            Clock.schedule_once(lambda dt: check_pass(), 30)

        send_get_digital_spindle_info()
        Clock.schedule_once(lambda dt: run_full_test(), 2)
