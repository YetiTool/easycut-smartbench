# -*- coding: utf-8 -*-
from datetime import datetime
import traceback


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


try:
    import pytds
    from influxdb import InfluxDBClient

except:
    log('Pytds or influxdb not installed')


class CalibrationDatabase(object):
    # THIS WILL NEED EDITING IF DB CHANGES AS IDS WILL LIKELY CHANGE TOO!!
    stage_id_dict = {
        "CalibrationQC" : 1,
        "CalibrationCheckQC" : 2,
        "UnweightedFT" : 3,
        "WeightedFT" : 4,
        "OvernightWearIn" : 5,
        "CalibrationOT" : 6,
        "CalibrationCheckOT" : 7,
        "FullyCalibratedTest" : 8
    }

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
            self.conn = pytds.connect(credentials.server, credentials.database, credentials.username,
                                      credentials.password, port=credentials.port)
            log("Connected to database")

        except:
            log('Unable to connect to database')
            print(traceback.format_exc())

        try:
            self.influx_client = InfluxDBClient(credentials.influx_server, credentials.influx_port,
                                                credentials.influx_username, credentials.influx_password,
                                                credentials.influx_database)
            log("Connected to InfluxDB")

        except:
            log("Unable to connect to InfluxDB")

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
        combined_id = (zh_serial + str(motor_index) + str(calibration_stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "INSERT INTO ZHeadCoefficients (Id, ZHeadSerialNumber, MotorIndex, CalibrationStageId) VALUES (" \
                    "'%s', '%s', %s, %s)" % (combined_id, zh_serial, motor_index, calibration_stage_id)

            cursor.execute(query)

        self.conn.commit()

    def setup_lower_beam_coefficients(self, lb_serial, motor_index, calibration_stage_id):
        combined_id = (lb_serial + str(motor_index) + str(calibration_stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "INSERT INTO LowerBeamCoefficients (Id, LowerBeamSerialNumber, MotorIndex, CalibrationStageId) " \
                    "VALUES ('%s', '%s', %s, %s)" % (combined_id, lb_serial, motor_index, calibration_stage_id)

            cursor.execute(query)

        self.conn.commit()

    def insert_calibration_coefficients(self, sub_serial, motor_index, calibration_stage_id, coefficients):
        combined_id = (sub_serial + str(motor_index) + str(calibration_stage_id))[2:]
        temp = self.get_ambient_temperature()

        with self.conn.cursor() as cursor:

            if temp is not None:
                query = "INSERT INTO Coefficients (SubAssemblyId, Coefficient, AmbientTemperature) VALUES ('%s', %s, %s)"
                for coefficient in coefficients:
                    cursor.execute(query % (combined_id, coefficient, temp))

            else:
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

        try:
            with self.conn.cursor() as cursor:
                query = "SELECT Id FROM Stages WHERE Description = '%s'" % description

                cursor.execute(query)

                return cursor.fetchone()[0]

        except:
            log("Could not get stage ID from DB!!")
            print(traceback.format_exc())

            # assign from list instead - this is a backup! 
            # BUT if anything in db changes, it may be wrong!! 
            return self.stage_id_dict.get(description)

    def insert_final_test_stage(self, machine_serial, ft_stage_id):

        try:
            combined_id = (machine_serial + str(ft_stage_id))[2:]

            if self.does_final_test_stage_already_exist(combined_id):
                log("Final test stage already exists for this SN")
                return

            with self.conn.cursor() as cursor:
                query = "INSERT INTO FinalTestStage (Id, MachineSerialNumber, FTStageId) VALUES ('%s', '%s', %s)" \
                        "" % (combined_id, machine_serial, ft_stage_id)

                cursor.execute(query)

            self.conn.commit()

        except pytds.tds_base.IntegrityError:
            log("Final test stage already exists for this SN")

    def does_final_test_stage_already_exist(self, combined_id):

        with self.conn.cursor() as cursor:
            query = "SELECT Id FROM FinalTestStage WHERE Id = '%s'" % combined_id[2:]
            cursor.execute(query)
            data = cursor.fetchone()

        return data

        ### check whether tuple is empty

    def insert_final_test_statistics(self, machine_serial, ft_stage_id, x_forw_avg, x_forw_peak, x_backw_avg,
                                     x_backw_peak,
                                     y_forw_avg, y_forw_peak, y_backw_avg, y_backw_peak, y1_forw_avg, y1_forw_peak,
                                     y1_backw_avg, y1_backw_peak, y2_forw_avg, y2_forw_peak, y2_backw_avg,
                                     y2_backw_peak,
                                     z_forw_avg, z_forw_peak, z_backw_avg, z_backw_peak):
        combined_id = (machine_serial + str(ft_stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "INSERT INTO FinalTestStatistics (FTID, XForwardAvg, XForwardPeak, XBackwardAvg, XBackwardPeak, " \
                    "YForwardAvg, YForwardPeak, YBackwardAvg, YBackwardPeak, Y1ForwardAvg, Y1ForwardPeak, " \
                    "Y1BackwardAvg, Y1BackwardPeak, Y2ForwardAvg, Y2ForwardPeak, Y2BackwardAvg, Y2BackwardPeak, " \
                    "ZForwardAvg, ZForwardPeak, ZBackwardAvg, ZBackwardPeak) VALUES ('%s', %s, %s, %s, %s, %s, %s, %s, " \
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
        combined_id = (machine_serial + str(ft_stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "INSERT INTO FinalTestStatuses (FTID, XCoordinate, YCoordinate, ZCoordinate, XDirection, " \
                    "YDirection, ZDirection, XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, " \
                    "MOTTemperature, Timestamp, Feedrate, XWeight, YWeight, ZWeight) VALUES ('%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                    "%s, %s, %s, '%s', %s, %s, %s, %s)"

            for status in statuses:
                print(status)

                cursor.execute(query % (combined_id, status[0], status[1], status[2], status[3], status[4], status[5],
                                        status[6], status[7], status[8], status[9], status[10], status[11], status[12],
                                        status[13], status[14], status[15], status[16], status[17], status[18]))

                self.conn.commit()

    def get_serials_by_machine_serial(self, machine_serial):
        with self.conn.cursor() as cursor:
            query = "SELECT ZHeadSerialNumber, LowerBeamSerialNumber FROM Machines WHERE MachineSerialNumber = '%s'" % machine_serial

            cursor.execute(query)

            data = cursor.fetchone()

            return [data[0], data[1]]

    def get_lower_beam_coefficents(self, lb_serial, motor_index, stage_id):
        combined_id = (lb_serial + str(motor_index) + str(stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "SELECT Coefficient FROM Coefficients WHERE SubAssemblyId = '%s'" % combined_id

            cursor.execute(query)

            data = cursor.fetchall()

            parameters = {}

            try:
                parameters = {
                    "coefficients": [int(i[0]) for i in data][0:128],
                    "cs": data[128][0],
                    "sgt": data[129][0],
                    "toff": data[130][0],
                    "temp": data[131][0],
                }
            except:
                log('Database is empty or incomplete for ' + combined_id)

            return parameters

    def get_ambient_temperature(self):

        try:

            query = u'SELECT "temperature" FROM "last_three_months"."environment_data" WHERE \
            ("device_ID" = \'“eDGE-2”\') AND time > now() - 2m ORDER ' \
                    u'BY DESC LIMIT 1 '

            return self.influx_client.query(query).raw['series'][0]['values'][0][1]

        except:
            return None

    def get_all_serials_by_machine_serial(self, machine_serial):
        with self.conn.cursor() as cursor:
            query = "SELECT + \
                    ZHeadSerialNumber, \
                    LowerBeamSerialNumber, \
                    UpperBeamSerialNumber, \
                    ConsoleSerialNumber, \
                    YBenchSerialNumber, \
                    SpindleSerialNumber, \
                    Squareness \
                    FROM Machines WHERE MachineSerialNumber = '%s'" % machine_serial

            cursor.execute(query)

            data = cursor.fetchone()

            return [data[0], data[1], data[2], data[3], data[4], data[5], data[6]]
