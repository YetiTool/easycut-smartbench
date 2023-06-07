import os
import sys
import mock

sys.path.append('./src')

from asmcnc.production.database.factory_payload_sender import get_csv, send_csv_to_ftp, CSV_PATH

CSV_PATH = 'src/' + CSV_PATH

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_factory_payload_sender.py
######################################
'''

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
