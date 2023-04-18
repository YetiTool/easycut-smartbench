import os
import sys
import mock

sys.path.append('./src')

from asmcnc.production.database.factory_payload_sender import get_csv, send_csv_to_ftp, CSV_PATH

CSV_PATH = 'src/' + CSV_PATH


def test_get_csv():
    json = [{
        'Id': 0,
        'Test': 'Example2'
    }]

    machine_serial = '123456'
    table = 'testingtable'

    file_path = get_csv(json, machine_serial, table, csv_path=CSV_PATH)

    assert os.path.exists(file_path)
    return file_path


def test_send_csv_to_ftp():
    file_path = test_get_csv()

    send_csv_to_ftp(file_path)


def test_screen_calibration_data_sends():
    from asmcnc.apps.systemTools_app.screens.calibration.screen_calibration_test import CalibrationTesting

    m = mock.Mock()
    systemtools_sm = mock.Mock()
    calibration_database = mock.Mock()
    sm = mock.Mock()
    l = mock.Mock()

    calibration_test = CalibrationTesting(m=m, systemtools=systemtools_sm,
                                          calibration_db=calibration_database, sm=sm, l=l)

    example_status_payload = {
        "UnweightedFT": [
            {
                "Id": None,
                "FTID": 100000000,
                "XCoordinate": 0,
                "YCoordinate": 0,
                "ZCoordinate": 0,
                "XDirection": 0,
                "YDirection": 0,
                "ZDirection": 0,
                "XSG": 0,
                "YSG": 0,
                "Y1SG": 0,
                "Y2SG": 0,
                "ZSG": 0,
                "TMCTemperature": 0,
                "MOTTemperature": 0,
                "PCBTemperature": 0,
                "Timestamp": "2018-01-01 00:00:00",
                "Feedrate": 0,
                "XWeight": 0,
                "YWeight": 0,
                "ZWeight": 0,
            }
        ]
    }

    example_statistic_payload = {
        "UnweightedFT": [
            {
                "Id": None,
                "FTID": 100000000,
                "XForwardAvg": 0,
                "XForwardPeak": 0,
                "XBackwardAvg": 0,
                "XBackwardPeak": 0,
                "YForwardAvg": 0,
                "YForwardPeak": 0,
                "YBackwardAvg": 0,
                "YBackwardPeak": 0,
                "Y1ForwardAvg": 0,
                "Y1ForwardPeak": 0,
                "Y1BackwardAvg": 0,
                "Y1BackwardPeak": 0,
                "Y2ForwardAvg": 0,
                "Y2ForwardPeak": 0,
                "Y2BackwardAvg": 0,
                "Y2BackwardPeak": 0,
                "ZForwardAvg": 0,
                "ZForwardPeak": 0,
                "ZBackwardAvg": 0,
                "ZBackwardPeak": 0,
            }
        ]
    }

    calibration_test.sn_for_db = 'ys1000000000'
    calibration_test.status_data_dict['UnweightedFT'] = example_status_payload['UnweightedFT']
    calibration_test.statistics_data_dict['UnweightedFT'] = example_statistic_payload['UnweightedFT']

    sent = calibration_test.send_data_for_each_stage('UnweightedFT',
                                                     csv_path=CSV_PATH)

    assert sent


def test_screen_overnight_data_sends():
    from asmcnc.apps.systemTools_app.screens.calibration.screen_overnight_test import OvernightTesting

    m = mock.Mock()
    systemtools_sm = mock.Mock()
    calibration_database = mock.Mock()
    sm = mock.Mock()
    l = mock.Mock()

    overnight_test = OvernightTesting(m=m, systemtools=systemtools_sm,
                                      calibration_db=calibration_database, sm=sm, l=l)

    example_status_payload = {
        "OvernightWearIn": {
            "Table": "FinalTestStatuses",
            "Statuses": [
                {
                    "Id": None,
                    "FTID": 100000000,
                    "XCoordinate": 0,
                    "YCoordinate": 0,
                    "ZCoordinate": 0,
                    "XDirection": 0,
                    "YDirection": 0,
                    "ZDirection": 0,
                    "XSG": 0,
                    "YSG": 0,
                    "Y1SG": 0,
                    "Y2SG": 0,
                    "ZSG": 0,
                    "TMCTemperature": 0,
                    "MOTTemperature": 0,
                    "PCBTemperature": 0,
                    "Timestamp": "2018-01-01 00:00:00",
                    "Feedrate": 0,
                    "XWeight": 0,
                    "YWeight": 0,
                    "ZWeight": 0,
                }
            ]
        }
    }

    example_statistic_payload = {
        "OvernightWearIn": {
            "Table": "FinalTestStatuses",
            "Statuses": [
                {
                    "Id": None,
                    "FTID": 100000000,
                    "XForwardAvg": 0,
                    "XForwardPeak": 0,
                    "XBackwardAvg": 0,
                    "XBackwardPeak": 0,
                    "YForwardAvg": 0,
                    "YForwardPeak": 0,
                    "YBackwardAvg": 0,
                    "YBackwardPeak": 0,
                    "Y1ForwardAvg": 0,
                    "Y1ForwardPeak": 0,
                    "Y1BackwardAvg": 0,
                    "Y1BackwardPeak": 0,
                    "Y2ForwardAvg": 0,
                    "Y2ForwardPeak": 0,
                    "Y2BackwardAvg": 0,
                    "Y2BackwardPeak": 0,
                    "ZForwardAvg": 0,
                    "ZForwardPeak": 0,
                    "ZBackwardAvg": 0,
                    "ZBackwardPeak": 0,
                }
            ]
        }
    }

    overnight_test.sn_for_db = 'ys1000000000'
    overnight_test.status_data_dict['OvernightWearIn'] = example_status_payload['OvernightWearIn']
    overnight_test.statistics_data_dict['OvernightWearIn'] = example_statistic_payload['OvernightWearIn']

    sent = overnight_test.send_data('OvernightWearIn',
                                    csv_path=CSV_PATH)

    assert sent