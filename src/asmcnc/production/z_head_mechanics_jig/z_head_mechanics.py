from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<ZHeadMechanics>:

    begin_test_button:begin_test_button

    test_progress_label:test_progress_label

    load_up_peak:load_up_peak
    load_down_peak:load_down_peak
    load_up_average:load_up_average
    load_down_average:load_down_average

    BoxLayout:
        orientation: 'vertical'
        padding: dp(5)
        spacing: dp(5)

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(5)

            Button:
                id: begin_test_button
                size_hint_x: 2
                text: 'Begin Test'
                bold: True
                font_size: dp(25)
                background_color: hex('#00C300FF')
                background_normal: ''
                on_press: root.begin_test()

            Button:
                text: 'STOP'
                bold: True
                font_size: dp(25)
                background_color: [1,0,0,1]
                background_normal: ''
                on_press: root.stop()

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(5)

            # Load value table
            GridLayout:
                size_hint_x: 4
                rows: 3
                cols: 3

                Label

                Label:
                    text: 'Up'

                Label:
                    text: 'Down'

                Label:
                    text: 'Peak load'

                Label:
                    id: load_up_peak
                    text: '-'

                Label:
                    id: load_down_peak
                    text: '-'

                Label:
                    text: 'Average load'

                Label:
                    id: load_up_average
                    text: '-'

                Label:
                    id: load_down_average
                    text: '-'

            Button:
                text: 'GCODE Monitor'
                bold: True
                font_size: dp(25)
                text_size: self.size
                valign: 'middle'
                halign: 'center'
                on_press: root.go_to_monitor()

        Label:
            size_hint_y: 2
            id: test_progress_label
            text: 'Waiting...'
            font_size: dp(30)
            markup: True
            bold: True
            text_size: self.size
            valign: 'middle'
            halign: 'center'

""")


# Copied PopupStop from popup_info but has additional reset_after_stop function call
class PopupStopTest(Widget):

    def __init__(self, machine, screen_manager, localization):
        
        self.m = machine
        self.m.soft_stop()

        self.sm = screen_manager
        self.l = localization
            
        def machine_reset(*args):
            self.sm.get_screen('mechanics').reset_after_stop()
            self.m.stop_from_soft_stop_cancel()

        def machine_resume(*args):
            self.m.resume_from_a_soft_door()
            
        stop_description = self.l.get_str("Is everything OK? You can resume the job, or cancel it completely.")
        resume_string = self.l.get_bold("Resume")
        cancel_string = self.l.get_bold("Cancel")
        title_string = self.l.get_str("Warning!")
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=stop_description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        resume_button = Button(text=resume_string, markup = True)
        resume_button.background_normal = ''
        resume_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        cancel_button = Button(text=cancel_string, markup = True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0], size_hint_y=2) 
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(resume_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                        title_color=[0, 0, 0, 1],
                        title_font= 'Roboto-Bold',
                        title_size = '20sp',
                        content=layout_plan,
                        size_hint=(None, None),
                        size=(400, 300),
                        auto_dismiss= False
                        )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        cancel_button.bind(on_press=machine_reset)
        cancel_button.bind(on_press=popup.dismiss)
        resume_button.bind(on_press=machine_resume)
        resume_button.bind(on_press=popup.dismiss)
        
        popup.open()


class ZHeadMechanics(Screen):

    sg_values_down = []
    sg_values_up = []

    def __init__(self, **kwargs):
        super(ZHeadMechanics, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']

    def begin_test(self):
        self.begin_test_button.disabled = True
        self.test_progress_label.text = 'Test running...\n[color=ff0000]WATCH FOR STALL THROUGHOUT ENTIRE TEST[/color]'

        self.load_up_peak.text = '-'
        self.load_down_peak.text = '-'
        self.load_up_average.text = '-'
        self.load_down_average.text = '-'

        self.m.send_command_to_motor("ENABLE MOTOR DRIVERS", command=SET_MOTOR_ENERGIZED, value=1)

    def stop(self):
        PopupStopTest(self.m, self.sm, self.l)

    def reset_after_stop(self):
        self.begin_test_button.disabled = False
        self.test_progress_label.text = 'Waiting...'

        self.m.send_command_to_motor("DISABLE MOTOR DRIVERS", command=SET_MOTOR_ENERGIZED, value=0)

        self.sg_values_down = []
        self.sg_values_up = []

    def go_to_monitor(self):
        self.sm.current = 'monitor'
