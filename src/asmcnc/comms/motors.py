'''
Class to hold the parameters for each individual motor
'''

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

class motor_class(object):

    got_registers              = False # this will update the first time that registers are read in

    index                      = 0 # index of this motor in "all_units" dictionary

    currentScale               = 0 #/* 0 - 31 where 31 is max */
    ActiveCurrentScale         = 0 #//set 1/4 of full scale
    standStillCurrentScale     = 0 #//set 1/4 of full scale
    stallGuardAlarmThreshold   = 0 # SG alarm threshold: when current SG reading is lower than calibrated by this value corresponded axis alarm will be triggered
    temperatureCoefficient     = 0 # correction for temperatures other than calibration
    max_step_period_us_SG      = 0 # maximum motor step size to read Stall guard. Higher step would lead to too low RPM and SG redings above that step size will be ignored
    SGdelta                    = -999 # distance from the current SG readins to calibrated SG value
    SGdeltaEMA                 = 0 # distance from the current SG readins to calibrated SG value

    SGdeltaAxis                = -999 # distance from the current SG readins to calibrated SG value, Average between two motors for each axis
    SGdelta_peak               = -999 # distance from the current SG readins to calibrated SG value
    SGdeltaAxis_peak           = -999 # distance from the current SG readins to calibrated SG value, Average between two motors for each axis
    M1M2Delta                  = 0 # squareness metric
    squareness                 = 0 # squareness metric


    isStandStillCurrent        = 0
    mStepCurrenValue           = 0
    coolStepCurrenValue        = 0
    stallGuardShortValue       = 0
    stallGuardCurrenValue      = 0
    StatusBits                 = 0
    DiagnosticBits             = 0

    motor_current              = 0
    microstep_resolution       = 0
    SGThreshold                = 0
    SGFilter                   = 0
    LowerSEThreshold           = 0
    UpperSEThreshold           = 0
    CurrentIncrementSpeed      = 0
    CurrentDecrementSpeed      = 0
    SEMinCurrent               = 0
    InterpolationEnabled       = 0
    HalfCurrent                = 0
    LowSideGateCurrent         = 0
    HighSideGateCurrent        = 0
    SlowDecayDuration          = 0
    BlankingTime               = 0
    HysteresisStartValue       = 0
    HysteresisEndValue         = 0
    HysteresisDecrementPeriod  = 0
    ChopperMode                = 0
    TOFFRandomisationEnabled   = 0
    MotorOFF                   = 0
    IdleCurrent                = 0

    shadowRegisters         = [0,0,0,0,0]

    def __init__(self, given_index):
        self.index = given_index
