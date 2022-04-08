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