'''
Created on 25 Jan 2022
@author: Letty
'''

import unittest
from mock import Mock, MagicMock
from serial_mock.mock import MockSerial, DummySerial
from serial_mock.decorators import serial_query
from time import sleep

import sys
sys.path.append('./src')
from asmcnc.comms import serial_connection
from asmcnc.comms import localization

##########################################################

#  PLAN THE TEST:
#  
#  >>> GIVEN:
#    1    GIVEN serial comms module is connected serial object connected to FW < 1.3.6 (no voltages or temps)
#    2    GIVEN serial comms module is connected serial object connected to 2.2.8 > FW > 1.3.6 (2 temps and all voltages)
#    3    GIVEN serial comms module is connected serial object connected to FW >= 2.2.8 (3 temps and all voltages)

#  >>> WHEN:
#    *    WHEN serial comms module reads in a status containing any number of temps or voltages
#  

#  >>> THEN:
#    *    THEN the serial comms module parses the status into corresponding variables in the serial comms module

##########################################################

# DOESN'T WANT TO BE MULTIPE OBJECTS - NOT SURE WHY 

class YETIPCB_OLDSCHOOL(MockSerial):


    thing = "HAI"

    @serial_query("?")
    def do_something(self):
        return "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

# class YETIPCB_v12(MockSerial):
#     @serial_query("?")
#     def do_something(self):
#         return "<Check|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

# class YETIPCB_v13(MockSerial):
#     @serial_query("?")
#     def do_something(self):
#         return "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"


class Test(unittest.TestCase):

	serial_module = object

	def setUp(self):
		# If the set_up method raises an exception while the test is running, 
		# the framework will consider the test to have suffered an error, 
		# and the runTest (or test_X_Name) method will not be executed.

		m = Mock()
		sm = Mock()
		sett = Mock()
		l = localization.Localization()
		jd = Mock()

		self.serial_module = serial_connection.SerialConnection(m, sm, sett, l, jd)
		self.serial_module.VERBOSE_ALL_RESPONSE = True

	def tearDown(self):
		self.serial_module.__del__()


	### TEST 1: DOES SERIAL THINK IT IS CONNECTED??
	def testDoesSerialThinkItsConnected(self):
		"""Test that serial module is connected"""
		THING = YETIPCB_OLDSCHOOL
		self.serial_module.s = DummySerial(THING)
		print(self.THING.thing)
		self.serial_module.s.fd = 1 # this is needed to force it to run
		assert self.serial_module.is_connected() == True, 'not connected'

	def testTheMockInterface(self):
		self.serial_module.s = DummySerial(YETIPCB_OLDSCHOOL)
		self.serial_module.s.fd = 1 # this is needed to force it to run
		self.serial_module.start_services(1)
		sleep(0.3)
		assert self.serial_module.m_state == "Idle", 'not idle'

	# def testStatusChange(self):
	# 	self.serial_module.s = DummySerial(YETIPCB_v12)
	# 	self.serial_module.s.fd = 1 # this is needed to force it to run
	# 	self.serial_module.start_services(1)
	# 	sleep(0.3)
	# 	assert self.serial_module.m_state == "Check", 'not check'
		




if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()