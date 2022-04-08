# RUN THIS INTERACTIVELY TO INSERT STAGES INTO DATABASE

from asmcnc.production.database.calibration_database import CalibrationDatabase

calibration_db = CalibrationDatabase()
calibration_db.set_up_connection()


## STAGES ADDED:
# calibration_db.insert_stage("CalibrationQC")
# calibration_db.insert_stage("CalibrationCheckQC")
# calibration_db.insert_stage("UnweightedFT")
# calibration_db.insert_stage("WeightedFT")
# calibration_db.insert_stage("OvernightWearIn")
# calibration_db.insert_stage("CalibrationOT")
# calibration_db.insert_stage("CalibrationCheckOT")
# calibration_db.insert_stage("FullyCalibratedTest")


def get_all_serials_by_machine_serial(self, machine_serial):

	
with calibration_db.conn.cursor() as cursor:
    query = "SELECT + \
            ZHeadSerialNumber, + \
            LowerBeamSerialNumber, + \
            UpperBeamSerialNumber, + \
            ConsoleSerialNumber, + \
            YBenchSerialNumber, + \
            SpindleSerialNumber, + \
            Squareness + \
            FROM Machines WHERE MachineSerialNumber = '%s'" % machine_serial

    cursor.execute(query)

    data = cursor.fetchone()

    return [data[0], data[1], data[2], data[3], data[4], data[5], data[6]]