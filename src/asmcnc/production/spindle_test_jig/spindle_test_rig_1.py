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


class SpindleTestRig1(Screen):
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

    def on_pass(self):
        self.pass_fail_img.source = 'asmcnc/skavaUI/img/green_tick.png'

    def run_spindle_test(self):
        def send_get_digital_spindle_info():
            self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")

        def confirm_digital_spindle_info():
            pass

        send_get_digital_spindle_info()
