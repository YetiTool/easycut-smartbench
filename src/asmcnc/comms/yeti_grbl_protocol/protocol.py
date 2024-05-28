# Class protocol_v2 implements interface communications between host and GRBL as defined in YETI-GRBL real time protocol V2
# all functions in this class return byte string to be sent to GRBL as is.
# No change shall be made to the byte_command, no end of line is required: use write_realtime()


import logging

import crc8
from asmcnc.comms.yeti_grbl_protocol.c_defines import *


class protocol_v2(object):
    def __init__(self):
        self.sequence_number = 0  # Sequence number. 1 byte incremental number. This number is increased at a rate of one for each new packet. Wraps to 0 after 255. Purpose of this field is to catch lost packets. This is one of the simple ways to handle errors in communications systems without acknowledgement.
        self.first_seq_after_boot = 1  # handshake flag, used to reset sequence number at host boot to avoid ASMCNC_RTL_SEQ_ERROR for the first packet

    def construct_rtl_v2_packet(self, command=255, data=[], printlog=False):
        # function returns byte string to be sent to GRBL as is.
        # No change shall be made to the byte_command, no end of line is required: use write_realtime()

        byte_command = b""

        # handshake: reset seq first time after boot
        if self.first_seq_after_boot == 1:
            self.first_seq_after_boot = 0
            byte_command = self._construct_first_rtl_v2_packet()

        packet_length = RTL_V2_COMMAND_SIZE_MIN + len(data)

        if packet_length <= RTL_V2_COMMAND_SIZE_MAX:
            hash = crc8.crc8()  # init crc8

            byte_array = (
                packet_length.to_bytes(1, "big")
                + self.sequence_number.to_bytes(1, "big")
                + command.to_bytes(1, "big")
                + data
            )

            hash.update(byte_array)  # compute crc8 : update crc8 hash

            # construct command as a byte array
            byte_command += bytes([CMD_RTL_V2]) + byte_array + hash.digest()

            if printlog:
                logging.info(
                    "sending command :" + str(command) + ", val:" + str(data)
                )  # implement as a queue to fix this error
                logging.info(str([hex(b) for b in byte_command]))

        else:
            # throw an error, command is not valid
            logging.info(
                "ERROR: unknown RTL command "
                + ", cmd:"
                + str(command)
                + ", val:"
                + str(data)
            )  # implement as a queue to fix this error

        # increment and wrap seq
        self.sequence_number += 1
        if self.sequence_number >= 256:
            self.sequence_number = 0

        # return constructed command
        return byte_command

    # Reset protocol V2 sequence number to 0. Command would not generate sequence error even if expected sequence number does not match
    def _construct_first_rtl_v2_packet(self):
        command = RESET_SEQUENCE_NUMBER
        byte_array = b""  # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    # Set the dust show light color in RGB 3 bytes format, Green would be “^\x01\x00\xFF\x00“
    def RGB_LED(self, R, G, B):
        command = SET_RGB_LED_STATE
        byte_array = R.to_bytes(1, "big") + G.to_bytes(1, "big") + B.to_bytes(1, "big")
        return self.construct_rtl_v2_packet(command, byte_array)

    # Enable or disable extraction. 1: enable, 0: disable.
    def SetExtractorState(self, ExtractorState):
        command = SET_EXTRACTION_STATE
        if ExtractorState > 1:
            ExtractorState = 1
        byte_array = ExtractorState.to_bytes(1, "big")
        return self.construct_rtl_v2_packet(command, byte_array)

    # Set spindle speed. Speed 0 would also turn off the spindle relay
    def SetSpindleSpeed(self, SpindleSpeed):
        command = SET_SPINDLE_SPEED
        data_length = 2
        if SpindleSpeed > 65000:
            SpindleSpeed = 65000
        u16_data = SpindleSpeed
        byte_array = b""
        for idx in range(data_length):
            byte_array = byte_array + ((u16_data >> idx * 8) & 0xFF).to_bytes(1, "big")
        return self.construct_rtl_v2_packet(command, byte_array)

    # Enable or disable laser datum. 1: enable, 0: disable.
    def SetLaserDatumState(self, LaserDatumState):
        command = SET_LASER_DATUM_STATE
        if LaserDatumState > 1:
            LaserDatumState = 1
        byte_array = LaserDatumState.to_bytes(1, "big")
        return self.construct_rtl_v2_packet(command, byte_array)

    # Report latest alarm reason (which end switch triggered the alarm)
    def GetAlarmLimitsState(self):
        command = GET_ALARM_REASON
        byte_array = b""  # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    # Store serial number to persistent memory
    def SetZHSerialNumber(self, SerialNumber):
        # serial number could contain numbers or characters. total lenght is ZH_SERIAL_NUMBER_LEN bytes. longer sting will be truncated. Shorter string will be preceded with '0's
        command = SET_ZH_SERIAL_NUMBER
        data_length = ZH_SERIAL_NUMBER_LEN

        # truncate
        if len(SerialNumber) > data_length:
            SerialNumber = SerialNumber[(len(SerialNumber) - data_length) :]

        # append spaces
        if len(SerialNumber) < data_length:
            SerialNumber = " " * (data_length - len(SerialNumber)) + SerialNumber

        byte_array = str.encode(SerialNumber)

        return self.construct_rtl_v2_packet(command, byte_array)

    # Store product version to persistent memory
    def SetLBSerialNumber(self, LBSerialNumber):
        # product number could contain numbers or characters. total lenght is LB_SERIAL_NUMBER_LEN bytes. longer sting will be truncated. Shorter string will be preceded with '0's
        command = SET_LB_SERIAL_NUMBER
        data_length = LB_SERIAL_NUMBER_LEN

        # truncate
        if len(LBSerialNumber) > data_length:
            LBSerialNumber = LBSerialNumber[(len(LBSerialNumber) - data_length) :]

        # append spaces
        if len(LBSerialNumber) < data_length:
            LBSerialNumber = " " * (data_length - len(LBSerialNumber)) + LBSerialNumber

        byte_array = str.encode(LBSerialNumber)

        return self.construct_rtl_v2_packet(command, byte_array)

    # Report serial number stored in persistent memory
    def GetSerialNumbers(self):
        command = GET_SERIAL_NUMBERS
        byte_array = b""  # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    # Report Mafell digital spindle info: serial number, uptime, brush time, etc.
    def GetDigitalSpindleInfo(self):
        command = GET_DIGITAL_SPINDLE_INFO
        byte_array = b""  # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    # Reset brush timer in Mafell digital spindle
    def ResetDigitalSpindleBrushTime(self):
        command = RESET_DIGITAL_SPINDLE_BRUSH_TIME
        byte_array = b""  # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    # Report full GRBL run-time statistics: resets, uptime, travel time, stalls
    def GetStatistics(self):
        command = GET_STATISTICS
        byte_array = b""  # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    # set arbitrary feed override
    def SetFeedOverride(self, FeedOverrideValue):
        command = SET_FEED_OVERRIDE
        if (FeedOverrideValue <= 0xFF) and (FeedOverrideValue > 0):
            byte_array = FeedOverrideValue.to_bytes(1, "big")
        elif FeedOverrideValue <= 0xFFFF:
            byte_array = FeedOverrideValue.to_bytes(2, "big")
        else:
            return  # value is too large for two bytes
        return self.construct_rtl_v2_packet(command, byte_array)

    # set arbitrary Spindle override
    def SetSpindleOverride(self, SpindleOverrideValue):
        command = SET_SPINDLE_OVERRIDE
        if (SpindleOverrideValue <= 0xFF) and (SpindleOverrideValue > 0):
            byte_array = SpindleOverrideValue.to_bytes(1, "big")
        elif SpindleOverrideValue <= 0xFFFF:
            byte_array = SpindleOverrideValue.to_bytes(2, "big")
        else:
            return  # value is too large for two bytes
        return self.construct_rtl_v2_packet(command, byte_array)

    # TMC command, see table xx
    def constructTMCcommand(self, cmd, data, len):
        command = TMC_COMMAND
        data_length = len
        byte_array = cmd.to_bytes(1, "big")  # first byte of data is TMC command
        for idx in range(data_length):
            byte_array = byte_array + ((data >> idx * 8) & 0xFF).to_bytes(1, "big")

        return self.construct_rtl_v2_packet(command, byte_array)
