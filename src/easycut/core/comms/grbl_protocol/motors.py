'''
Class to hold the parameters for each individual motor
'''

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

class Motor(object):

    got_registers = False # this will update the first time that registers are read in
    got_calibration_coefficients = False

    def __init__(self, given_index):

        self.index = given_index # index of this motor in "all_units" dictionary
        self.reset_registers()

    def reset_registers(self):

        self.got_registers = False

        # REGISTERS
        self.shadowRegisters         = [0,0,0,0,0]    
        self.currentScale               = 0 #/* 0 - 31 where 31 is max */
        self.ActiveCurrentScale         = 0 #//set 1/4 of full scale
        self.standStillCurrentScale     = 0 #//set 1/4 of full scale
        self.stallGuardAlarmThreshold   = 0 # SG alarm threshold: when current SG reading is lower than calibrated by this value corresponded axis alarm will be triggered
        self.temperatureCoefficient     = 0 # correction for temperatures other than calibration
        self.max_step_period_us_SG      = 0 # maximum motor step size to read Stall guard. Higher step would lead to too low RPM and SG redings above that step size will be ignored


        self.SGdelta                    = -999 # distance from the current SG readins to calibrated SG value
        self.SGdeltaEMA                 = 0 # distance from the current SG readins to calibrated SG value

        self.SGdeltaAxis                = -999 # distance from the current SG readins to calibrated SG value, Average between two motors for each axis
        self.SGdelta_peak               = -999 # distance from the current SG readins to calibrated SG value
        self.SGdeltaAxis_peak           = -999 # distance from the current SG readins to calibrated SG value, Average between two motors for each axis
        self.M1M2Delta                  = 0 # squareness metric
        self.squareness                 = 0 # squareness metric


        self.isStandStillCurrent        = 0
        self.mStepCurrenValue           = 0
        self.coolStepCurrenValue        = 0
        self.stallGuardShortValue       = 0
        self.stallGuardCurrenValue      = 0
        self.StatusBits                 = 0
        self.DiagnosticBits             = 0

        self.motor_current              = 0
        self.microstep_resolution       = 0
        self.SGThreshold                = 0
        self.SGFilter                   = 0
        self.LowerSEThreshold           = 0
        self.UpperSEThreshold           = 0
        self.CurrentIncrementSpeed      = 0
        self.CurrentDecrementSpeed      = 0
        self.SEMinCurrent               = 0
        self.InterpolationEnabled       = 0
        self.HalfCurrent                = 0
        self.LowSideGateCurrent         = 0
        self.HighSideGateCurrent        = 0
        self.SlowDecayDuration          = 0
        self.BlankingTime               = 0
        self.HysteresisStartValue       = 0
        self.HysteresisEndValue         = 0
        self.HysteresisDecrementPeriod  = 0
        self.ChopperMode                = 0
        self.TOFFRandomisationEnabled   = 0
        self.MotorOFF                   = 0
        self.IdleCurrent                = 0


        # CALIBRATION PARAMS
        self.calibration_dataset_SG_values   = []
        self.calibrated_at_current_setting   = 0
        self.calibrated_at_sgt_setting       = 0
        self.calibrated_at_toff_setting      = 0
        self.calibrated_at_temperature       = 0

        self.got_calibration_coefficients    = False
    




