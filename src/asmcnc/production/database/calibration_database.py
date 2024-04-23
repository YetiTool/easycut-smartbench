# -*- coding: utf-8 -*-
from datetime import datetime
import traceback, threading
import json
import sys

from asmcnc.comms.logging_system.logging_system import Logger

from asmcnc.production.database.payload_publisher import DataPublisher


try: 
    try:
        import pymysql as my_sql_client

    except:
        import MySQLdb as my_sql_client
except:
    Logger.exception("No MySQLdb or pymysql package installed")

try:
    from influxdb import InfluxDBClient
except:
    Logger.exception('Influxdb not installed')


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


    # if sys.platform == 'win32' or sys.platform == 'darwin':
    #     # ODBC Driver 17 for SQL Server ON WINDOWS
    #     connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s;TDS_Version = 7.2'
    #
    # else:
    #     # FreeTDS
    #     connection_string = 'DRIVER={FreeTDS};SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s;TDS_Version = 7.2'

    def __init__(self):
        self.conn = None
        self.ssh_conn = None

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

            self.conn = my_sql_client.connect(host=credentials.server, db=credentials.database,
                                              user=credentials.username,
                                              passwd=credentials.password)
            Logger.info("Connected to database")

            self.ssh_conn = my_sql_client.connect(host=credentials.server, db='sshdb', user=credentials.username,
                                                  passwd=credentials.password)
            Logger.info('Connected to ssh key db')

            self.influx_client = InfluxDBClient(credentials.influx_server, credentials.influx_port,
                                                credentials.influx_username, credentials.influx_password,
                                                credentials.influx_database)
            Logger.info("Connected to InfluxDB")

        except Exception as e:
            Logger.exception('Failed to import credentials!')
            if sys.platform != 'win32' and sys.platform != 'darwin':
                Logger.error("Can't import credentials (trying to get local folder creds)")
                import credentials

    def insert_serial_numbers(self, machine_serial, z_head_serial, lower_beam_serial, upper_beam_serial,
                              console_serial, y_bench_serial, spindle_serial, software_version, firmware_version,
                              squareness):
        date = datetime.now().strftime('%d/%m/%Y %H:%M')

        with self.conn.cursor() as cursor:
            query = "INSERT INTO Machines (MachineSerialNumber, ZHeadSerialNumber, LowerBeamSerialNumber, " \
                    "UpperBeamSerialNumber, ConsoleSerialNumber, YBenchSerialNumber, SpindleSerialNumber, " \
                    "SoftwareVersion, FirmwareVersion, Squareness, DateProduced) VALUES (%s, %s, %s, %s, " \
                    "%s, %s, %s, %s, %s, %s, %s)"

            params = [machine_serial, z_head_serial, lower_beam_serial, upper_beam_serial, console_serial,
                      y_bench_serial, spindle_serial, software_version, firmware_version, squareness, date]

            cursor.execute(query, params)

        self.conn.commit()

    def do_z_head_coefficients_exist(self, combined_id):
        with self.conn.cursor() as cursor:
            query = "SELECT Id FROM ZHeadCoefficients WHERE Id = %s"

            cursor.execute(query, [combined_id])

            return cursor.fetchone() is not None

    def do_lower_beam_coefficients_exist(self, combined_id):
        with self.conn.cursor() as cursor:
            query = "SELECT Id FROM LowerBeamCoefficients WHERE Id = %s"

            cursor.execute(query, [combined_id])

            return cursor.fetchone() is not None

    def delete_z_head_coefficients(self, combined_id):
        Logger.info("Deleting existing data from ZHeadCoefficients: " + str(combined_id))
        with self.conn.cursor() as cursor:
            query = "DELETE FROM ZHeadCoefficients WHERE Id = %s"

            cursor.execute(query, [combined_id])

            self.delete_coefficients(combined_id)

        self.conn.commit()

    def delete_coefficients(self, combined_id):
        Logger.info("Deleting existing data from Coefficients: " + str(combined_id))
        with self.conn.cursor() as cursor:
            query = "DELETE FROM Coefficients WHERE SubAssemblyId = %s"

            cursor.execute(query, [combined_id])

        self.conn.commit()

    def delete_lower_beam_coefficients(self, combined_id):
        Logger.info("Deleting existing data from LowerBeamCoefficients: " + str(combined_id))
        with self.conn.cursor() as cursor:
            query = "DELETE FROM LowerBeamCoefficients WHERE Id = %s"

            cursor.execute(query, [combined_id])

            self.delete_coefficients(combined_id)

        self.conn.commit()

    def setup_z_head_coefficients(self, zh_serial, motor_index, calibration_stage_id):
        combined_id = (zh_serial + str(motor_index) + str(calibration_stage_id))[2:]

        if self.do_z_head_coefficients_exist(combined_id):
            self.delete_z_head_coefficients(combined_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO ZHeadCoefficients (Id, ZHeadSerialNumber, MotorIndex, CalibrationStageId) VALUES (" \
                    "%s, %s, %s, %s)"

            params = [combined_id, zh_serial, motor_index, calibration_stage_id]

            cursor.execute(query, params)

        self.conn.commit()

    def setup_lower_beam_coefficients(self, lb_serial, motor_index, calibration_stage_id):
        combined_id = (lb_serial + str(motor_index) + str(calibration_stage_id))[2:]

        if self.do_lower_beam_coefficients_exist(combined_id):
            self.delete_lower_beam_coefficients(combined_id)

        with self.conn.cursor() as cursor:
            query = "INSERT INTO LowerBeamCoefficients (Id, LowerBeamSerialNumber, MotorIndex, CalibrationStageId) " \
                    "VALUES (%s, %s, %s, %s)"

            params = [combined_id, lb_serial, motor_index, calibration_stage_id]

            cursor.execute(query, params)

        self.conn.commit()

    def insert_calibration_coefficients(self, sub_serial, motor_index, calibration_stage_id, coefficients):
        combined_id = (sub_serial + str(motor_index) + str(calibration_stage_id))[2:]
        temp = self.get_ambient_temperature()

        with self.conn.cursor() as cursor:

            if temp is not None:
                query = "INSERT INTO Coefficients (SubAssemblyId, Coefficient, AmbientTemperature) VALUES (%s, %s, %s)"
                for coefficient in coefficients:
                    params = [combined_id, coefficient, temp]
                    cursor.execute(query, params)

            else:
                query = "INSERT INTO Coefficients (SubAssemblyId, Coefficient) VALUES (%s, %s)"
                for coefficient in coefficients:
                    params = [combined_id, coefficient]
                    cursor.execute(query, params)

        self.conn.commit()

    def insert_stage(self, description):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO Stages (Description) VALUES (%s)"

            params = [description]

            cursor.execute(query, params)

        self.conn.commit()

    def get_stage_id_by_description(self, description):
        return self.stage_id_dict.get(description)

        # try:
        #     with self.conn.cursor() as cursor:
        #         query = "SELECT Id FROM Stages WHERE Description = ?"
        #
        #         params = description
        #
        #         cursor.execute(query, params)
        #
        #         return cursor.fetchone()[0]
        #
        # except:
        #     Logger.info("Could not get stage ID from DB!!")
        #     Logger.info(traceback.format_exc())
        #
        #     # assign from list instead - this is a backup!
        #     # BUT if anything in db changes, it may be wrong!!
        #     return self.stage_id_dict.get(description)

    def insert_calibration_check_stage(self, sub_serial, stage_id):
        try:
            
            combined_id = str(sub_serial)[2:] + str(stage_id)

            if self.does_calibration_check_stage_already_exist(combined_id):
                Logger.warning("Calibration check stage already exists for this SN")
                return

            with self.conn.cursor() as cursor:
                query = "INSERT INTO CalibrationCheckStages (Id, SubSerialNumber, StageId) VALUES (%s, %s, %s)"

                params = [combined_id, sub_serial, stage_id]

                cursor.execute(query, params)

            self.conn.commit()

        except:
            Logger.exception('Failed to insert calibration check stage!')

    def does_calibration_check_stage_already_exist(self, combined_id_only_ints):

        with self.conn.cursor() as cursor:
            query = "SELECT Id FROM CalibrationCheckStages WHERE Id = %s"

            params = [combined_id_only_ints]

            cursor.execute(query, params)
            data = cursor.fetchone()

        return data

        ### check whether tuple is empty

    def insert_final_test_stage(self, machine_serial, ft_stage_id):

        try:
            combined_id = (machine_serial + str(ft_stage_id))[2:]

            if self.does_final_test_stage_already_exist(combined_id):
                Logger.warning("Final test stage already exists for this SN")
                return

            with self.conn.cursor() as cursor:
                query = "INSERT INTO FinalTestStage (Id, MachineSerialNumber, FTStageId) VALUES (%s, %s, %s)"

                params = [combined_id, machine_serial, ft_stage_id]

                cursor.execute(query, params)

            self.conn.commit()

        except:
            Logger.warning("Final test stage already exists for this SN")

    def does_final_test_stage_already_exist(self, combined_id_only_ints):

        with self.conn.cursor() as cursor:
            query = "SELECT Id FROM FinalTestStage WHERE Id = %s"

            params = [combined_id_only_ints]

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
                    "ZForwardAvg, ZForwardPeak, ZBackwardAvg, ZBackwardPeak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, " \
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            params = [combined_id, x_forw_avg, x_forw_peak, x_backw_avg, x_backw_peak, y_forw_avg, y_forw_peak,
                      y_backw_avg, y_backw_peak, y1_forw_avg, y1_forw_peak, y1_backw_avg, y1_backw_peak, y2_forw_avg,
                      y2_forw_peak, y2_backw_avg, y2_backw_peak, z_forw_avg, z_forw_peak, z_backw_avg, z_backw_peak]

            cursor.execute(query, params)

        self.conn.commit()

    # @lettie please ensure data is input in the correct order according to below
    def insert_final_test_statuses(self, statuses):

        Logger.debug("Before insert ft status")

        try:
            with self.conn.cursor() as cursor:
                query = "INSERT INTO FinalTestStatuses (FTID, XCoordinate, YCoordinate, ZCoordinate, XDirection, " \
                        "YDirection, ZDirection, XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, " \
                        "MOTTemperature, Timestamp, Feedrate, XWeight, YWeight, ZWeight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s," \
                        " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor.executemany(query, statuses)

                self.conn.commit()

        except: 
            Logger.exception('Failed to insert final test statuses!')

        Logger.debug("After insert ft status")

    def get_serials_by_machine_serial(self, machine_serial):
        with self.conn.cursor() as cursor:
            query = "SELECT ZHeadSerialNumber, LowerBeamSerialNumber FROM Machines WHERE MachineSerialNumber = %s"

            params = [machine_serial]
            cursor.execute(query, params)

            data = cursor.fetchone()

            return [data[0], data[1]]

    def get_lower_beam_coefficents(self, lb_serial, motor_index, stage_id):
        combined_id = (lb_serial + str(motor_index) + str(stage_id))[2:]

        with self.conn.cursor() as cursor:
            query = "SELECT Coefficient FROM Coefficients WHERE SubAssemblyId = %s"

            params = [combined_id]

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
                Logger.exception('Database is empty or incomplete for ' + str(combined_id))

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
            query = """SELECT ZHeadSerialNumber, LowerBeamSerialNumber, UpperBeamSerialNumber, ConsoleSerialNumber,
            YBenchSerialNumber, SpindleSerialNumber, Squareness FROM Machines WHERE MachineSerialNumber = %s"""

            params = [machine_serial]

            cursor.execute(query, params)

            data = cursor.fetchone()

            return [data[0], data[1], data[2], data[3], data[4], data[5], data[6]]


    def insert_stall_experiment_results(self, stall_events):

        # # Example data: 
        # # ["ID, "X", 6000, 150, 5999, 170, -1100.4 ]

        # last_test_pass = [

        #     self.id_stage,
        #     self.current_axis(),
        #     self.feed_dict[self.current_axis()][self.indices["feed"]],
        #     self.threshold_dict[self.current_axis()][self.indices["threshold"]],
        #     reported_feed,
        #     self.m.s.last_stall_load,
        #     stall_coord
        # ]

        Logger.debug("Before insert stall events")

        try:

            with self.conn.cursor() as cursor:
                query = "INSERT INTO StallTest (FTID, Axis, Feedrate, Threshold, FeedReported, " \
                        "SGReported, CoordinateReported) VALUES (%s, %s, %s, %s, %s, %s, %s)"

                cursor.executemany(query, stall_events)
                self.conn.commit()
                return True

        except: 
            Logger.exception('Failed to execute query!')
            return False

    processing_running_data = False
    processed_running_data = {

        "2": ([], "CalibrationCheckStatuses", "CalibrationCheckQC"),
        "9": ([], "FinalTestStatuses", "StallExperiment"),
        "10": ([], "FinalTestStatuses", "CalibrationCheckStall"),
        "11": ([], "FinalTestStatuses", "CalibrationCheckAfterStall"),
        "12": ([], "CalibrationCheckStatuses", "CalibrationCheckZH"),
        "13": ([], "CalibrationCheckStatuses", "CalibrationCheckXL")

    }
    def process_status_running_data_for_database_insert(self, unprocessed_status_data, serial_number, x_weight=0, y_weight=0, z_weight=2):

        self.processing_running_data = True

        processing_running_data_thread = threading.Thread(target=self._process_running_data, args=(unprocessed_status_data, serial_number, x_weight, y_weight, z_weight))
        processing_running_data_thread.daemon = True
        processing_running_data_thread.start()

    def _process_running_data(self, unprocessed_status_data, serial_number, x_weight=0, y_weight=0, z_weight=2):

        self.processing_running_data = True

        try: 

            for idx, element in enumerate(unprocessed_status_data): 

                x_dir, y_dir, z_dir = self.generate_directions(unprocessed_status_data, idx)

            # XCoordinate, YCoordinate, ZCoordinate, XDirection, YDirection, ZDirection, XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, MOTTemperature, Timestamp, Feedrate

                status = {
                    "Id": "",
                    "FTID": int(serial_number[2:] + str(element[0])),
                    "XCoordinate": element[1],
                    "YCoordinate": element[2],
                    "ZCoordinate": element[3],
                    "XDirection": x_dir,
                    "YDirection": y_dir,
                    "ZDirection": z_dir,
                    "XSG": element[4],
                    "YSG": element[5],
                    "Y1SG": element[6],
                    "Y2SG":element[7],
                    "ZSG":element[8],
                    "TMCTemperature":element[9],
                    "PCBTemperature":element[10],
                    "MOTTemperature":element[11],
                    "Timestamp": element[12].strftime('%Y-%m-%d %H:%M:%S'),
                    "Feedrate": element[13],
                    "XWeight": x_weight,
                    "YWeight": y_weight,
                    "ZWeight": z_weight
                }

                self.processed_running_data[str(element[0])][0].append(status)

        except:
            Logger.exception('Something failed!')

        self.processing_running_data = False


    def generate_directions(self, unprocessed_status_data, idx):

        # -1    FORWARDS/DOWN (AWAY FROM HOME)
        # 0     NOT MOVING
        # 1     BACKWARDS/UP (TOWARDS HOME)

        if idx > 0:

            if unprocessed_status_data[idx-1][1] < unprocessed_status_data[idx][1]:
                x_dir = -1
            elif unprocessed_status_data[idx-1][1] > unprocessed_status_data[idx][1]:
                x_dir = 1
            else:
                x_dir = 0

            if unprocessed_status_data[idx-1][2] < unprocessed_status_data[idx][2]:
                y_dir = -1
            elif unprocessed_status_data[idx-1][2] > unprocessed_status_data[idx][2]:
                y_dir = 1
            else:
                y_dir = 0

            if unprocessed_status_data[idx-1][3] < unprocessed_status_data[idx][3]:
                z_dir = 1
            elif unprocessed_status_data[idx-1][3] > unprocessed_status_data[idx][3]:
                z_dir = -1
            else:
                z_dir = 0

        else:
            x_dir = 0
            y_dir = 0
            z_dir = 0 

        return x_dir, y_dir, z_dir


    def send_data_through_publisher(self, sn_for_db, stage_id):
        
        publisher = DataPublisher(sn_for_db)

        if not self.processed_running_data[str(stage_id)][0]:
            Logger.warning("No status data to send for stage id: " + str(stage_id))
            return False

        response = publisher.run_data_send(*self.processed_running_data[str(stage_id)])
        Logger.debug("Received %s from consumer" % response)
        return response

    def send_ssh_keys(self, serial, key):
        with self.ssh_conn.cursor() as cursor:
            query = "INSERT INTO public_keys (ConsoleSerial, PublicKey) VALUES (%s, %s)"

            params = [serial, key]

            cursor.execute(query, params)

        self.ssh_conn.commit()

    def get_ssh_key(self, serial):
        with self.ssh_conn.cursor() as cursor:
            query = "SELECT * FROM public_keys WHERE ConsoleSerial = %s"

            params = [serial]

            cursor.execute(query, params)

            key = cursor.fetchone()
            return key

    def delete_ssh_key(self, serial):
        with self.ssh_conn.cursor() as cursor:
            query = "DELETE FROM public_keys WHERE ConsoleSerial = %s"

            params = [serial]

            cursor.execute(query, params)


