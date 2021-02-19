'''
Test to read in encoder & print live readings

'''
import time
from asmcnc.production import encoder_connection

AMA0 = 'ttyACM0' # check these when HW is installed
AMA1 = 'ttyACM1' # check these when HW is installed

encoder_resolution = 0.025 # mm (25 microns)

sm = None
e_test = encoder_connection.EncoderConnection(sm, AMA0)


while True: 
	print(str(float(e_test.F_side + e_test.H_side)))
	time.sleep(2)
