from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from kivy.clock import Clock

Builder.load_string("""
<DownloadLBCalDataScreen>:
    serial_no_input : serial_no_input
    main_label : main_label
    main_button : main_button

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        Button:
            text: '<<< REPEAT CALIBRATION'
            on_press: root.enter_prev_screen()
            text_size: self.size
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            padding: [dp(10),0]
            size_hint_y: 0.2
            size_hint_x: 0.5
            font_size: dp(20)

        GridLayout:
            cols: 1
            rows: 3

            spacing: 50

            GridLayout:
                cols: 1
                rows: 1

                padding: [200, 0]

                TextInput:
                    id: serial_no_input
                    font_size: dp(50)
                    multiline: False
            Label:
                id: main_label
                text: '^ Enter LB serial number:^'
                font_size: dp(50)
            

            Button:
                id: main_button
                on_press: root.download_and_upload_LB_cal_data()
                text: 'Download'
                font_size: dp(30)
                size_hint_y: 0.6

""")

class DownloadLBCalDataScreen(Screen):
    def __init__(self, **kwargs):
        super(DownloadLBCalDataScreen, self).__init__(**kwargs)

        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['m']
        self.calibration_db = kwargs['calibration_db']

    def go_back(self):
        self.systemtools_sm.open_factory_settings_screen()

    def download_and_upload_LB_cal_data(self):

        self.main_label.text = "Getting data..."

        Y1_data = self.calibration_db.get_lower_beam_parameters(self.serial_no_input.text, TMC_Y1)
        Y2_data = self.calibration_db.get_lower_beam_parameters(self.serial_no_input.text, TMC_Y2)

        print(Y1_data)

        self.save_calibration_data_to_motor(TMC_Y1, Y1_data)
        self.save_calibration_data_to_motor(TMC_Y2, Y2_data)

        self.main_label.text = "Uploading to ZH..."

        Clock.schedule_once(lambda dt: self.m.upload_Y_calibration_settings_from_motor_classes(), 1)

    def save_calibration_data_to_motor(self, motor_index, data):



        self.m.TMC_motor[motor_index].calibration_dataset_SG_values = [int(i) for i in data[3].strip('[]').split(',')]
        self.m.TMC_motor[motor_index].calibrated_at_current_setting = int(data[4])
        self.m.TMC_motor[motor_index].calibrated_at_sgt_setting = int(data[5])
        self.m.TMC_motor[motor_index].calibrated_at_toff_setting = int(data[6])
        self.m.TMC_motor[motor_index].calibrated_at_temperature = int(data[7])

        print("FROM HERE")
        print(self.m.TMC_motor[motor_index].calibration_dataset_SG_values)
        print(self.m.TMC_motor[motor_index].calibrated_at_current_setting)
        print(self.m.TMC_motor[motor_index].calibrated_at_sgt_setting)
        print(self.m.TMC_motor[motor_index].calibrated_at_toff_setting)
        print(self.m.TMC_motor[motor_index].calibrated_at_temperature)



    def report_info_back_to_user_and_return(self):

        if not self.m.calibration_upload_in_progress:
            
            if self.m.calibration_upload_fail_info:
                self.main_label.text = self.m.calibration_upload_fail_info

            else:
                self.main_label = "Success!!"

            self.main_button.on_press = self.go_back()
