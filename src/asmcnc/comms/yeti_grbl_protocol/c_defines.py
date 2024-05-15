# -*- coding: utf-8 -*-
### definitiions shared with C code



# Controller types. 
TMC_X1                = 0
TMC_X2                = 1
TMC_Y1                = 2
TMC_Y2                = 3
TMC_Z                 = 4
TOTAL_TMCS            = 5

# host commands definitions */
CMD_RTL_V2            = 0x5E  #'^'   //BK Mod allow control of the TMC motor controllers while bypassing serial buffer
TMC_COMMAND_BIT_SIZE  = 5
MOTOR_OFFSET_MASK     = 0xF   #/* Motor offset mask must be a mask of contiguous zeroes, followed by contiguous sequence of ones: 000...111. */
MOTOR_OFFSET          = (MOTOR_OFFSET_MASK+1)     #/* Motor offset */

# first 16x5 positions are taken by individual motors commands:
DRVCTRL               = 0
CHOPCONF              = 1
SMARTEN               = 2
SGCSCONF              = 3
DRVCONF               = 4
REG_RESPONSE_LEN      = 1+5+5   # motor + Nregs + currentScale + StandStill + AlarmThreshold + Min 
TM_RESPONSE_LEN       = 6       # motor + stallGuardCurrentValue, coolStepCurrentValue, StatusBits, DiagnosticBits, mStepCurrentValue
SET_DRVCTRL           = DRVCTRL 
SET_CHOPCONF          = CHOPCONF
SET_SMARTEN           = SMARTEN 
SET_SGCSCONF          = SGCSCONF
SET_DRVCONF           = DRVCONF 
SET_IDLE_CURRENT      = 5  # set the current scale applied when no pulses are detected on the given axis
SET_ACTIVE_CURRENT    = 6  # set the active current scale 
SET_MOTOR_ENERGIZED   = 7  # energize or shut off the motor completely, for example to let user move turret easier 
SET_SG_ALARM_TRSHLD   = 8  # SG alarm threshold: when current SG reading is lower than calibrated by this value corresponded axis alarm will be triggered
SET_THERMAL_COEFF     = 9  # coefficient defining thermal offset applied to calibration curve
SET_MAX_SG_STEP_US    = 10 # maximum motor step size to read Stall guard. Higher step would lead to too low RPM and SG redings above that step size will be ignored

# common commands to be applied to whole system
SET_SG_ALARM          = 100  # desired stall behaviour: if "true" then stall guard value below the limit will trigger alarm
SET_CALIBR_MODE       = 101  # 1: reset all calibrations and prepare for new one, 2: complete calibration, compute , 3: print calibration coefficients
RESTORE_TMC_DEFAULTS  = 104  # restore all TMC default settings from flash - safety net in case parameters are completely bollocked 
STORE_TMC_PARAMS      = 105  # store existing (tuned) paraeters to the flash
GET_REGISTERS         = 106 
WDT_TMC_TEST          = 107  # value = 0x10: disable WD feed; other value: report EEPROM dump
REPORT_STALLS         = 108  # report list of last stalls with associated freeze frame
UPLOAD_CALIBR_VALUE   = 109  # upload calibration from host. Must be preceded by TMC_CALIBRATION_INIT_xxx 
REPORT_RAW_SG         = 110  # 1: report raw stall guard values for calibration purposes. default: 0; non-persistent

TMC_CALIBRATION_MODE_INIT = 1 # 1: reset all calibrations and prepare for new one, 
TMC_CALIBRATION_COMPUTE   = 2 # 2: complete calibration, compute cal tables and apply correction, 
TMC_CALIBRATION_REPORT    = 4 # 3: print calibration coefficients 
TMC_CALIBRATION_INIT_X    = 32  # initialise calibration for X axis only */
TMC_CALIBRATION_INIT_Y    = 64  # initialise calibration for Y axis only */
TMC_CALIBRATION_INIT_Z    = 128 #  initialise calibration for Z axis only */
TMC_CALIBRATION_INIT_ALL  = 16


#default values:
TMC_MAX_CURRENT     = 31
TMC_MED_CURRENT     = 15
SE_OFF              = 0
SE_DEFAULT          = 7

