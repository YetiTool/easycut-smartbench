from asmcnc.comms.logging_system.logging_system import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
import traceback

Builder.load_string("""
<ZHeadQCDB2>:

    Label:
        text: 'Updating database...'
        font_size: dp(50)

""")

class ZHeadQCDB2(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQCDB2, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.calibration_db = kwargs['calibration_db']

    def send_calibration_payload(self, motor_index):
        self.calibration_db.set_up_connection()

        stage = self.calibration_db.get_stage_id_by_description('CalibrationQC')

        sg_coefficients = self.m.TMC_motor[motor_index].calibration_dataset_SG_values
        cs = self.m.TMC_motor[motor_index].calibrated_at_current_setting
        sgt = self.m.TMC_motor[motor_index].calibrated_at_sgt_setting
        toff = self.m.TMC_motor[motor_index].calibrated_at_toff_setting
        temperature = self.m.TMC_motor[motor_index].calibrated_at_temperature

        coefficients = sg_coefficients + [cs] + [sgt] + [toff] + [temperature]

        self.calibration_db.setup_z_head_coefficients(self.serial_number, motor_index, stage)
        self.calibration_db.insert_calibration_coefficients(self.serial_number, motor_index, stage, coefficients)

    def on_enter(self):
        Clock.schedule_once(self.prep_data_send, 0.2)

    def prep_data_send(self, dt):

        self.calibration_db.process_status_running_data_for_database_insert(self.m.measured_running_data(), self.serial_number)
        self.calibration_db.insert_calibration_check_stage(self.serial_number, 12)
        self.do_data_send_when_ready()

    def do_data_send_when_ready(self):

        if self.calibration_db.processing_running_data:
            Logger.info("Poll for sending ZH QC statuses when ready")
            Clock.schedule_once(lambda dt: self.do_data_send_when_ready(), 1)
            return

        if self.calibration_db.send_data_through_publisher(self.serial_number, 12):

            try:
                self.send_calibration_payload(TMC_Z)
                self.send_calibration_payload(TMC_X1)
                self.send_calibration_payload(TMC_X2)
                self.sm.current = 'qcDB3'
                return

            except:
                Logger.exception('Failed to send calibration payload!')

        self.sm.current = 'qcDB4'

    def set_serial_no(self, serial_number):
        self.serial_number = serial_number

    def enter_next_screen(self, dt):
        self.sm.current = 'qcDB3'
