from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.comms.yeti_grbl_protocol import crc8
import logging, struct


class protocol_v2(object):

    def __init__(self):
        self.sequence_number = 0
        self.first_seq_after_boot = 1

    def custom_int_to_bytes(self, thing_to_convert):
        return struct.pack('>B', thing_to_convert)

    def construct_rtl_v2_packet(self, command=255, data=[], printlog=False):
        byte_command = ''
        if self.first_seq_after_boot == 1:
            self.first_seq_after_boot = 0
            byte_command = self._construct_first_rtl_v2_packet()
        packet_length = RTL_V2_COMMAND_SIZE_MIN + len(data)
        if packet_length <= RTL_V2_COMMAND_SIZE_MAX:
            hash = crc8.crc8()
            byte_array = self.custom_int_to_bytes(packet_length
                ) + self.custom_int_to_bytes(self.sequence_number
                ) + self.custom_int_to_bytes(command) + data
            hash.update(byte_array)
            byte_command += bytearray([CMD_RTL_V2]) + byte_array + hash.digest(
                )
            if printlog:
                logging.info('sending command :' + str(command) + ', val:' +
                    str(data))
                logging.info(str([hex(b) for b in byte_command]))
        else:
            logging.info('ERROR: unknown RTL command ' + ', cmd:' + str(
                command) + ', val:' + str(data))
        self.sequence_number += 1
        if self.sequence_number >= 256:
            self.sequence_number = 0
        return byte_command

    def _construct_first_rtl_v2_packet(self):
        command = RESET_SEQUENCE_NUMBER
        byte_array = ''
        return self.construct_rtl_v2_packet(command, byte_array)

    def RGB_LED(self, R, G, B):
        command = SET_RGB_LED_STATE
        byte_array = self.custom_int_to_bytes(R) + self.custom_int_to_bytes(G
            ) + self.custom_int_to_bytes(B)
        return self.construct_rtl_v2_packet(command, byte_array)

    def SetExtractorState(self, ExtractorState):
        command = SET_EXTRACTION_STATE
        if ExtractorState > 1:
            ExtractorState = 1
        byte_array = self.custom_int_to_bytes(ExtractorState)
        return self.construct_rtl_v2_packet(command, byte_array)

    def SetSpindleSpeed(self, SpindleSpeed):
        command = SET_SPINDLE_SPEED
        data_length = 2
        if SpindleSpeed > 65000:
            SpindleSpeed = 65000
        u16_data = SpindleSpeed
        byte_array = ''
        for idx in range(data_length):
            byte_array = byte_array + self.custom_int_to_bytes(u16_data >> 
                idx * 8 & 255)
        return self.construct_rtl_v2_packet(command, byte_array)

    def SetLaserDatumState(self, LaserDatumState):
        command = SET_LASER_DATUM_STATE
        if LaserDatumState > 1:
            LaserDatumState = 1
        byte_array = self.custom_int_to_bytes(LaserDatumState)
        return self.construct_rtl_v2_packet(command, byte_array)

    def GetAlarmLimitsState(self):
        command = GET_ALARM_REASON
        byte_array = ''
        return self.construct_rtl_v2_packet(command, byte_array)

    def SetSerialNumber(self, SerialNumber):
        command = SET_SERIAL_NUMBER
        data_length = SERIAL_NUMBER_LEN
        if len(SerialNumber) > data_length:
            SerialNumber = SerialNumber[len(SerialNumber) - data_length:]
        if len(SerialNumber) < data_length:
            SerialNumber = '0' * (data_length - len(SerialNumber)
                ) + SerialNumber
        byte_array = str.encode(SerialNumber)
        return self.construct_rtl_v2_packet(command, byte_array)

    def SetProductVersion(self, ProductVersion):
        command = SET_PRODUCT_VERSION
        data_length = PRODUCT_VERSION_LEN
        if len(ProductVersion) > data_length:
            ProductVersion = ProductVersion[len(ProductVersion) - data_length:]
        if len(ProductVersion) < data_length:
            ProductVersion = '0' * (data_length - len(ProductVersion)
                ) + ProductVersion
        byte_array = str.encode(ProductVersion)
        return self.construct_rtl_v2_packet(command, byte_array)

    def GetSerialNumber(self):
        command = GET_SERIAL_NUMBER
        byte_array = ''
        return self.construct_rtl_v2_packet(command, byte_array)

    def GetProductVersion(self):
        command = GET_PRODUCT_VERSION
        byte_array = ''
        return self.construct_rtl_v2_packet(command, byte_array)

    def GetDigitalSpindleInfo(self):
        command = GET_DIGITAL_SPINDLE_INFO
        byte_array = ''
        return self.construct_rtl_v2_packet(command, byte_array)

    def ResetDigitalSpindleBrushTime(self):
        command = RESET_DIGITAL_SPINDLE_BRUSH_TIME
        byte_array = ''
        return self.construct_rtl_v2_packet(command, byte_array)

    def GetStatistics(self):
        command = GET_STATISTICS
        byte_array = ''
        return self.construct_rtl_v2_packet(command, byte_array)

    def constructTMCcommand(self, cmd, data, len):
        command = TMC_COMMAND
        data_length = len
        byte_array = self.custom_int_to_bytes(cmd)
        for idx in range(data_length):
            byte_array = byte_array + self.custom_int_to_bytes(data >> idx *
                8 & 255)
        return self.construct_rtl_v2_packet(command, byte_array)
