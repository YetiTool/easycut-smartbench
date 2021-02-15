'''
Module to process readings from DTI
'''

from kivy.clock import Clock
from asmcnc.comms import micrometer


PORT = '/dev/ttyUSB0'

DTI = micrometer.micrometer(PORT)

reading = DTI.read_mm()



def test_readout(dt):
	print(DTI.read_mm())

Clock.schedule_once(test_readout, 5)