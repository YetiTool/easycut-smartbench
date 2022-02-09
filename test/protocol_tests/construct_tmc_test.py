'''
Created on 1 Feb 2022
@author: Letty
'''

try: 
    import unittest

except: 
    print("Can't import mocking packages, are you on a dev machine?")

import sys
sys.path.append('./src')


########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.protocol_tests.construct_tmc_test


from asmcnc.comms.yeti_grbl_protocol import protocol
from asmcnc.comms.yeti_grbl_protocol.c_defines import *



class ConstructTMCCommandTest(unittest.TestCase):

    def setUp(self):

        # Object to construct and send custom YETI GRBL commands
        self.p = protocol.protocol_v2()


    # testing this guy: def constructTMCcommand(self, cmd, data, len):

    def testconstructTMCcommand1(self):

        """sending command to motor:4, cmd:101, val:128"""
        # assert self.constructTMCcommand(101,128, 1), 'not connected'
        print self.p.constructTMCcommand(101+16*4,128, 1)

    def testconstructTMCcommand2(self):

        """sending command to motor:4, cmd:101, val:128"""
        # assert self.constructTMCcommand(101,128, 1), 'not connected'
        print self.p.constructTMCcommand(109+16*4,67109336, 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()