# must be size of TMC_SG_PROFILE_POINTS, can be put in PROGMEM  */
SG_step_periods_us =  [ 
    6250, # entry 1, speed=3.0rpm, feed=169.4mm/min */
    6036, # entry 2, speed=3.1rpm, feed=175.4mm/min */
    5829, # entry 3, speed=3.2rpm, feed=181.6mm/min */
    5630, # entry 4, speed=3.3rpm, feed=188.1mm/min */
    5437, # entry 5, speed=3.4rpm, feed=194.7mm/min */
    5251, # entry 6, speed=3.6rpm, feed=201.6mm/min */
    5071, # entry 7, speed=3.7rpm, feed=208.8mm/min */
    4898, # entry 8, speed=3.8rpm, feed=216.2mm/min */
    4730, # entry 9, speed=4.0rpm, feed=223.8mm/min */
    4568, # entry 10, speed=4.1rpm, feed=231.8mm/min */
    4412, # entry 11, speed=4.2rpm, feed=240.0mm/min */
    4261, # entry 12, speed=4.4rpm, feed=248.5mm/min */
    4115, # entry 13, speed=4.6rpm, feed=257.3mm/min */
    3974, # entry 14, speed=4.7rpm, feed=266.4mm/min */
    3838, # entry 15, speed=4.9rpm, feed=275.9mm/min */
    3707, # entry 16, speed=5.1rpm, feed=285.6mm/min */
    3580, # entry 17, speed=5.2rpm, feed=295.8mm/min */
    3458, # entry 18, speed=5.4rpm, feed=306.2mm/min */
    3339, # entry 19, speed=5.6rpm, feed=317.1mm/min */
    3225, # entry 20, speed=5.8rpm, feed=328.3mm/min */
    3115, # entry 21, speed=6.0rpm, feed=340.0mm/min */
    3008, # entry 22, speed=6.2rpm, feed=352.0mm/min */
    2905, # entry 23, speed=6.5rpm, feed=364.5mm/min */
    2806, # entry 24, speed=6.7rpm, feed=377.4mm/min */
    2710, # entry 25, speed=6.9rpm, feed=390.8mm/min */
    2617, # entry 26, speed=7.2rpm, feed=404.6mm/min */
    2527, # entry 27, speed=7.4rpm, feed=419.0mm/min */
    2441, # entry 28, speed=7.7rpm, feed=433.8mm/min */
    2357, # entry 29, speed=8.0rpm, feed=449.2mm/min */
    2277, # entry 30, speed=8.2rpm, feed=465.1mm/min */
    2199, # entry 31, speed=8.5rpm, feed=481.6mm/min */
    2123, # entry 32, speed=8.8rpm, feed=498.7mm/min */
    2051, # entry 33, speed=9.1rpm, feed=516.3mm/min */
    1980, # entry 34, speed=9.5rpm, feed=534.6mm/min */
    1913, # entry 35, speed=9.8rpm, feed=553.6mm/min */
    1847, # entry 36, speed=10.2rpm, feed=573.2mm/min */
    1784, # entry 37, speed=10.5rpm, feed=593.5mm/min */
    1723, # entry 38, speed=10.9rpm, feed=614.5mm/min */
    1664, # entry 39, speed=11.3rpm, feed=636.3mm/min */
    1607, # entry 40, speed=11.7rpm, feed=658.9mm/min */
    1552, # entry 41, speed=12.1rpm, feed=682.2mm/min */
    1499, # entry 42, speed=12.5rpm, feed=706.4mm/min */
    1448, # entry 43, speed=13.0rpm, feed=731.4mm/min */
    1398, # entry 44, speed=13.4rpm, feed=757.4mm/min */
    1350, # entry 45, speed=13.9rpm, feed=784.2mm/min */
    1304, # entry 46, speed=14.4rpm, feed=812.0mm/min */
    1259, # entry 47, speed=14.9rpm, feed=840.8mm/min */
    1216, # entry 48, speed=15.4rpm, feed=870.6mm/min */
    1175, # entry 49, speed=16.0rpm, feed=901.4mm/min */
    1134, # entry 50, speed=16.5rpm, feed=933.4mm/min */
    1096, # entry 51, speed=17.1rpm, feed=966.4mm/min */
    1058, # entry 52, speed=17.7rpm, feed=1000.7mm/min */
    1022, # entry 53, speed=18.3rpm, feed=1036.1mm/min */
    987,  # entry 54, speed=19.0rpm, feed=1072.9mm/min */
    953,  # entry 55, speed=19.7rpm, feed=1110.9mm/min */
    921,  # entry 56, speed=20.4rpm, feed=1150.3mm/min */
    889,  # entry 57, speed=21.1rpm, feed=1191.0mm/min */
    859,  # entry 58, speed=21.8rpm, feed=1233.2mm/min */
    829,  # entry 59, speed=22.6rpm, feed=1276.9mm/min */
    801,  # entry 60, speed=23.4rpm, feed=1322.2mm/min */
    773,  # entry 61, speed=24.2rpm, feed=1369.0mm/min */
    747,  # entry 62, speed=25.1rpm, feed=1417.6mm/min */
    721,  # entry 63, speed=26.0rpm, feed=1467.8mm/min */
    697,  # entry 64, speed=26.9rpm, feed=1519.8mm/min */
    673,  # entry 65, speed=27.9rpm, feed=1573.7mm/min */
    650,  # entry 66, speed=28.9rpm, feed=1629.4mm/min */
    628,  # entry 67, speed=29.9rpm, feed=1687.2mm/min */
    606,  # entry 68, speed=30.9rpm, feed=1747.0mm/min */
    585,  # entry 69, speed=32.0rpm, feed=1808.9mm/min */
    565,  # entry 70, speed=33.2rpm, feed=1873.0mm/min */
    546,  # entry 71, speed=34.3rpm, feed=1939.4mm/min */
    527,  # entry 72, speed=35.6rpm, feed=2008.1mm/min */
    509,  # entry 73, speed=36.8rpm, feed=2079.3mm/min */
    492,  # entry 74, speed=38.1rpm, feed=2153.0mm/min */
    475,  # entry 75, speed=39.5rpm, feed=2229.3mm/min */
    459,  # entry 76, speed=40.9rpm, feed=2308.3mm/min */
    443,  # entry 77, speed=42.3rpm, feed=2390.1mm/min */
    428,  # entry 78, speed=43.8rpm, feed=2474.8mm/min */
    413,  # entry 79, speed=45.4rpm, feed=2562.5mm/min */
    399,  # entry 80, speed=47.0rpm, feed=2653.3mm/min */
    385,  # entry 81, speed=48.7rpm, feed=2747.3mm/min */
    372,  # entry 82, speed=50.4rpm, feed=2844.7mm/min */
    359,  # entry 83, speed=52.2rpm, feed=2945.5mm/min */
    347,  # entry 84, speed=54.0rpm, feed=3049.9mm/min */
    335,  # entry 85, speed=55.9rpm, feed=3158.0mm/min */
    324,  # entry 86, speed=57.9rpm, feed=3269.9mm/min */
    313,  # entry 87, speed=60.0rpm, feed=3385.8mm/min */
    302,  # entry 88, speed=62.1rpm, feed=3505.7mm/min */
    292,  # entry 89, speed=64.3rpm, feed=3630.0mm/min */
    282,  # entry 90, speed=66.6rpm, feed=3758.6mm/min */
    272,  # entry 91, speed=68.9rpm, feed=3891.8mm/min */
    263,  # entry 92, speed=71.4rpm, feed=4029.8mm/min */
    254,  # entry 93, speed=73.9rpm, feed=4172.6mm/min */
    245,  # entry 94, speed=76.5rpm, feed=4320.4mm/min */
    237,  # entry 95, speed=79.2rpm, feed=4473.5mm/min */
    229,  # entry 96, speed=82.0rpm, feed=4632.1mm/min */
    221,  # entry 97, speed=84.9rpm, feed=4796.2mm/min */
    213,  # entry 98, speed=87.9rpm, feed=4966.2mm/min */
    206,  # entry 99, speed=91.1rpm, feed=5142.2mm/min */
    199,  # entry 100, speed=94.3rpm, feed=5324.4mm/min */
    192,  # entry 101, speed=97.6rpm, feed=5513.1mm/min */
    185,  # entry 102, speed=101.1rpm, feed=5708.5mm/min */
    179,  # entry 103, speed=104.7rpm, feed=5910.8mm/min */
    173,  # entry 104, speed=108.4rpm, feed=6120.3mm/min */
    167,  # entry 105, speed=112.2rpm, feed=6337.2mm/min */
    161,  # entry 106, speed=116.2rpm, feed=6561.8mm/min */
    156,  # entry 107, speed=120.3rpm, feed=6794.3mm/min */
    151,  # entry 108, speed=124.6rpm, feed=7035.1mm/min */
    145,  # entry 109, speed=129.0rpm, feed=7284.4mm/min */
    140,  # entry 110, speed=133.6rpm, feed=7542.6mm/min */
    136,  # entry 111, speed=138.3rpm, feed=7809.9mm/min */
    131,  # entry 112, speed=143.2rpm, feed=8086.7mm/min */
    126,  # entry 113, speed=148.3rpm, feed=8373.2mm/min */
    122,  # entry 114, speed=153.5rpm, feed=8670.0mm/min */
    118,  # entry 115, speed=159.0rpm, feed=8977.2mm/min */
    114,  # entry 116, speed=164.6rpm, feed=9295.4mm/min */
    110,  # entry 117, speed=170.4rpm, feed=9624.8mm/min */
    106,  # entry 118, speed=176.5rpm, feed=9965.9mm/min */
    103,  # entry 119, speed=182.7rpm, feed=10319.1mm/min */
    99,   #entry 120, speed=189.2rpm, feed=10684.8mm/min */
    96,   #entry 121, speed=195.9rpm, feed=11063.4mm/min */
    92,   #entry 122, speed=202.9rpm, feed=11455.5mm/min */
    89,   #entry 123, speed=210.0rpm, feed=11861.5mm/min */
    86,   #entry 124, speed=217.5rpm, feed=12281.9mm/min */
    83,   #entry 125, speed=225.2rpm, feed=12717.1mm/min */
    80,   #entry 126, speed=233.2rpm, feed=13167.8mm/min */
    78,   #entry 127, speed=241.4rpm, feed=13634.5mm/min */
    75,   #entry 128, speed=250.0rpm, feed=14117.6mm/min */
]           





