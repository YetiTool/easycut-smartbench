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


    # AVAILABLE STAGES ARE: 

    # "CalibrationQC"
    # "CalibrationCheckQC"
    # "UnweightedFT"
    # "WeightedFT"
    # "OvernightWearIn"
    # "CalibrationOT"
    # "CalibrationCheckOT"
    # "FullyCalibratedTest"


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

    def is_connected(self):
        return self.conn.product_version != None
        
    def insert_serial_numbers(self, machine_serial, z_head_serial, lower_beam_serial, upper_beam_serial,
                            console_serial, y_bench_serial, spindle_serial, software_version, firmware_version,
                            squareness):
        date = datetime.now().strftime('%d/%m/%Y %H:%M')

        with self.conn.cursor() as cursor:
            query = "INSERT INTO Machines (MachineSerialNumber, ZHeadSerialNumber, LowerBeamSerialNumber, " \
                    "UpperBeamSerialNumber, ConsoleSerialNumber, YBenchSerialNumber, SpindleSerialNumber, " \
                    "SoftwareVersion, FirmwareVersion, Squareness, DateProduced) VALUES ('%s', '%s', '%s', '%s', " \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (machine_serial, z_head_serial, lower_beam_serial,
                                                                   upper_beam_serial, console_serial, y_bench_serial,
                                                                   spindle_serial, software_version, firmware_version,
                                                                   squareness, date)

            cursor.execute(query)

        self.conn.commit()

    def setup_z_head_coefficients(self, zh_serial, motor_index, calibration_stage_id):
        combined_id = zh_serial + str(motor_index) + str(calibration_stage_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO ZHeadCoefficients (Id, ZHeadSerialNumber, MotorIndex, CalibrationStageId) VALUES (" \
                    "'%s', '%s', %s, %s)" % (combined_id, zh_serial, motor_index, calibration_stage_id)

            cursor.execute(query)

        self.conn.commit()

    def insert_z_head_coefficients(self, zh_serial, motor_index, calibration_stage_id, coefficients):
        combined_id = zh_serial + str(motor_index) + str(calibration_stage_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO Coefficients (SubAssemblyId, Coefficient) VALUES ('%s', %s)"

            for coefficient in coefficients:
                cursor.execute(query % (combined_id, coefficient))

        self.conn.commit()

    def setup_lower_beam_coefficients(self, lb_serial, motor_index, calibration_stage_id):
        combined_id = lb_serial + str(motor_index) + str(calibration_stage_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO LowerBeamCoefficients (Id, LowerBeamSerialNumber, MotorIndex, CalibrationStageId) " \
                    "VALUES ('%s', '%s', %s, %s)" % (combined_id, lb_serial, motor_index, calibration_stage_id)

            cursor.execute(query)

        self.conn.commit()

    def insert_lower_beam_coefficients(self, lb_serial, motor_index, calibration_stage_id, coefficients):
        combined_id = lb_serial + str(motor_index) + str(calibration_stage_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO Coefficients (SubAssemblyId, Coefficient) VALUES ('%s', %s)"

            for coefficient in coefficients:
                cursor.execute(query % (combined_id, coefficient))

        self.conn.commit()

    def insert_stage(self, description):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO Stages (Description) VALUES ('%s')" % description

            cursor.execute(query)

        self.conn.commit()

    def get_stage_id_by_description(self, description):
        with self.conn.cursor() as cursor:
            query = "SELECT Id FROM Stages WHERE Description = '%s'" % description

            cursor.execute(query)

            return cursor.fetchone()[0]

    def insert_final_test_stage(self, machine_serial, ft_stage_id):

        try: 
            combined_id = machine_serial + str(ft_stage_id)

            with self.conn.cursor() as cursor:
                query = "INSERT INTO FinalTestStage (Id, MachineSerialNumber, FTStageId) VALUES ('%s', '%s', %s)" \
                        "" % (combined_id, machine_serial, ft_stage_id)

                cursor.execute(query)

            self.conn.commit()

        except pytds.tds_base.IntegrityError:
            log("Final test stage already exists for this SN")

    def insert_final_test_statistics(self, machine_serial, ft_stage_id, x_forw_avg, x_forw_peak, x_backw_avg, x_backw_peak,
                                     y_forw_avg, y_forw_peak, y_backw_avg, y_backw_peak, y1_forw_avg, y1_forw_peak,
                                     y1_backw_avg, y1_backw_peak, y2_forw_avg, y2_forw_peak, y2_backw_avg, y2_backw_peak,
                                     z_forw_avg, z_forw_peak, z_backw_avg, z_backw_peak):
        combined_id = machine_serial + str(ft_stage_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO FinalTestStatistics (FTID, XForwardAvg, XForwardPeak, XBackwardAvg, XBackwardPeak, " \
                    "YForwardAvg, YForwardPeak, YBackwardAvg, YBackwardPeak, Y1ForwardAvg, Y1ForwardPeak, " \
                    "Y1BackwardAvg, Y1BackwardPeak, Y2ForwardAvg, Y2ForwardPeak, Y2BackwardAvg, Y2BackwardPeak, " \
                    "ZForwardAvg, ZForwardPeak, ZBackwardAvg, ZBackwardPeak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, " \
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (combined_id, x_forw_avg, x_forw_peak,
                                                                             x_backw_avg, x_backw_peak, y_forw_avg,
                                                                             y_forw_peak, y_backw_avg, y_backw_peak,
                                                                             y1_forw_avg, y1_forw_peak, y1_backw_avg,
                                                                             y1_backw_peak, y2_forw_avg, y2_forw_peak,
                                                                             y2_backw_avg, y2_backw_peak, z_forw_avg,
                                                                             z_forw_peak, z_backw_avg, z_backw_peak)

            cursor.execute(query)

        self.conn.commit()

    # @lettie please ensure data is input in the correct order according to below
    def insert_final_test_statuses(self, machine_serial, ft_stage_id, statuses):
        combined_id = machine_serial + str(ft_stage_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO FinalTestStatuses (FTID, XCoordinate, YCoordinate, ZCoordinate, XDirection, " \
                    "YDirection, ZDirection, XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, " \
                    "MOTTemperature, Timestamp, Feedrate) VALUES ('%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                    "%s, %s, %s, %s, %s)"

            for status in statuses:
                cursor.execute(query % (combined_id, status[0], status[1], status[2], status[3], status[4], status[5],
                                        status[6], status[7], status[8], status[9], status[10], status[11], status[12],
                                        status[13], status[14], status[15]))
        
        self.conn.commit()

