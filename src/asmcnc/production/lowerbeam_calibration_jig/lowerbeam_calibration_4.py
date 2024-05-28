import traceback
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
import re
from kivy.clock import Clock

Builder.load_string(
    """
<LBCalibration4>:
    serial_no_input:serial_no_input
    error_label:error_label
    ok_button : ok_button

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
            rows: 4

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
                text: '^ Enter LB serial number: ^'
                font_size: dp(50)

            Label:
                id: error_label
                font_size: dp(30)

            Button:
                id: ok_button
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.6
                disabled: False

"""
)


class LBCalibration4(Screen):
    serial_number = ""

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("sm")
        self.m = kwargs.pop("m")
        self.calibration_db = kwargs.pop("calibration_db")
        super(LBCalibration4, self).__init__(**kwargs)

    def enter_prev_screen(self):
        self.sm.current = "lbc2"

    def on_enter(self):
        self.ok_button.disabled = False

    def validate_serial_number(self, serial):
        expression = "(xl)\\d{4}"
        pattern = re.compile(expression)
        match = bool(pattern.match(serial))
        return match

    def enter_next_screen(self):
        self.ok_button.disabled = True
        self.ok_button.text = "Updating..."
        self.serial_number = self.serial_no_input.text.replace(" ", "").lower()
        validated = self.validate_serial_number(self.serial_number)
        if not validated:
            self.error_label.text = "Serial number invalid"
            self.ok_button.text = "OK"
            self.ok_button.disabled = False
            return
        Clock.schedule_once(self.prep_data_send, 0.2)

    def prep_data_send(self, dt):
        self.calibration_db.process_status_running_data_for_database_insert(
            self.m.measured_running_data(), self.serial_number
        )
        self.calibration_db.insert_calibration_check_stage(self.serial_number, 2)
        self.do_data_send_when_ready()
        self.calibration_db.set_up_connection()
        serial_number = self.serial_no_input.text.replace(" ", "").lower()
        validated = self.validate_serial_number(serial_number)

    def do_data_send_when_ready(self):
        if self.calibration_db.processing_running_data:
            Logger.info("Poll for sending LB QC statuses when ready")
            Clock.schedule_once(lambda dt: self.do_data_send_when_ready(), 1)
            return
        if self.calibration_db.send_data_through_publisher(self.serial_number, 13):
            try:
                self.send_calibration_payload(TMC_Y1, self.serial_number)
                self.send_calibration_payload(TMC_Y2, self.serial_number)
                next_screen_name = "lbc5"
            except Exception:
                next_screen_name = "lbc6"
                Logger.exception("Failed to send calibration payload!")
        else:
            next_screen_name = "lbc6"
        self.sm.get_screen(next_screen_name).set_serial_no(self.serial_number)
        self.ok_button.disabled = False
        self.ok_button.text = "OK"
        self.sm.current = next_screen_name

    def send_calibration_payload(self, motor_index, serial_number):
        stage = self.calibration_db.get_stage_id_by_description("CalibrationQC")
        sg_coefficients = self.m.TMC_motor[motor_index].calibration_dataset_SG_values
        cs = self.m.TMC_motor[motor_index].calibrated_at_current_setting
        sgt = self.m.TMC_motor[motor_index].calibrated_at_sgt_setting
        toff = self.m.TMC_motor[motor_index].calibrated_at_toff_setting
        temperature = self.m.TMC_motor[motor_index].calibrated_at_temperature
        coefficients = sg_coefficients + [cs] + [sgt] + [toff] + [temperature]
        self.calibration_db.setup_lower_beam_coefficients(
            serial_number, motor_index, stage
        )
        self.calibration_db.insert_calibration_coefficients(
            serial_number, motor_index, stage, coefficients
        )