TMC_REG_CMD_LENGTH      = 4  #/* value */
TMC_GBL_CMD_LENGTH      = 1  #/* 1 byte command */

#DRVCTRL 
MRES_MASK      = 0x0F
DEDGE_MASK     = 0x01
INTERPOL_MASK  = 0x01
MRES_SHIFT     = 0
DEDGE_SHIFT    = 8
INTERPOL_SHIFT = 9

                         
# TMC2590_CHOPCONF       
TOFF_MASK      = 0x0F
HSTRT_MASK     = 0x07
HEND_MASK      = 0x0F
HDEC_MASK      = 0x03
RNDTF_MASK     = 0x01
CHM_MASK       = 0x01
TBL_MASK       = 0x03
TOFF_SHIFT     = 0
HSTRT_SHIFT    = 4
HEND_SHIFT     = 7
HDEC_SHIFT     = 11
RNDTF_SHIFT    = 13
CHM_SHIFT      = 14
TBL_SHIFT      = 15
                         
# TMC2590_SMARTEN        
SEMIN_MASK     = 0x0F
SEUP_MASK      = 0x03
SEMAX_MASK     = 0x0F
SEDN_MASK      = 0x03
SEIMIN_MASK    = 0x01
SEMIN_SHIFT    = 0
SEUP_SHIFT     = 5
SEMAX_SHIFT    = 8
SEDN_SHIFT     = 13
SEIMIN_SHIFT   = 15                         
                         
