import pika
import uuid
import csv
import json
import paramiko
import traceback
from datetime import datetime

CSV_PATH = './asmcnc/production/database/csvs/'
QUEUE = 'calibration_data'
WORKING_DIR = 'C:\\CalibrationReceiver\\CSVS\\'


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


def get_unique_file_name(machine_serial, table, stage):
    return str(machine_serial) + '-' + str(table) + '-' + str(stage) + '-' + str(uuid.uuid4()) + '.csv'


status_order = {
    "Id": 1,
    "FTID": 2,
    "XCoordinate": 3,
    "YCoordinate": 4,
    "ZCoordinate": 5,
    "XDirection": 6,
    "YDirection": 7,
    "ZDirection": 8,
    "XSG": 9,
    "YSG": 10,
    "Y1SG": 11,
    "Y2SG": 12,
    "ZSG": 13,
    "TMCTemperature": 14,
    "PCBTemperature": 15,
    "MOTTemperature": 16,
    "Timestamp": 17,
    "Feedrate": 18,
    "XWeight": 19,
    "YWeight": 20,
    "ZWeight": 21
}


def json_to_csv(data, machine_serial, table, stage):
    file_path = CSV_PATH + get_unique_file_name(machine_serial, table, stage)

    keys = data[0].keys()
    keys.sort(key=lambda i: status_order[i])

    with open(file_path, 'w') as data_file:
        dict_writer = csv.DictWriter(data_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    return file_path


class DataPublisher(object):
    def __init__(self, machine_serial):
        from asmcnc.production.database import credentials as creds
        self.creds = creds

        self.machine_serial = machine_serial

        pika_credentials = pika.PlainCredentials(
            username='calibration',
            password=creds.password
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='51.68.204.96',
                credentials=pika_credentials
            )
        )

        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue=QUEUE,
            durable=True
        )

    def send_file_paramiko_sftp(self, file_path):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.creds.ftp_server, username=self.creds.ftp_username, password=self.creds.ftp_password)
        sftp = ssh.open_sftp()

        file_name = file_path.split('/')[-1]
        sftp.put(file_path, WORKING_DIR + file_name)

    def publish(self, data):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=QUEUE,
                body=json.dumps(data)
            )
            return True
        except:
            print(traceback.format_exc())
            return False

    def run_data_send(self, statuses, table, stage):
        csv_name = json_to_csv(statuses, self.machine_serial, table, stage)
        self.send_file_paramiko_sftp(csv_name)

        raw_file_name = csv_name.split('/')[-1]

        payload = {
            'Stage': stage,
            'MachineSerial': self.machine_serial,
            'FileName': raw_file_name,
            'Table': table
        }

        return self.publish(payload)

# import datetime
# import random
#
#
# def gfloat(a, b):
#     return random.uniform(a, b)
#
#
# def gint(a, b):
#     return random.randint(a, b)
#
#
# def generate_status():
#     return {
#         "Id": "",
#         "FTID": gint(1000, 6000),
#         "XCoordinate": gfloat(0, 3000), "YCoordinate": gfloat(0, 3000), "ZCoordinate": gfloat(0, 3000),
#         "XDirection": gint(0, 1), "YDirection": gint(0, 1), "ZDirection": gint(0, 1),
#         "XSG": gint(0, 250), "YSG": gint(0, 250), "Y1SG": gint(0, 250), "Y2SG": gint(0, 250), "ZSG": gint(0, 250),
#         "TMCTemperature": gint(30, 80), "PCBTemperature": gint(30, 80), "MOTTemperature": gint(30, 80),
#         "Timestamp": datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
#         "Feedrate": gint(0, 1500),
#         "XWeight": gint(0, 10), "YWeight": gint(0, 10), "ZWeight": gint(0, 10)
#     }
#
#
# def generate_payload():
#     return [generate_status() for _ in range(0, 10)]
#
#
# if __name__ == '__main__':
#     serial = 'YS6139'
#
#     publisher = DataPublisher(serial)
#
#     publisher.run_data_send(generate_payload(), "FinalTestStatuses")
