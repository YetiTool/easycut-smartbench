import logging

"""
Created on 1 Feb 2022
@author: Letty
"""
try:
    import unittest
except:
    print("Can't import mocking packages, are you on a dev machine?")
import sys

sys.path.append("./src")
"""
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.automated_unit_tests.comms.test_construct_tmc_commands
"""
from asmcnc.comms.yeti_grbl_protocol import protocol
from asmcnc.comms.yeti_grbl_protocol.c_defines import *


class ConstructTMCCommandTest(unittest.TestCase):
    def setUp(self):
        self.p = protocol.protocol_v2()

    def testconstructTMCcommand1(self):
        """sending command to motor:4, cmd:101, val:128"""
        print(list(self.p.constructTMCcommand(101, 128, 1)))

    def testconstructTMCcommand2(self):
        """sending command to motor:4, cmd:101, val:128"""
        print(list(self.p.constructTMCcommand(109, 67109336, 1)))

    def testconstructTMCcommand1(self):
        """sending command to motor:4, cmd:101, val:128"""
        self.assertEqual(
            self.p.constructTMCcommand(101, 128, 1), "^\x04\x00\x0c\x8f^\x06\x012e\x80W"
        )

    def testconstructTMCcommand2(self):
        """sending command to motor:4, cmd:101, val:128"""
        self.assertEqual(
            self.p.constructTMCcommand(109, 67109336, 1),
            "^\x04\x00\x0c\x8f^\x06\x012mØp",
        )


if __name__ == "__main__":
    unittest.main()
