from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from kivy.properties import ObjectProperty
import re
import traceback
from datetime import datetime
from kivy.clock import Clock

Builder.load_string("""
<UploadSerialNumbersScreen>:

    zhead_serial_input:zhead_serial_input
    lb_serial_input:lb_serial_input
    ub_serial_input:ub_serial_input
    console_serial_input:console_serial_input
    ybench_serial_input:ybench_serial_input
    spindle_serial_input:spindle_serial_input
    squareness_input:squareness_input
    main_button:main_button
    error_label:error_label

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        BoxLayout:
            size_hint_y: 0.1
            orientation: 'horizontal'

            Button:
                text: '<<< BACK'
                on_press: root.go_back()
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]
                size_hint_x: 0.5
                font_size: dp(20)

            BoxLayout:
                padding: [dp(10),0]
                size_hint_x: 0.5
                orientation: 'horizontal'

                Label:
                    text: 'Squareness'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    font_size: dp(25)

                TextInput:
                    id: squareness_input
                    font_size: dp(30)
                    multiline: False

        GridLayout:
            cols: 3
            rows: 2
            size_hint_y: 0.4

            
            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'ZHead Serial'
                    font_size: dp(25)

                TextInput:
                    id: zhead_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'LB Serial'
                    font_size: dp(25)

                TextInput:
                    id: lb_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'UB Serial'
                    font_size: dp(25)

                TextInput:
                    id: ub_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'Console Serial'
                    font_size: dp(25)

                TextInput:
                    id: console_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'YBench Serial'
                    font_size: dp(25)

                TextInput:
                    id: ybench_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'Spindle Serial'
                    font_size: dp(25)

                TextInput:
                    id: spindle_serial_input
                    font_size: dp(30)
                    multiline: False


                    
        Label:
            id: error_label
            text: 'Ensure all fields are entered accurately'
            font_size: dp(30)
            size_hint_y: 0.3

        Button:
            id: main_button
            on_press: root.validate_and_download()
            text: 'Download'
            font_size: dp(30)
            size_hint_y: 0.2
                

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class UploadSerialNumbersScreen(Screen):

    machine_serial_number = ''
    fw_version = ''
    sw_version = ''

    poll_for_end_of_upload = None

    dev_mode = True


    def __init__(self, **kwargs):
        super(UploadSerialNumbersScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['systemtools']
        self.m = kwargs['m']
        self.calibration_db = kwargs['calibration_db']
        self.set = kwargs['settings']

        if self.dev_mode:
            self.auto_generate_sns()

    def auto_generate_sns(self):

        self.zhead_serial_input.text = "zh0000"
        self.lb_serial_input.text = "xl0000"
        self.ub_serial_input.text = "xu0000"
        self.console_serial_input.text = "cs0000"
        self.ybench_serial_input.text = "yb0000"
        self.spindle_serial_input.text = "123456Y"
        self.squareness_input.text = "0.0"


    def on_enter(self):
        self.machine_serial_number = 'ys6' + str(self.m.serial_number()).split('.')[0]
        self.get_software_version_before_release()
        self.fw_version = self.get_truncated_fw_version(str(self.m.firmware_version()))

        if self.dev_mode:
            self.auto_generate_sns()
    
    def go_back(self):
        self.systemtools_sm.open_factory_settings_screen()


    def get_software_version_before_release(self):

        if self.set.sw_branch == 'ft' or self.dev_mode: self.sw_version = self.set.latest_sw_version
        else: self.sw_version = self.set.sw_version

    def validate_and_download(self):
        regex_check = self.check_valid_inputs_regex()
        valid_check = self.check_valid_inputs()
        version_check = self.check_versions_valid_regex()

        if not regex_check or not valid_check or not version_check:
            return

        ## LINK SERIAL NUMBERS IN DATABASE


        all_serial_numbers = [
                                self.machine_serial_number,
                                self.zhead_serial_input.text,
                                self.lb_serial_input.text,
                                self.ub_serial_input.text,
                                self.console_serial_input.text,
                                self.ybench_serial_input.text,
                                self.spindle_serial_input.text,
                                self.sw_version,
                                self.fw_version,
                                self.squareness_input.text
            ]

        self.calibration_db.insert_serial_numbers(*all_serial_numbers)

        ## DOWNLOAD LB CALIBRATION & UPLOAD TO Z HEAD
        self.download_and_upload_LB_cal_data()

        log("EVERYTHING CHECKED OUT!")
        self.error_label.text = "EVERYTHING CHECKED OUT!"

    def check_valid_inputs(self):
        validated = True

        if len(self.spindle_serial_input.text) < 7:
            self.error_label.text = 'Spindle serial invalid'
            validated = False

        if len(self.squareness_input.text) < 1:
            self.error_label.text = 'Squareness invalid'
            validated = False

        return validated

    def check_versions_valid_regex(self):

        fw_version_pattern = re.compile('\d[.]\d[.]\d')
        sw_version_pattern = re.compile('v\d[.]\d[.]\d')

        fw_match = bool(fw_version_pattern.match(self.fw_version))
        sw_match = bool(sw_version_pattern.match(self.sw_version))

        validated = True

        if not fw_match:
            self.error_label.text = "fw version invalid" 
            validated = False

        if not sw_match:
            self.error_label.text = "sw version invalid"  
            validated = False

        return validated

    def check_valid_inputs_regex(self):
        regex = '^({start})\d{4}$'

        machine_expression = regex.replace('{start}', 'ys6')
        zhead_expression = regex.replace('{start}', 'zh')
        lb_expression = regex.replace('{start}', 'xl')
        ub_expression = regex.replace('{start}', 'xu')
        console_expression = regex.replace('{start}', 'cs')
        ybench_expression = regex.replace('{start}', 'yb')

        machine_pattern = re.compile(machine_expression)
        zhead_pattern = re.compile(zhead_expression)
        lb_pattern = re.compile(lb_expression)
        ub_pattern = re.compile(ub_expression)
        console_pattern = re.compile(console_expression)
        ybench_pattern = re.compile(ybench_expression)

        machine_match = bool(machine_pattern.match(self.machine_serial_number))
        zhead_match = bool(zhead_pattern.match(self.zhead_serial_input.text))
        lb_match = bool(lb_pattern.match(self.lb_serial_input.text))
        ub_match = bool(ub_pattern.match(self.ub_serial_input.text))
        console_match = bool(console_pattern.match(self.console_serial_input.text))
        ybench_match = bool(ybench_pattern.match(self.ybench_serial_input.text))

        validated = True

        if not machine_match:
            self.error_label.text = 'Machine serial invalid'
            validated = False
        
        if not zhead_match:
            self.error_label.text = 'ZHead serial invalid'
            validated = False

        if not lb_match:
            self.error_label.text = 'LB serial invalid'
            validated = False
        
        if not ub_match:
            self.error_label.text = 'UB serial invalid'
            validated = False

        if not console_match:
            self.error_label.text = 'Console serial invalid'
            validated = False

        if not ybench_match:
            self.error_label.text = 'YBench serial invalid'
            validated = False

        return validated

    def get_truncated_fw_version(self, version):

        ver_lst = version.split('.')
        truncated_fw_version = ver_lst[0] + '.' + ver_lst[1] + '.' + ver_lst[2]
        return truncated_fw_version

    # CALIBRATION DATA DOWNLOAD & UPLOAD

    def download_and_upload_LB_cal_data(self):

        self.error_label.text = "Getting LB data..."

        stage_id = self.calibration_db.get_stage_id_by_description("CalibrationQC")

        try: 
            Y1_data = self.calibration_db.get_lower_beam_coefficents(self.lb_serial_input.text.replace(" ", "").lower(), TMC_Y1, stage_id)
            Y2_data = self.calibration_db.get_lower_beam_coefficents(self.lb_serial_input.text.replace(" ", "").lower(), TMC_Y2, stage_id)

            self.save_calibration_data_to_motor(TMC_Y1, Y1_data)
            self.save_calibration_data_to_motor(TMC_Y2, Y2_data)

            self.error_label.text = "Uploading to ZH..."

            Clock.schedule_once(lambda dt: self.m.upload_Y_calibration_settings_from_motor_classes(), 1)

            self.poll_for_end_of_upload = Clock.schedule_interval(self.report_info_back_to_user_and_return, 5)

        except:
            self.error_label.text = "Could not get data"
            print(traceback.format_exc())

    def save_calibration_data_to_motor(self, motor_index, data):

        self.m.TMC_motor[motor_index].calibration_dataset_SG_values = data["coefficients"]
        self.m.TMC_motor[motor_index].calibrated_at_current_setting = data["cs"]
        self.m.TMC_motor[motor_index].calibrated_at_sgt_setting = data["sgt"]
        self.m.TMC_motor[motor_index].calibrated_at_toff_setting = data["toff"]
        self.m.TMC_motor[motor_index].calibrated_at_temperature = data["temp"]

    def report_info_back_to_user_and_return(self, dt):

        if not self.m.calibration_upload_in_progress:

            Clock.unschedule(self.poll_for_end_of_upload)
            
            if self.m.calibration_upload_fail_info:
                self.main_label.text = self.m.calibration_upload_fail_info

            else:
                self.main_label.text = "Success!!"

    def on_leave(self):
        if self.poll_for_end_of_upload != None: Clock.unschedule(self.poll_for_end_of_upload)   

        
