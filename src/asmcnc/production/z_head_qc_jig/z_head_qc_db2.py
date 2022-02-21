from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

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
        sg_coefficients = self.m.TMC_MOTOR[motor_index].calibration_dataset_SG_values
        cs = self.m.TMC_MOTOR[motor_index].calibrated_at_current_setting
        sgt = self.m.TMC_MOTOR[motor_index].calibrated_at_sgt_setting
        toff = self.m.TMC_MOTOR[motor_index].calibrated_at_toff_setting
        temperature = self.m.TMC_motor[motor_index].calibrated_at_temperature
        
        self.calibration_db.send_z_head_calibration(self.serial_number, motor_index, sg_coefficients, cs, sgt, toff, temperature)

    def on_enter(self):
        try:
            self.send_calibration_payload(TMC_Z)
            self.send_calibration_payload(TMC_X1)
            self.send_calibration_payload(TMC_X2)
            self.sm.current = 'qcDB3'
        except:
            self.sm.current = 'qcDB4'

    def set_serial_number(self, serial_number):
        self.serial_number = serial_number

    def enter_next_screen(self, dt):
        self.sm.current = 'qcDB3'