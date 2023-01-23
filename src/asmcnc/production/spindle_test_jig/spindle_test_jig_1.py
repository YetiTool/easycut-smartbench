from math import ceil, sqrt

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.production.spindle_test_jig.popups.popup_confirm_shutdown import ConfirmShutdownPopup
# from asmcnc.production.spindle_test_jig.printer.receipt_printer import print_unlock_receipt
from asmcnc.skavaUI import widget_status_bar
from asmcnc.production.spindle_test_jig.spindle_test_jig_function import SpindleTest


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
    unlock_code_label:unlock_code_label

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
                        
                        Button:
                            id: unlock_code_label
                            text: 'Unlock Code:'
                            bold: True
                            background_color: [0.62, 0.12, 0.94, 1]
                            on_press: root.update_unlock_code()
                        
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
    unlock_code = None
    poll_for_spindle_info = None

    def __init__(self, **kwargs):
        super(SpindleTestJig1, self).__init__(**kwargs)

        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)
        self.poll_for_spindle_info = Clock.schedule_interval(lambda dt: self.get_spindle_info, 2)
        self.test = SpindleTest(screen_manager=self.sm, machine=self.m, screen=self)

    def generate_unlock_code(self):
        serial = self.m.s.spindle_serial_number

        serial += 42
        serial *= 10000
        serial = str(hex(serial))[2:]

        self.unlock_code = serial
        self.unlock_code_label.text = serial

    def print_receipt(self):
        # print_unlock_receipt(self.unlock_code)
        pass

    def stop(self):
        self.m.s.write_command('M3 S0')
        [unschedule(clock) for clock in self.test.clocks]
        self.run_test_button.disabled = False

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.m.s.write_command('M3 S0'), 1)

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except:
            pass

    def shutdown(self):
        ConfirmShutdownPopup()

    def toggle_run_button(self):
        if self.run_test_button.disabled:
            self.run_test_button.disabled = False
        else:
            self.run_test_button.disabled = True

    def update_spindle_feedback(self):
        self.voltage_value.text = str(self.m.s.digital_spindle_mains_voltage) + 'V'
        self.load_value.text = str(
            ceil(ld_qda_to_w(self.m.s.digital_spindle_mains_voltage, self.m.s.digital_spindle_ld_qdA))) + 'W'
        self.temp_value.text = str(self.m.s.digital_spindle_temperature) + 'C'
        self.kill_time_value.text = str(self.m.s.digital_spindle_kill_time) + 'S'
        self.measured_rpm_value.text = str(self.m.s.spindle_speed)

    def get_spindle_info(self):
        def show_spindle_info():
            def format_week_year(week, year):
                return str(week) + 'th wk ' + str(year)

            def format_seconds(seconds):
                try:
                    days = seconds // 86400
                    seconds = seconds % 86400
                    hours = seconds // 3600
                    seconds %= 3600
                    minutes = seconds // 60
                    seconds %= 60
                    return str(days) + 'd, ' + str(hours) + 'h, ' + str(minutes) + 'm, ' + str(seconds) + 's'
                except:
                    self.get_spindle_info()
                    return 'err'

            self.serial_number_value.text = str(self.m.s.spindle_serial_number)
            self.mains_value.text = ('230V' if self.m.s.spindle_mains_frequency_hertz == 50 else '120V') + '/ ' + \
                                           str(self.m.s.spindle_mains_frequency_hertz) + "Hz"
            self.production_date_value.text = format_week_year(self.m.s.spindle_production_week,
                                                                      self.m.s.spindle_production_year)
            self.up_time_value.text = format_seconds(self.m.s.spindle_total_run_time_seconds)
            self.firmware_version_value.text = str(self.m.s.spindle_firmware_version)
            self.brush_time_value.text = format_seconds(self.m.s.spindle_brush_run_time_seconds)
            self.update_unlock_code()

        self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
        Clock.schedule_once(lambda dt: show_spindle_info(), 1)

    def update_unlock_code(self):
        serial = self.m.s.spindle_serial_number

        serial += 42
        serial *= 10000
        serial = str(hex(serial))[2:]

        self.unlock_code_label.text = serial
        self.unlock_code = serial

    def open_console(self):
        self.sm.current = 'spindle_test_console'