# TMC2590_SGCSCONF       
CS_MASK        = 0x1F
SGT_MASK       = 0x7F
SFILT_MASK     = 0x01
CS_SHIFT       = 0
SGT_SHIFT      = 8
SFILT_SHIFT    = 16

# TMC2590_DRVCONF        
ENS2VS_MASK    = 0x01
SHRTSENS_MASK  = 0x01
RDSEL_MASK     = 0x03
VSENSE_MASK    = 0x01
SDOFF_MASK     = 0x01
TS2G_MASK      = 0x03
DISS2G_MASK    = 0x01
SLP2_MASK      = 0x01
SLPL_MASK      = 0x03
SLPH_MASK      = 0x03
TST_MASK       = 0x01
ENS2VS_SHIFT   = 0
SHRTSENS_SHIFT = 2
RDSEL_SHIFT    = 4
VSENSE_SHIFT   = 6
SDOFF_SHIFT    = 7
TS2G_SHIFT     = 8
DISS2G_SHIFT   = 10
SLP2_SHIFT     = 11
SLPL_SHIFT     = 12
SLPH_SHIFT     = 14
TST_SHIFT      = 16






SET_MRES              = 301   # Microstep resolution for STEP/DIR mode. Microsteps per fullstep: %0000: 256; %0001: 128; %0010: 64; %0011: 32; %0100: 16; %0101: 8; %0110: 4; %0111: 2 (halfstep); %1000: 1 (fullstep) */
SET_DEDGE             = 302   # 
SET_INTERPOL          = 303   # Enable STEP interpolation. 0: Disable STEP pulse interpolation. 1: Enable MicroPlyer STEP pulse multiplication by 16 */
SET_TOFF              = 304   # Off time/MOSFET disable. Duration of slow decay phase. If TOFF is 0, the MOSFETs are shut off. If TOFF is nonzero, slow decay time is a multiple of system clock periods: NCLK= 24 + (32 x TOFF) (Minimum time is 64clocks.), %0000: Driver disable, all bridges off, %0001: 1 (use wit30h TBL of minimum 24 clocks) %0010 … %1111: 2 … 15
SET_HSTRT             = 305   # Hysteresis start value, Hysteresis start offset from HEND: %000: 1 %100: 5; %001: 2 %101: 6; %010: 3 %110: 7; %011: 4 %111: 8; Effective: HEND+HSTRT must be ≤ 15
SET_HEND              = 306   # Hysteresis end (low) value; %0000 … %1111: Hysteresis is -3, -2, -1, 0, 1, …, 12 (1/512 of this setting adds to current setting) This is the hysteresis value which becomes used for the hysteresis chopper.
SET_HDEC              = 307   # Hysteresis decrement period setting, in system clock periods: %00: 16; %01: 32; %10: 48; %11: 64
SET_RNDTF             = 308   # Enable randomizing the slow decay phase duration: 0: Chopper off time is fixed as set by bits tOFF 1: Random mode, tOFF is random modulated by dNCLK= -12 - +3 clocks
SET_CHM               = 309   # Chopper mode. This mode bit affects the interpretation of the HDEC, HEND, and HSTRT parameters shown below. 0 Standard mode (SpreadCycle)
SET_TBL               = 310  # Blanking time. Blanking time interval, in system clock periods: %00: 16 %01: 24 %10: 36 %11: 54
SET_SEMIN             = 311  # Lower CoolStep threshold/CoolStep disable. If SEMIN is 0, CoolStep is disabled. If SEMIN is nonzero and the StallGuard2 value SG falls below SEMIN x 32, the CoolStep current scaling factor is increased */
SET_SEUP              = 312  # Current increment size. Number of current increment steps for each time that the StallGuard2 value SG is sampled below the lower threshold: %00: 1; %01: 2; %10: 4; %11: 8 */
SET_SEMAX             = 313  # Upper CoolStep threshold as an offset from the lower threshold. If the StallGuard2 measurement value SG is sampled equal to or above (SEMIN+SEMAX+1) x 32 enough times, then the coil current scaling factor is decremented. */
SET_SEDN              = 314  # Current decrement speed. Number of times that the StallGuard2 value must be sampled equal to or above the upper threshold for each decrement of the coil current: %00: 32; %01: 8; %10: 2; %11: 1 */
SET_SEIMIN            = 315  # Minimum CoolStep current: 0: 1/2 CS current setting; 1: 1/4 CS current setting */
SET_CS                = 316  # Current scale (scales digital currents A and B). Current scaling for SPI and STEP/DIR operation. 0-31: 1/32, 2/32, 3/32, ... 32/32;  . Example: CS=20 is 21/32 current. */                   
SET_SGT               = 317  # StallGuard2 threshold value. A lower value results in a higher sensitivity and less torque is required to indicate a stall.Range: -64 to +63 */
SET_SFILT             = 318  # StallGuard2 filter enable. 0: Standard mode, fastest response time. 1: Filtered mode, updated once for each four fullsteps to compensate for variation in motor construction, highest accuracy. */
SET_RDSEL             = 319  # 
SET_VSENSE            = 320  # Sense resistor voltage-based current scaling. 0: Full-scale sense resistor voltage is 325mV. 1: Full-scale sense resistor voltage is 173mV. (Full-scale refers to a current setting of 31.)
SET_SDOFF             = 321  # 
SET_TS2G              = 322  # 
SET_DISS2G            = 323  # 
SET_SLPL              = 324  # Slope control, low side, Gate driver strength 1 to 7. 7 is maximum current for fastest slopes
SET_SLPH              = 325  # Slope control, high side. Gate driver strength 1 to 7. 7 is maximum current for fastest slopes
SET_TST               = 326  # 
SET_CACB              = 327  # explicitly write phase currents to coils A and B

