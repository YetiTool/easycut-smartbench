# -*- coding: utf-8 -*-
from datetime import datetime
import traceback


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


try:
    import pyodbc
    from influxdb import InfluxDBClient

except:
    log('Pyodbc or influxdb not installed')


class CalibrationDatabase(object):
    # THIS WILL NEED EDITING IF DB CHANGES AS IDS WILL LIKELY CHANGE TOO!!
    stage_id_dict = {
        "CalibrationQC": 1,
        "CalibrationCheckQC": 2,
        "UnweightedFT": 3,
        "WeightedFT": 4,
        "OvernightWearIn": 5,
        "CalibrationOT": 6,
        "CalibrationCheckOT": 7,
        "FullyCalibratedTest": 8
    }

    #ODBC Driver 17 for SQL Server ON WINDOWS
    connection_string = 'DRIVER={FreeTDS};SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s;TDS_Version = 7.2'

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
            import credentials

        try:
            self.conn = pyodbc.connect(self.connection_string % (credentials.server, credentials.port,
                                                                 credentials.database, credentials.username,
                                                                 credentials.password))
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
                    "SoftwareVersion, FirmwareVersion, Squareness, DateProduced) VALUES (?, ?, ?, ?, " \
                    "?, ?, ?, ?, ?, ?, ?)"

            params = (machine_serial, z_head_serial, lower_beam_serial, upper_beam_serial, console_serial,
                      y_bench_serial, spindle_serial, software_version, firmware_version, squareness, date)

            cursor.execute(query, params)

        self.conn.commit()

    def setup_z_head_coefficients(self, zh_serial, motor_index, calibration_stage_id):
        combined_id = (zh_serial + str(motor_index) + str(calibration_stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "INSERT INTO ZHeadCoefficients (Id, ZHeadSerialNumber, MotorIndex, CalibrationStageId) VALUES (" \
                    "?, ?, ?, ?)"

            params = (combined_id, zh_serial, motor_index, calibration_stage_id)

            cursor.execute(query, params)

        self.conn.commit()

    def setup_lower_beam_coefficients(self, lb_serial, motor_index, calibration_stage_id):
        combined_id = (lb_serial + str(motor_index) + str(calibration_stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "INSERT INTO LowerBeamCoefficients (Id, LowerBeamSerialNumber, MotorIndex, CalibrationStageId) " \
                    "VALUES (?, ?, ?, ?)"

            params = (combined_id, lb_serial, motor_index, calibration_stage_id)

            cursor.execute(query, params)

        self.conn.commit()

    def insert_calibration_coefficients(self, sub_serial, motor_index, calibration_stage_id, coefficients):
        combined_id = (sub_serial + str(motor_index) + str(calibration_stage_id))[2:]
        temp = self.get_ambient_temperature()

        with self.conn.cursor() as cursor:

            if temp is not None:
                query = "INSERT INTO Coefficients (SubAssemblyId, Coefficient, AmbientTemperature) VALUES (?, ?, ?)"
                for coefficient in coefficients:
                    params = (combined_id, coefficient, temp)
                    cursor.execute(query, params)

            else:
                query = "INSERT INTO Coefficients (SubAssemblyId, Coefficient) VALUES (?, ?)"
                for coefficient in coefficients:
                    params = (combined_id, coefficient)
                    cursor.execute(query, params)

        self.conn.commit()

    def insert_stage(self, description):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO Stages (Description) VALUES (?)"

            params = description

            cursor.execute(query, params)

        self.conn.commit()

    def get_stage_id_by_description(self, description):
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT Id FROM Stages WHERE Description = ?"

                params = description

                cursor.execute(query, params)

                return cursor.fetchone()[0]
        except:
            log("Could not get stage ID from DB!!")

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
                query = "INSERT INTO FinalTestStage (Id, MachineSerialNumber, FTStageId) VALUES (?, ?, ?)"

                params = (combined_id, machine_serial, ft_stage_id)

                cursor.execute(query, params)

            self.conn.commit()

        except:
            log("Final test stage already exists for this SN")

    def does_final_test_stage_already_exist(self, combined_id_only_ints):

        with self.conn.cursor() as cursor:
            query = "SELECT Id FROM FinalTestStage WHERE Id = ?"

            params = combined_id_only_ints

            cursor.execute(query, params)
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
                    "ZForwardAvg, ZForwardPeak, ZBackwardAvg, ZBackwardPeak) VALUES (?, ?, ?, ?, ?, ?, ?, ?, " \
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            params = (combined_id, x_forw_avg, x_forw_peak, x_backw_avg, x_backw_peak, y_forw_avg, y_forw_peak,
                      y_backw_avg, y_backw_peak, y1_forw_avg, y1_forw_peak, y1_backw_avg, y1_backw_peak, y2_forw_avg,
                      y2_forw_peak, y2_backw_avg, y2_backw_peak, z_forw_avg, z_forw_peak, z_backw_avg, z_backw_peak)

            cursor.execute(query, params)

        self.conn.commit()

    # @lettie please ensure data is input in the correct order according to below
    def insert_final_test_statuses(self, statuses):

        print("Before insert ft status")

        try:
            with self.conn.cursor() as cursor:
                query = "INSERT INTO FinalTestStatuses (FTID, XCoordinate, YCoordinate, ZCoordinate, XDirection, " \
                        "YDirection, ZDirection, XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, " \
                        "MOTTemperature, Timestamp, Feedrate, XWeight, YWeight, ZWeight) VALUES (?, ?, ?, ?, ?, ?, ?, ?," \
                        " ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                cursor.executemany(query, statuses)

                self.conn.commit()

        except:
            print(traceback.format_exc())

        print("After insert ft status")

    def get_serials_by_machine_serial(self, machine_serial):
        with self.conn.cursor() as cursor:
            query = "SELECT ZHeadSerialNumber, LowerBeamSerialNumber FROM Machines WHERE MachineSerialNumber = ?"

            params = machine_serial
            cursor.execute(query, params)

            data = cursor.fetchone()

            return [data[0], data[1]]

    def get_lower_beam_coefficents(self, lb_serial, motor_index, stage_id):
        combined_id = (lb_serial + str(motor_index) + str(stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "SELECT Coefficient FROM Coefficients WHERE SubAssemblyId = ?"

            params = combined_id

            cursor.execute(query, params)

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
                    FROM Machines WHERE MachineSerialNumber = ?"

            params = machine_serial

            cursor.execute(query, params)

            data = cursor.fetchone()

            return [data[0], data[1], data[2], data[3], data[4], data[5], data[6]]

    # NEW

    def insert_z_head_statistics(self):
        pass

def test_get_stage_id_by_description():
    db = CalibrationDatabase()
    db.set_up_connection()

    print(db.get_stage_id_by_description('CalibrationQC'))

test_get_stage_id_by_description()

