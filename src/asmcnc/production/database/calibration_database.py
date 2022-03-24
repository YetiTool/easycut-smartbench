from datetime import datetime
import traceback

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

    def set_up_connection(self):

        try:
            from asmcnc.production.database import credentials

        except ImportError:
            log("Can't import credentials")

        try:
            self.conn = pytds.connect(credentials.server, credentials.database, credentials.username, credentials.password)
            log("Connected to database")

        except: 
            log('Unable to connect to database')

    # add machine to 'Machines' table
    # returns Id from database
    # this should be stored and used to insert into other tables
    def create_new_machine(self, serial_number):
        query = "INSERT INTO Machines (SerialNumber) OUTPUT INSERTED.Id VALUES ('%s')" % serial_number

        with self.conn.cursor() as cursor:
            data = cursor.execute_scalar(query)
            return data

    # store machine id to sb_values folder
    def store_machine_id(self, machine_id):
        with open('sb_values/smartbench_machine_id.txt', 'w+') as file:
            file.write(machine_id)

    # get stored machine id from sb_values folder
    def get_stored_machine_id(self):
        try:
            with open('sb_values/smartbench_machine_id.txt', 'r') as file:
                return file.readline()

        except: 
            return 'test'

    # use this function to insert the full payload
    # returns true/false depending on whether was successful
    def insert_status_wrapper(self, status):
        
        # try:
        #     self.insert_status(self.get_stored_machine_id(), *status)
        # except:
        #     print(str(traceback.format_exc()))
        #     return False

        return True

    # use this function to insert single statistic array into database
    # returns true/false depending on whether was successful
    def insert_statistics_wrapper(self, statistics):
        try:
            self.insert_statistics(self.get_stored_machine_id(), *statistics)
        except:
            print(str(traceback.format_exc()))
            return False
        
        return True

    # use this function to insert the full payload
    # returns true/false depending on whether was successful
    def insert_coefficients_wrapper(self, coefficients):
        for coefficient in coefficients:
            try:
                self.insert_coefficients(self.get_stored_machine_id(), *coefficient)
            except:
                print(str(traceback.format_exc()))
                return False
        
        return True

    # run as many times as required to insert full payload
    # stage defines whether it's weighted, unweighted, overnight etc
    def insert_status(self, machine_id, stage, x_coordinate, y_coordinate, z_coordinate, x_direction, y_direction, z_direction, 
        x_sg, y_sg, y1_sg, y2_sg, z_sg, tmc_temperature, pcb_temperature, mot_temperature, feedrate, timestamp):

        query = """INSERT INTO FinalTestStatuses (MachineId, Stage, XCoordinate, YCoordinate, ZCoordinate, XDirection, YDirection, ZDirection,
            XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, MOTTemperature, Feedrate, Timestamp) VALUES (%s, '%s', %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')""" % (machine_id, stage, x_coordinate, y_coordinate, z_coordinate, x_direction, y_direction, z_direction,
            x_sg, y_sg, y1_sg, y2_sg, z_sg, tmc_temperature, pcb_temperature, mot_temperature, feedrate, timestamp)
        
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()

    # run as many times as required to insert full payload
    # stage defines whether it's weighted, unweighted, overnight etc
    def insert_statistics(self, machine_id, stage, x_forward_avg, x_forward_peak, x_backward_avg, x_backward_peak, y_forward_avg,
        y_forward_peak, y_backward_avg, y_backward_peak, y1_forward_avg, y1_forward_peak, y1_backward_avg, y1_backward_peak,
        y2_forward_avg, y2_forward_peak, y2_backward_avg, y2_backward_peak, z_forward_avg, z_forward_peak, z_backward_avg, z_backward_peak):

        query = """INSERT INTO FinalTestStatistics (MachineId, Stage, XForwardAvg, XForwardPeak, XBackwardAvg, XBackwardPeak, YForwardAvg,
            YForwardPeak, YBackwardAvg, YBackwardPeak, Y1ForwardAvg, Y1ForwardPeak, Y1BackwardAvg, Y1BackwardPeak, Y2ForwardAvg, Y2ForwardPeak,
            Y2BackwardAvg, Y2BackwardPeak, ZForwardAvg, ZForwardPeak, ZBackwardAvg, ZBackwardPeak) VALUES (%s, '%s', %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" % (machine_id, stage, x_forward_avg, x_forward_peak, x_backward_avg, x_backward_peak,
            y_forward_avg, y_forward_peak, y_backward_avg, y_backward_peak, y1_forward_avg, y1_forward_peak, y1_backward_avg, y1_backward_peak, 
            y2_forward_avg, y2_forward_peak, y2_backward_avg, y2_backward_peak, z_forward_avg, z_forward_peak, z_backward_avg, z_backward_peak)

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()

    # run as many times as required to insert full payload
    # stage defines whether it's weighted, unweighted, overnight etc
    def insert_calibration_coefficients(self, machine_id, stage, motor_index, coefficient):

        query = "INSERT INTO CalibrationCoefficients (MachineId, Stage, MotorIndex, Coefficient) VALUES (%s, '%s', %s, %s)" % (machine_id, stage, motor_index, coefficient)

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()