cmdMatrix = [
    [DRVCTRL    ,   SET_DRVCTRL     ,       MRES_MASK       ,       MRES_SHIFT      ],
    [DRVCTRL    ,   SET_DRVCTRL     ,       DEDGE_MASK      ,       DEDGE_SHIFT     ],
    [DRVCTRL    ,   SET_DRVCTRL     ,       INTERPOL_MASK   ,       INTERPOL_SHIFT  ],
    [CHOPCONF   ,   SET_CHOPCONF    ,       TOFF_MASK       ,       TOFF_SHIFT      ],
    [CHOPCONF   ,   SET_CHOPCONF    ,       HSTRT_MASK      ,       HSTRT_SHIFT     ],
    [CHOPCONF   ,   SET_CHOPCONF    ,       HEND_MASK       ,       HEND_SHIFT      ],
    [CHOPCONF   ,   SET_CHOPCONF    ,       HDEC_MASK       ,       HDEC_SHIFT      ],
    [CHOPCONF   ,   SET_CHOPCONF    ,       RNDTF_MASK      ,       RNDTF_SHIFT     ],
    [CHOPCONF   ,   SET_CHOPCONF    ,       CHM_MASK        ,       CHM_SHIFT       ],
    [CHOPCONF   ,   SET_CHOPCONF    ,       TBL_MASK        ,       TBL_SHIFT       ],
    [SMARTEN    ,   SET_SMARTEN     ,       SEMIN_MASK      ,       SEMIN_SHIFT     ],
    [SMARTEN    ,   SET_SMARTEN     ,       SEUP_MASK       ,       SEUP_SHIFT      ],
    [SMARTEN    ,   SET_SMARTEN     ,       SEMAX_MASK      ,       SEMAX_SHIFT     ],
    [SMARTEN    ,   SET_SMARTEN     ,       SEDN_MASK       ,       SEDN_SHIFT      ],
    [SMARTEN    ,   SET_SMARTEN     ,       SEIMIN_MASK     ,       SEIMIN_SHIFT    ],
    [SGCSCONF   ,   SET_DRVCTRL     ,       CS_MASK         ,       CS_SHIFT        ],
    [SGCSCONF   ,   SET_DRVCTRL     ,       SGT_MASK        ,       SGT_SHIFT       ],
    [SGCSCONF   ,   SET_DRVCTRL     ,       SFILT_MASK      ,       SFILT_SHIFT     ],
    [DRVCONF    ,   SET_DRVCONF     ,       ENS2VS_MASK     ,       ENS2VS_SHIFT    ],
    [DRVCONF    ,   SET_DRVCONF     ,       SHRTSENS_MASK   ,       SHRTSENS_SHIFT  ],
    [DRVCONF    ,   SET_DRVCONF     ,       RDSEL_MASK      ,       RDSEL_SHIFT     ],
    [DRVCONF    ,   SET_DRVCONF     ,       VSENSE_MASK     ,       VSENSE_SHIFT    ],
    [DRVCONF    ,   SET_DRVCONF     ,       SDOFF_MASK      ,       SDOFF_SHIFT     ],
    [DRVCONF    ,   SET_DRVCONF     ,       TS2G_MASK       ,       TS2G_SHIFT      ], 
    [DRVCONF    ,   SET_DRVCONF     ,       DISS2G_MASK     ,       DISS2G_SHIFT    ],
    [DRVCONF    ,   SET_DRVCONF     ,       SLP2_MASK       ,       SLP2_SHIFT      ],
    [DRVCONF    ,   SET_DRVCONF     ,       SLPL_MASK       ,       SLPL_SHIFT      ],
    [DRVCONF    ,   SET_DRVCONF     ,       SLPH_MASK       ,       SLPH_SHIFT      ],
    [DRVCONF    ,   SET_DRVCONF     ,       TST_MASK        ,       TST_SHIFT       ], 
    ]



