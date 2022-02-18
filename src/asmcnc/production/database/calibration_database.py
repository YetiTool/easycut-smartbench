import pytds
from datetime import datetime

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class CalibrationDatabase(object):
    def __init__(self):
        try:
            from asmcnc.production.database import credentials
        except ImportError:
            log("Can't import credentials")

            # try to load from usb stick here
        try:
            self.conn = pytds.connect(credentials.server, credentials.database, credentials.username, credentials.password)
        except: 
            log('Unable to connect to database')

    def is_connected(self):
        return self.conn.product_version != None

    def send_final_test_payload(self, serial_number, non_weighted_payload, weighted_payload, overnight_payload):
        with self.conn.cursor() as cursor:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO FinalTest (MachineSerialNo, NonWeightedPayload, WeightedPayload, OvernightPayload, Date) VALUES ('" + serial_number + "', '" + non_weighted_payload + "', '" + weighted_payload + "', '" + overnight_payload + "', '" + date + "')"
            cursor.execute(query)
            self.conn.commit()
        
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

    