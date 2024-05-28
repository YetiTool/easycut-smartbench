"""
Class to hold the parameters for each individual motor
"""

from asmcnc.comms.yeti_grbl_protocol.c_defines import *


class motor_class(object):
    got_registers = False
    got_calibration_coefficients = False

    def __init__(self, given_index):
        self.index = given_index
        self.reset_registers()

    def reset_registers(self):
        self.got_registers = False
        self.shadowRegisters = [0, 0, 0, 0, 0]
        self.currentScale = 0
        self.ActiveCurrentScale = 0
        self.standStillCurrentScale = 0
        self.stallGuardAlarmThreshold = 0
        self.temperatureCoefficient = 0
        self.max_step_period_us_SG = 0
        self.SGdelta = -999
        self.SGdeltaEMA = 0
        self.SGdeltaAxis = -999
        self.SGdelta_peak = -999
        self.SGdeltaAxis_peak = -999
        self.M1M2Delta = 0
        self.squareness = 0
        self.isStandStillCurrent = 0
        self.mStepCurrenValue = 0
        self.coolStepCurrenValue = 0
        self.stallGuardShortValue = 0
        self.stallGuardCurrenValue = 0
        self.StatusBits = 0
        self.DiagnosticBits = 0
        self.motor_current = 0
        self.microstep_resolution = 0
        self.SGThreshold = 0
        self.SGFilter = 0
        self.LowerSEThreshold = 0
        self.UpperSEThreshold = 0
        self.CurrentIncrementSpeed = 0
        self.CurrentDecrementSpeed = 0
        self.SEMinCurrent = 0
        self.InterpolationEnabled = 0
        self.HalfCurrent = 0
        self.LowSideGateCurrent = 0
        self.HighSideGateCurrent = 0
        self.SlowDecayDuration = 0
        self.BlankingTime = 0
        self.HysteresisStartValue = 0
        self.HysteresisEndValue = 0
        self.HysteresisDecrementPeriod = 0
        self.ChopperMode = 0
        self.TOFFRandomisationEnabled = 0
        self.MotorOFF = 0
        self.IdleCurrent = 0
        self.calibration_dataset_SG_values = []
        self.calibrated_at_current_setting = 0
        self.calibrated_at_sgt_setting = 0
        self.calibrated_at_toff_setting = 0
        self.calibrated_at_temperature = 0
        self.got_calibration_coefficients = False
