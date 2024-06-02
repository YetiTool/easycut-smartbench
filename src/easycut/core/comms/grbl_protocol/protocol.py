# -*- coding: utf-8 -*-
# Class protocol_v2 implements interface communications between host and GRBL as defined in YETI-GRBL real time protocol V2
# all functions in this class return byte string to be sent to GRBL as is. 
# No change shall be made to the byte_command, no end of line is required: use write_realtime()


from asmcnc.comms.yeti_grbl_protocol.c_defines import *  # definitions common between FW and console SW
from asmcnc.comms.yeti_grbl_protocol import crc8
import logging, struct


class protocol_v2(object):

    def __init__(self):
        self.sequence_number = 0        # Sequence number. 1 byte incremental number. This number is increased at a rate of one for each new packet. Wraps to 0 after 255. Purpose of this field is to catch lost packets. This is one of the simple ways to handle errors in communications systems without acknowledgement.
        self.first_seq_after_boot = 1   # handshake flag, used to reset sequence number at host boot to avoid ASMCNC_RTL_SEQ_ERROR for the first packet

    # Python 2.7 int type doesn't have to_bytes function in built, so have to make one. 
    # This will convert into "big" endian size 1 bytes.
    def custom_int_to_bytes(self, thing_to_convert):
        return struct.pack('>B', thing_to_convert)

    def construct_rtl_v2_packet(self, command = 255, data = [], printlog=False):     
        # function returns byte string to be sent to GRBL as is. 
        # No change shall be made to the byte_command, no end of line is required: use write_realtime()

        byte_command = b''

        #handshake: reset seq first time after boot
        if self.first_seq_after_boot == 1:
            self.first_seq_after_boot = 0
            byte_command = self._construct_first_rtl_v2_packet()

        packet_length = RTL_V2_COMMAND_SIZE_MIN + len(data)

        if packet_length <= RTL_V2_COMMAND_SIZE_MAX: 
            
            hash = crc8.crc8() # init crc8
            
            byte_array = self.custom_int_to_bytes(packet_length) + self.custom_int_to_bytes(self.sequence_number) + self.custom_int_to_bytes(command) + data            

            hash.update(byte_array)# compute crc8 : update crc8 hash
            
            # construct command as a byte array
            byte_command += bytearray([CMD_RTL_V2]) + byte_array + hash.digest()

            if printlog: 
                logging.info("sending command :" + str(command) + ", val:" + str(data)) #implement as a queue to fix this error
                logging.info(str([hex(b) for b in byte_command]))

        else:
            # throw an error, command is not valid
            logging.info("ERROR: unknown RTL command " + ", cmd:" + str(command) + ", val:" + str(data)) #implement as a queue to fix this error


        # increment and wrap seq
        self.sequence_number +=1
        if self.sequence_number >= 256:
            self.sequence_number = 0

        # return constructed command
        return byte_command


    # Reset protocol V2 sequence number to 0. Command would not generate sequence error even if expected sequence number does not match
    def _construct_first_rtl_v2_packet(self):
        command = RESET_SEQUENCE_NUMBER
        byte_array = b'' # empty data
        return self.construct_rtl_v2_packet(command, byte_array)


    # Set the dust show light color in RGB 3 bytes format, Green would be “^\x01\x00\xFF\x00“
    def RGB_LED(self, R, G, B):
        command = SET_RGB_LED_STATE
        byte_array = self.custom_int_to_bytes(R) + self.custom_int_to_bytes(G) + self.custom_int_to_bytes(B)
        return self.construct_rtl_v2_packet(command, byte_array)


    # Enable or disable extraction. 1: enable, 0: disable.
    def SetExtractorState(self, ExtractorState):
        command = SET_EXTRACTION_STATE
        if (ExtractorState>1):
            ExtractorState = 1
        byte_array = self.custom_int_to_bytes(ExtractorState) 
        return self.construct_rtl_v2_packet(command, byte_array)


    # Set spindle speed. Speed 0 would also turn off the spindle relay
    def SetSpindleSpeed(self, SpindleSpeed):
        command = SET_SPINDLE_SPEED
        data_length = 2
        if (SpindleSpeed>65000):
            SpindleSpeed = 65000
        u16_data = SpindleSpeed
        byte_array = b''
        for idx in range(data_length):
            byte_array = byte_array + self.custom_int_to_bytes(((u16_data >> idx*8) & 0xff))
        return self.construct_rtl_v2_packet(command, byte_array)


    # Enable or disable laser datum. 1: enable, 0: disable.
    def SetLaserDatumState(self, LaserDatumState):
        command = SET_LASER_DATUM_STATE
        if (LaserDatumState>1):
            LaserDatumState = 1
        byte_array = self.custom_int_to_bytes(LaserDatumState) 
        return self.construct_rtl_v2_packet(command, byte_array)

    
    # Report latest alarm reason (which end switch triggered the alarm)
    def GetAlarmLimitsState(self):
        command = GET_ALARM_REASON
        byte_array = b'' # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    
    # Store serial number to persistent memory
    def SetSerialNumber(self, SerialNumber):
        # serial number could contain numbers or characters. total lenght is SERIAL_NUMBER_LEN bytes. longer sting will be truncated. Shorter string will be preceded with '0's
        command = SET_SERIAL_NUMBER
        data_length = SERIAL_NUMBER_LEN

        #truncate
        if len(SerialNumber) > data_length:
            SerialNumber = SerialNumber[(len(SerialNumber) - data_length ):]

        #append '0's
        if len(SerialNumber) < data_length:
            SerialNumber = '0' * (data_length - len(SerialNumber)) + SerialNumber

        byte_array = str.encode(SerialNumber)

        return self.construct_rtl_v2_packet(command, byte_array)


    # Store product version to persistent memory
    def SetProductVersion(self, ProductVersion):
        # product number could contain numbers or characters. total lenght is PRODUCT_VERSION_LEN bytes. longer sting will be truncated. Shorter string will be preceded with '0's
        command = SET_PRODUCT_VERSION
        data_length = PRODUCT_VERSION_LEN

        #truncate
        if len(ProductVersion) > data_length:
            ProductVersion = ProductVersion[(len(ProductVersion) - data_length ):]

        #append '0's
        if len(ProductVersion) < data_length:
            ProductVersion = '0' * (data_length - len(ProductVersion)) + ProductVersion

        byte_array = str.encode(ProductVersion)

        return self.construct_rtl_v2_packet(command, byte_array)

    
    # Report serial number stored in persistent memory
    def GetSerialNumber(self):
        command = GET_SERIAL_NUMBER
        byte_array = b'' # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    
    # Report product number stored in persistent memory
    def GetProductVersion(self):
        command = GET_PRODUCT_VERSION
        byte_array = b'' # empty data
        return self.construct_rtl_v2_packet(command, byte_array)
    
    
    # Report Mafell digital spindle info: serial number, uptime, brush time, etc.
    def GetDigitalSpindleInfo(self):
        command = GET_DIGITAL_SPINDLE_INFO
        byte_array = b'' # empty data
        return self.construct_rtl_v2_packet(command, byte_array)


    # Reset brush timer in Mafell digital spindle
    def ResetDigitalSpindleBrushTime(self):
        command = RESET_DIGITAL_SPINDLE_BRUSH_TIME
        byte_array = b'' # empty data
        return self.construct_rtl_v2_packet(command, byte_array)

    # Report full GRBL run-time statistics: resets, uptime, travel time, stalls
    def GetStatistics(self):
        command = GET_STATISTICS
        byte_array = b'' # empty data
        return self.construct_rtl_v2_packet(command, byte_array)


    # TMC command, see table xx
    def constructTMCcommand(self, cmd, data, len):
        command = TMC_COMMAND
        data_length = len
        byte_array = self.custom_int_to_bytes(cmd) # first byte of data is TMC command
        for idx in range(data_length):
            byte_array = byte_array + self.custom_int_to_bytes(((data >> idx*8) & 0xff))

        return self.construct_rtl_v2_packet(command, byte_array)








