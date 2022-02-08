# -*- coding: utf-8 -*-
### definitiions shared with C code

# /* protocol v2 Commands, refer to gdoc "Yeti-GRBL extended Protocol"*/

COMMAND_LENGTH_BYTES                = 1  # 1 byte command
RTL_V2_COMMAND_SIZE_MIN             = 4  # 5 bytes: len, seq, command, crc */
RTL_V2_COMMAND_SIZE_MAX             = 20 # 20 bytes: len, seq, command, data (0-16), crc */
SERIAL_NUMBER_LEN                   = 12
PRODUCT_VERSION_LEN                 = 8


SET_RGB_LED_STATE					= 1			 # Set the dust show light color in RGB 3 bytes format, Green would be “^\x01\x00\xFF\x00“
SET_SPINDLE_SPEED					= 2			 # Set spindle speed. Speed 0 would also turn off the spindle relay
SET_EXTRACTION_STATE				= 3			 # Enable or disable extraction. 1: enable, 0: disable.
SET_LASER_DATUM_STATE				= 4			 # Enable or disable laser datum. 1: enable, 0: disable.
SET_SERIAL_NUMBER					= 5			 # Store serial number to persistent memory
SET_PRODUCT_VERSION					= 6			 # Store product version to persistent memory
GET_SERIAL_NUMBER					= 7			 # Report serial number stored in persistent memory
GET_PRODUCT_VERSION					= 8			 # Report product number stored in persistent memory
GET_ALARM_REASON					= 9			 # Report latest alarm reason (which end switch triggered the alarm)
GET_DIGITAL_SPINDLE_INFO			= 10		 # Report Mafell digital spindle info: serial number, uptime, brush time, etc.
RESET_DIGITAL_SPINDLE_BRUSH_TIME	= 11		 # Reset brush timer in Mafell digital spindle
RESET_SEQUENCE_NUMBER				= 12		 # Reset protocol V2 sequence number to 0. Command would not generate sequence error even if expected sequence number does not match
TMC_COMMAND					        = 50		 # TMC command, see table xx

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

TMC_REG_CMD_LENGTH      = 4  #/* value */
TMC_GBL_CMD_LENGTH      = 1  #/* 1 byte command */