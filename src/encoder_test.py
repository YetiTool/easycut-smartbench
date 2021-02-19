'''
Test to read in encoder & print live readings

'''
import time

AMA0 = 'ttyAMA0' # check these when HW is installed
AMA1 = 'ttyAMA1' # check these when HW is installed
y_length = float(2645 - 20)
encoder_resolution = 0.025 # mm (25 microns)

e_test = encoder_connection.EncoderConnection(self.sm, AMA0)


while True: 
	print(str(float(self.e_test.F_side + self.e_test.F_side)*encoder_resolution))
	time.sleep(2)
