from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<LBCalibration4>:
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

            Label:
                id: main_label
                text: 'Enter LB serial number:'
                font_size: dp(50)
            
            GridLayout:
                cols: 1
                rows: 1

                padding: [200, 0]

                TextInput:
                    id: serial_no_input
                    font_size: dp(50)

            Button:
                id: main_button
                on_press: root.download_and_upload_LB_cal_data()
                text: 'Download'
                font_size: dp(30)
                size_hint_y: 0.6

""")

class LBCalibration4(Screen):
    def __init__(self, **kwargs):
        super(LBCalibration4, self).__init__(**kwargs)

        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['m']
        self.calibration_db = kwargs['calibration_db']

    def go_back(self):
        self.systemtools_sm.open_factory_settings_screen()

    def download_and_upload_LB_cal_data(self):

        self.main_label.text = "Getting data..."

        data = self.calibration_db.get_lower_beam_parameters(self.serial_no_input.text)

        self.save_calibration_data_to_motor(TMC_Y1, data)
        self.save_calibration_data_to_motor(TMC_Y2, data)

        self.main_label.text = "Uploading to ZH..."

        Clock.schedule_once(lambda dt: self.m.upload_Y_calibration_settings_from_motor_classes(), 1)

    def save_calibration_data_to_motor(self, motor_index, data):
        self.m.TMC_motor[motor_index].calibration_dataset_SG_values = ''
        self.m.TMC_motor[motor_index].calibrated_at_current_setting = ''
        self.m.TMC_motor[motor_index].calibrated_at_sgt_setting = ''
        self.m.TMC_motor[motor_index].calibrated_at_toff_setting = ''
        self.m.TMC_motor[motor_index].calibrated_at_temperature = ''

    def report_info_back_to_user_and_return(self):

        if not self.m.calibration_upload_in_progress:
            
            if self.m.calibration_upload_fail_info:
                self.main_label.text = self.m.calibration_upload_fail_info

            else:
                self.main_label = "Success!!"

            self.main_button.on_press = self.go_back()

# (4, u'test', 4, u'[454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 454, 456, 458, 458, 457, 460, 461, 463, 463, 463, 465, 466, 470, 470, 470, 471, 471, 472, 473, 473, 473, 475, 478, 478, 479, 480, 482, 481, 482, 482, 482, 482, 483, 482, 482, 482, 481, 481, 481, 480, 480, 479, 479, 478, 478, 478, 478, 477, 477, 474, 475, 473, 472, 473, 472, 472, 472, 471, 471, 470, 469, 468, 467, 465, 464, 459, 458, 440, 443, 449, 444, 452, 463, 458, 458, 457, 455, 456, 452, 452, 449, 449, 446, 445, 443, 441, 438, 437, 437, 436, 436, 433, 431, 432, 430, 430, 427, 429, 423, 423, 422, 419]', u'31', u'7', u'5', u'5187')




    # def enter_next_screen(self):
    #     try:
    #         self.calibration_db.send_calibration_payload(TMC_Y1)
    #         self.calibration_db.send_calibration_payload(TMC_Y2)
    #         self.sm.get_screen('lbc5').set_serial_no(self.serial_no_input.text)
    #         self.sm.current = 'lbc5'
    #     except:
    #         self.sm.get_screen('lbc6').set_serial_no(self.serial_no_input.text)
    #         self.sm.current = 'lbc6'

    # def send_calibration_payload(self, motor_index):
    #     sg_coefficients = self.m.TMC_motor[motor_index].calibration_dataset_SG_values
    #     cs = self.m.TMC_motor[motor_index].calibrated_at_current_setting
    #     sgt = self.m.TMC_motor[motor_index].calibrated_at_sgt_setting
    #     toff = self.m.TMC_motor[motor_index].calibrated_at_toff_setting
    #     temperature = self.m.TMC_motor[motor_index].calibrated_at_temperature
        
    #     self.calibration_db.send_z_head_calibration(self.serial_number, motor_index, sg_coefficients, cs, sgt, toff, temperature)