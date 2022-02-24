from datetime import datetime

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

try:
    import pytds
except:
    log('Pytds not installed - pip install python-tds')

class CalibrationDatabase(object):
    def __init__(self):
        self.conn = None

    def set_up_connection(self, location):

        try:

            if location  == "console":
                from asmcnc.production.database import credentials

            elif location == "usb":
                from ......media.usb import credentials

        except ImportError:
            log("Can't import credentials")

        try:
            self.conn = pytds.connect(credentials.server, credentials.database, credentials.username, credentials.password)
            log("Connected to database")

        except: 
            log('Unable to connect to database')

    def is_connected(self):
        return self.conn.product_version != None
        
    def get_serial_number(self):
        serial_number_filepath = "/home/pi/smartbench_serial_number.txt"
        serial_number_from_file = ''
        
        try:
            file = open(serial_number_filepath, 'r')
            serial_number_from_file  = str(file.read())
            file.close()
        except: 
            print 'Could not get serial number! Please contact YetiTool support!'
            
        return str(serial_number_from_file)

    def send_final_test_calibration(self, serial_number, unweighted_x, unweighted_y, unweighted_z, weighted_x, weighted_y, weighted_z):
        with self.conn.cursor() as cursor:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO FinalTest (SerialNumber, Date, UnweightedX, UnweightedY, UnweightedZ, WeightedX, WeightedY, WeightedZ) VALUES ('" + serial_number + "', '" + date + "', '" + str(unweighted_x) + "', '" + str(unweighted_y) + "', '" + str(unweighted_z) + "', '" + str(weighted_x) + "', '" + str(weighted_y) + "', '" + str(weighted_z) + "')"

            cursor.execute(query)
            self.conn.commit()

    def send_overnight_test_calibration(self, serial_number, overnight_x, overnight_y, overnight_z):
        with self.conn.cursor() as cursor:
            query = "UPDATE FinalTest SET OvernightX = '" + str(overnight_x) + "', OvernightY = '" + str(overnight_y) + "', OvernightZ = '" + str(overnight_z) + "' WHERE SerialNumber = '" + serial_number + "'"
            
            cursor.execute(query)

            self.conn.commit()

    def send_z_head_calibration(self, serial_number, motor_index, sg_coefficients, cs, sgt, toff, temperature):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO TMC (SerialNumber, MotorIndex, CS, SG, SGT, TOFF, Temperature) VALUES ('" + str(serial_number) + "', '" + str(motor_index) + "', '" + str(cs) + "', '" + str(sg_coefficients) + "', '" + str(sgt) + "', '" + str(toff) + "', '" + str(temperature) + "')"
            cursor.execute(query)

            self.conn.commit()

    def send_lower_beam_calibration(self, serial_number, motor_index, sg_coefficients, cs, sgt, toff, temperature):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO TMC (SerialNumber, MotorIndex, CS, SG, SGT, TOFF, Temperature) VALUES ('" + str(serial_number) + "', '" + str(motor_index) + "', '" + str(cs) + "', '" + str(sg_coefficients) + "', '" + str(sgt) + "', '" + str(toff) + "', '" + str(temperature) + "')"
            cursor.execute(query)

            self.conn.commit()

    def get_lower_beam_parameters(self, serial_number, motor_index):
        with self.conn.cursor() as cursor:
            query = "SELECT * FROM TMC WHERE SerialNumber = '" + str(serial_number) + "' AND MotorIndex = '" + str(motor_index) + "' ORDER BY Id DESC"

            cursor.execute(query)

            data = cursor.fetchone()

            return data


    