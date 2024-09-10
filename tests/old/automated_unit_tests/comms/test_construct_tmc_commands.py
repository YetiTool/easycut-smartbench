# -*- coding: utf-8 -*-
'''
Created on 1 Feb 2022
@author: Letty
'''
from core.logging.logging_system import Logger

try: 
    import unittest

except: 
    Logger.info("Can't import mocking packages, are you on a dev machine?")

import sys
sys.path.append('./src')

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.automated_unit_tests.comms.test_construct_tmc_commands
'''

from core.serial.yeti_grbl_protocol import protocol


class ConstructTMCCommandTest(unittest.TestCase):

    def setUp(self):

        # Object to construct and send custom YETI GRBL commands
        self.p = protocol.protocol_v2()


    # testing this guy: def constructTMCcommand(self, cmd, data, len):

    def testconstructTMCcommand1(self):

        """sending command to motor:4, cmd:101, val:128"""
        # assert self.constructTMCcommand(101,128, 1), 'not connected'
        Logger.info(list(self.p.constructTMCcommand(101,128, 1)))

    def testconstructTMCcommand2(self):

        """sending command to motor:4, cmd:101, val:128"""
        # assert self.constructTMCcommand(101,128, 1), 'not connected'
        Logger.info(list(self.p.constructTMCcommand(109,67109336, 1)))


    def testconstructTMCcommand1(self):

        """sending command to motor:4, cmd:101, val:128"""
        # assert self.constructTMCcommand(101,128, 1), 'not connected'
        self.assertEqual(self.p.constructTMCcommand(101,128, 1), b'^\x04\x00\x0c\x8f^\x06\x012e\x80W')

    def testconstructTMCcommand2(self):

        """sending command to motor:4, cmd:101, val:128"""
        # assert self.constructTMCcommand(101,128, 1), 'not connected'
        self.assertEqual(self.p.constructTMCcommand(109,67109336, 1), b'^\x04\x00\x0c\x8f^\x06\x012m\xd8p')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()