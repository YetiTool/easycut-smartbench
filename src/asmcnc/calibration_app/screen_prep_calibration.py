"""
Created on 12 December 2019
Screen to inform user of essential preparation before they continue calibrating

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from asmcnc.calibration_app import screen_measurement
Builder.load_string(
    """

<PrepCalibrationScreenClass>:

    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'vertical'
        padding: [0.025*app.width, 0.0416666666667*app.height]
        spacing: 0

        BoxLayout:
            orientation: 'horizontal'
            padding:0, 0
            spacing: 0.025*app.width
            size_hint_y: 0.2
        
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_y:0.9
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: True
                on_press: 
                    root.repeat_section()
                    
                BoxLayout:
                    padding: [0.00625*app.width, 0.0104166666667*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        font_size: str(0.025*app.width) + 'sp'
                        text: 'Go Back'

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_y:0.9
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: True
                on_press: 
                    root.skip_section()
                    
                BoxLayout:
                    padding: [0.00625*app.width, 0.0104166666667*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: str(0.025*app.width) + 'sp'
                        text: 'Skip section'
                        
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_y:0.9
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                background_normal: ''
                background_color: hex('#FFCDD2')
                on_press: 
                    root.quit_calibration()
                    
                BoxLayout:
                    padding: [0.00625*app.width, 0.0104166666667*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: str(0.025*app.width) + 'sp'
                        text: '[color=455A64]Quit calibration[/color]'
                        markup: True

        BoxLayout:
            orientation: 'horizontal'
            spacing: 0.0416666666667*app.height
            padding: [0.0125*app.width, 0.0208333333333*app.height]

            BoxLayout:
                orientation: 'vertical'
                spacing: 0
                size_hint_x: 1.3
                 
                Label:
                    size_hint_y: 0.2
                    font_size: str(0.04375*app.width) + 'sp'
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
                    text: '[color=000000]Essential preparation:[/color]'
                    markup: True

                ScrollView:
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_scroll_x: True
                    do_scroll_y: True
                    scroll_type: ['content']
                    
                    RstDocument:
                        text: root.preparation_list
                        background_color: hex('#FFFFFF')

            BoxLayout:
                orientation: 'vertical'
                # spacing: 10
                # padding: 10
                size_hint_x: 0.6

                Label:
                    text_size: self.size
                    font_size: str(0.0225*app.width) + 'sp'
                    halign: 'left'
                    valign: 'middle'
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    padding: [0.025*app.width, 0.0416666666667*app.height]
                    size_hint_y: 0.6
                    
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        background_normal: ''
                        background_color: hex('#C5E1A5')
                        disabled: False
                        on_press: 
                            root.next_screen()
                            
                        BoxLayout:
                            padding: [0.00625*app.width, 0.0104166666667*app.height]
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                font_size: str(0.025*app.width) + 'sp'
                                text: '[color=455A64]Home[/color]'
                                markup: True
                        
            
"""
    )


class PrepCalibrationScreenClass(Screen):
    preparation_list = """- Ensure that wheels and pinions are set by gently rocking each axis. See our YouTube video, [i]SmartBench: Walkthrough of Calibration Wizard[/i], for more information.
- Clear the machine - remove any material from the machine.
- Lower the X beam so that it is running on the bench.
- Clean all tracks and racks with a vacuum.
- Disconnect the vacuum hose from the Z-head.
- Prepare a calibrated tape measure (e.g. check the tape against a meter rule).
- When your machine is prepared, press "Home" to start the homing sequence."""

    def __init__(self, **kwargs):
        super(PrepCalibrationScreenClass, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']

    def quit_calibration(self):
        self.sm.get_screen('calibration_complete').calibration_cancelled = True
        self.sm.current = 'calibration_complete'

    def skip_section(self):
        if not self.sm.has_screen('measurement'):
            measurement_screen = screen_measurement.MeasurementScreenClass(name
                ='measurement', screen_manager=self.sm, machine=self.m)
            self.sm.add_widget(measurement_screen)
        self.sm.get_screen('measurement').axis = 'X'
        self.sm.current = 'measurement'

    def repeat_section(self):
        self.sm.current = 'calibration_landing'

    def next_screen(self):
        if not self.sm.has_screen('measurement'):
            measurement_screen = screen_measurement.MeasurementScreenClass(name
                ='measurement', screen_manager=self.sm, machine=self.m)
            self.sm.add_widget(measurement_screen)
        self.sm.get_screen('measurement').axis = 'X'
        self.m.request_homing_procedure('measurement', 'calibration_complete')