# /* protocol v2 Commands, refer to gdoc "Yeti-GRBL extended Protocol"*/

COMMAND_LENGTH_BYTES                = 1  # 1 byte command
RTL_V2_COMMAND_SIZE_MIN             = 4  # 5 bytes: len, seq, command, crc */
RTL_V2_COMMAND_SIZE_MAX             = 20 # 20 bytes: len, seq, command, data (0-16), crc */
SERIAL_NUMBER_LEN                   = 12
PRODUCT_VERSION_LEN                 = 8


SET_RGB_LED_STATE					= 1			# Set the dust show light color in RGB 3 bytes format, Green would be “^\x01\x00\xFF\x00“
SET_SPINDLE_SPEED					= 2			# Set spindle speed. Speed 0 would also turn off the spindle relay
SET_EXTRACTION_STATE				= 3			# Enable or disable extraction. 1: enable, 0: disable.
SET_LASER_DATUM_STATE				= 4			# Enable or disable laser datum. 1: enable, 0: disable.
SET_SERIAL_NUMBER					= 5			# Store serial number to persistent memory
SET_PRODUCT_VERSION					= 6			# Store product version to persistent memory
GET_SERIAL_NUMBER					= 7			# Report serial number stored in persistent memory
GET_PRODUCT_VERSION					= 8			# Report product number stored in persistent memory
GET_ALARM_REASON					= 9			# Report latest alarm reason (which end switch triggered the alarm)
GET_DIGITAL_SPINDLE_INFO			= 10		# Report Mafell digital spindle info: serial number, uptime, brush time, etc.
RESET_DIGITAL_SPINDLE_BRUSH_TIME	= 11		# Reset brush timer in Mafell digital spindle
RESET_SEQUENCE_NUMBER				= 12		# Reset protocol V2 sequence number to 0. Command would not generate sequence error even if expected sequence number does not match
GET_STATISTICS                      = 13        # Report full GRBL run-time statistics: resets, uptime, travel time, stalls
TMC_COMMAND					        = 50		# TMC command, see table xx


# status string headers definitions for interfacing between GRBL and Console
SINGLE_MOTOR_HEX_RESP_LENGTH = 12       # hex bytes
STATUS_FS_IDENTIFIER    = '|FS:'        # feed and speed block
STATUS_PN_IDENTIFIER    = '|Pn:'        # end switches and other switches state
STATUS_BF_IDENTIFIER    = '|Bf:'        # UART buffer bytes and blocks status 
STATUS_LD_IDENTIFIER    = '|Ld:'        # spindle load block
STATUS_SP_IDENTIFIER    = '|Sp:'        # Mafell digital spindle statistics
STATUS_TC_IDENTIFIER    = '|TC:'        # Temperatures block
STATUS_TM_IDENTIFIER    = '|TM:'        # full TMC statistics report
STATUS_SG_IDENTIFIER    = '|SG:'        # Stall guard block
STATUS_VOL_IDENTIFIER   = '|V:'         # Voltages block
STATUS_TCAL_IDENTIFIER  = '|TCAL:'      # Calibration coefficients block
STATUS_TREG_IDENTIFIER  = '|TREG:'      # TMC registers and parameters state: DRVCTRL, CHOPCONF, SMARTEN, SGCSCONF, DRVCONF, activeCurrentScale, standStillCurrentScale, stallGuardAlarmThreshold, step_period_us_to_read_SG, gradient_per_Celsius
STATUS_STAT_IDENTIFIER  = '|STAT:'      # GRBL runtime statistics
STATUS_SGAL_IDENTIFIER  = '|SGALARM:'   # Stall guard stop statistics
STATUS_ALRM_IDENTIFIER  = '|Pa:'        # last Alarm reason
